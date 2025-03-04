"""
Module for card detection and evaluation in a blackjack context.

This module defines the BlackjackVisionAnalyzer class, which integrates video capture, object detection using a
YOLO model, card tracking, hand grouping, EV (expected value) evaluation, and frame annotation. It uses various
utility modules to process video frames, detect playing cards, evaluate blackjack hands, and display annotated
results.
"""

import cv2
import time
from ultralytics import YOLO
from config import Config
from annotation.annotator import annotate_frame_with_scores
from debugging.logger import setup_logger
from detection.card_tracker import CardTracker
from detection.detection_utils import group_cards
from detection.inference import run_inference
from evaluation.deck import CardDeck
from evaluation.ev_engine import EVEngineWrapper
from evaluation.hand_utils import calculate_hand_score
from video.video_stream import VideoStreamReader

logger = setup_logger(__name__)

class BlackjackVisionAnalyzer:
  """
  Main application class for card detection, hand evaluation, and game state tracking
  in a blackjack context.

  The BlackjackVisionAnalyzer handles the initialization of video capture (webcam or video file),
  loads the YOLO model for card detection, sets up a card tracker to maintain detection consistency,
  manages a deck of cards for blackjack, and evaluates the expected value (EV) of various actions
  for player hands. It also processes video frames by annotating them with detection and evaluation data.
  """

  def __init__(self, config):
    """
    Initializes the BlackjackVisionAnalyzer with the provided configuration.

    Parameters:
      config (Config): Configuration object containing application settings such as video source, model path, deck
      size, inference intervals, and thresholds.

    The initialization process includes:
      - Setting up video capture based on whether a webcam or video file is used.
      - Loading the YOLO model for card detection.
      - Initializing a CardDeck to manage available cards.
      - Defining and initializing a CardTracker with custom callback for when a card is locked.
      - Setting up the EVEngineWrapper for evaluating blackjack hands.
    """
    self.config = config
    logger.info("Initializing BlackjackVisionAnalyzer with config: %s", config.__dict__)
    
    # Initialize video capture from webcam or video file
    if config.use_webcam:
      self.cap = VideoStreamReader(config.webcam_index)
    else:
      self.cap = VideoStreamReader(config.video_path)

    # Load the YOLO model with the specified weights
    try:
      self.model = YOLO(config.yolo_path)
    except Exception as e:
      raise FileNotFoundError(f"YOLO model file not found or invalid: {config.yolo_path}") from e
        
    # Initialize variables for frame processing
    self.last_update = 0.0
    self.annotated_frame = None

    # Initialize the deck of cards with the specified deck size
    self.deck = CardDeck(config.deck_size)
    
    # Define a callback function to remove a card from the deck when it is locked
    def on_card_locked(card_label):
      self.deck.remove_card(card_label)
    
    # Initialize the CardTracker with thresholds and callback settings
    self.tracker = CardTracker(
      confirmation_frames=config.confirmation_frames,
      disappear_frames=config.disappear_frames,
      confidence_threshold=config.confidence_threshold,
      overlap_threshold=config.inference_overlap_threshold,
      on_lock_callback=on_card_locked
    )

    # Initialize the EV engine for blackjack hand evaluation
    self.evaluator = EVEngineWrapper(jar_path="build/EVEngine.jar", java_class="jsrc.evaluation.EVEngine")

  def evaluate_hands(self, player_hands, dealer_hand):
    """
    Evaluates the expected value (EV) of different actions for each player hand against the dealer's hand.

    The method iterates over each player hand and calculates EV for standard blackjack actions:
    'stand', 'hit', 'double', and 'split'. It logs the EVs and determines the best action for each hand.

    Parameters:
      player_hands (list of lists): Each sublist contains card labels for a player's hand.
      dealer_hand (list): List of card labels representing the dealer's hand.
    """
    actions = ["stand", "hit", "double", "split"]

    for i, p_hand in enumerate(player_hands, start=1):
      evs = {}

      for action in actions:
        try:
          # Calculate EV for the given action
          ev = self.evaluator.calculate_ev(action, self.deck.get_counts(), p_hand, dealer_hand)
          evs[action] = ev
        except Exception as e:
          # Log any errors encountered during EV calculation
          logger.error("Error evaluating action '%s' for hand %d (%s): %s", action, i, p_hand, e)
      if evs:
        # Determine the best action based on the highest EV
        best_action = max(evs, key=evs.get)
        formatted_evs = {action: f"{ev * 100:.2f}%" for action, ev in evs.items()}
        logger.info("Hand %d: %s | %s", i, formatted_evs, best_action)
      else:
        logger.warning("No valid evaluation for hand %d", i)

  def process_frame(self, frame):
    """
    Processes a single video frame: runs card detection inference, tracks and groups cards,
    calculates hand scores, evaluates EV for blackjack decisions, and annotates the frame.

    Parameters:
      frame (numpy.ndarray): The video frame to process.

    Returns:
      annotated (numpy.ndarray): The frame with annotations for detected cards and evaluated scores.
    """
    # Run card detection inference using the YOLO model
    boxes, labels, confidences = run_inference(
      frame, self.model, overlap_threshold=self.config.inference_overlap_threshold
    )

    # Update the card tracker with the current detections and obtain stable labels
    stable_labels = self.tracker.update(boxes, labels, confidences) if boxes else []

    # Group detected cards into player hands and dealer hand
    grouped_hands = group_cards(boxes, overlap_threshold=self.config.overlap_threshold) if boxes else {"player_hands": [], "dealer_hand": None}
    grouped_hands_labels = {
        "player_hands": [
            [stable_labels[i] for i in group if i < len(stable_labels)]
            for group in grouped_hands.get("player_hands", [])
        ],
        "dealer_hand": [stable_labels[i] for i in grouped_hands["dealer_hand"] if i < len(stable_labels)] if grouped_hands.get("dealer_hand") is not None else None
    }
    logger.info("Hands: %s", grouped_hands_labels)

    # Process player hands based on grouped indices and stable labels
    player_hands = grouped_hands_labels.get("player_hands", [])

    # Process dealer hand if available
    dealer_hand = grouped_hands_labels.get("dealer_hand")
    
    # Calculate the blackjack score for each hand
    hand_totals = {}
    for i, hand in enumerate(player_hands, start=1):
      hand_totals[i] = calculate_hand_score(hand)
    if dealer_hand is not None:
      hand_totals["dealer"] = calculate_hand_score(dealer_hand)

    # Evaluate EV for player hands if both player and dealer hands are available
    if player_hands and dealer_hand:
      self.evaluate_hands(player_hands, dealer_hand)
    else:
      logger.info("Insufficient hands for EV evaluation")

    # Log current deck composition for debugging purposes
    logger.info("Current deck composition: %s", self.deck.get_counts())

    # Annotate the frame with detection boxes, grouped hands, labels, and hand scores
    annotated = annotate_frame_with_scores(frame.copy(), boxes, grouped_hands, stable_labels, hand_totals)
    return annotated

  def run(self):
    """
    Starts the main loop of the application.

    The main loop continuously reads frames from the video source, processes them at defined intervals,
    displays the annotated frames, and listens for a quit signal ('q'). It ensures proper release of resources
    after the loop ends.
    """
    logger.info("Starting main loop")
    
    while True:
      # Read a frame from the video capture source
      frame = self.cap.read_frame()
      if frame is None:
        logger.info("No frame received; exiting main loop")
        break

      # Resize frame for inference processing
      inference_frame = cv2.resize(frame, self.config.inference_frame_size)
      current_time = time.time()

      # Process frame only if the inference interval has elapsed
      if current_time - self.last_update >= self.config.inference_interval:
        annotated_frame = self.process_frame(inference_frame)
        self.last_update = current_time
      else:
        # Use the previously annotated frame if available, otherwise fallback to current inference frame
        annotated_frame = self.annotated_frame if self.annotated_frame is not None else inference_frame

      # Store the current annotated frame and resize for display
      self.annotated_frame = annotated_frame
      display_frame = cv2.resize(annotated_frame, self.config.display_frame_size)
      cv2.imshow("rain-vision-v1", display_frame)

      # Exit loop if 'q' key is pressed
      if cv2.waitKey(1) & 0xFF == ord("q"):
        logger.info("Quit signal received; exiting")
        break

    # Release video capture, JVM, and close display windows
    self.cap.release()
    self.evaluator.shutdown()
    cv2.destroyAllWindows()
    logger.info("Resources released; application terminated")
    

if __name__ == "__main__":
  # Create a configuration object from the Config class
  config = Config()
  # Instantiate the BlackjackVisionAnalyzer with the provided configuration
  app = BlackjackVisionAnalyzer(config)
  # Run the main application loop
  app.run()