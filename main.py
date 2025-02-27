"""
Main module for card detection, grouping, scoring, and annotation.

This module ties together the various components (inference, grouping, tracking, scoring, and annotation) to
process a video stream of card detections. It manages the application loop, processes each frame, and displays
the annotated output.
"""

import os
import cv2
import time
from ultralytics import YOLO
from detection.inference import run_inference
from detection.hand_detector import group_cards
from game.blackjack_utils import calculate_hand_score
from detection.annotator import annotate_frame_with_scores
from config import Config
from game.deck import CardDeck
from detection.card_tracker import CardTracker

class CardDetectionApp:
  def __init__(self, config):
    """
    Initializes the CardDetectionApp with the specified configuration.
    
    Parameters:
      config (Config): An instance of the configuration containing all adjustable parameters.
    
    Raises:
      FileNotFoundError: If the YOLO weights file or video file is not found.
    """
    self.config = config
    
    # Check that the YOLO weights file exists
    if not os.path.exists(config.yolo_path):
      raise FileNotFoundError(f"YOLO weights file not found at '{config.yolo_path}'.")
    
    # Use webcam if enabled, otherwise check that the video file exists
    if config.use_webcam:
      self.cap = cv2.VideoCapture(config.webcam_index)
    else:
      if not os.path.exists(config.video_path):
        raise FileNotFoundError(f"Video file not found at '{config.video_path}'.")
      self.cap = cv2.VideoCapture(config.video_path)

    # Initialize YOLO model, video capture, and tracking parameters
    self.model = YOLO(config.yolo_path)
    self.last_update = 0.0
    self.annotated_frame = None
    self.deck = CardDeck(config.deck_size)
    self.tracker = CardTracker(
      confirmation_frames=config.confirmation_frames,
      disappear_frames=config.disappear_frames,
      confidence_threshold=config.confidence_threshold,
      overlap_threshold=config.inference_overlap_threshold,
      deck=self.deck
    )
  
  def process_frame(self, frame):
    """
    Processes a single video frame: runs detection, tracking, grouping, scoring, and annotation.
    
    Parameters:
      frame (numpy.ndarray): The input video frame.
    
    Returns:
      numpy.ndarray: The annotated frame with detection boxes, labels, hand grouping, and scores.
    """
    # Run YOLO inference
    boxes, labels, confidences = run_inference(
      frame, self.model, overlap_threshold=self.config.inference_overlap_threshold
    )

    stable_labels = self.tracker.update(boxes, labels, confidences)  # Update tracker to obtain stable labels
    hands_dict = group_cards(boxes, threshold=self.config.overlap_threshold) if boxes else {"player_hands": [], "dealer_hand": None} # Group cards using the updated grouping function
    hand_totals = {}  # Dictionary to store total scores for each hand

    # Calculate totals for player hands
    hand_num = 1

    for group in hands_dict.get("player_hands", []):
      player_cards = [stable_labels[idx] for idx in group if idx < len(stable_labels)]
      player_score = calculate_hand_score(player_cards)
      hand_totals[hand_num] = player_score
      hand_num += 1
      print(f"HAND {hand_num}; {player_score}")

    if hands_dict.get("dealer_hand") is not None:
      dealer_cards = [stable_labels[idx] for idx in hands_dict["dealer_hand"] if idx < len(stable_labels)]
      dealer_score = calculate_hand_score(dealer_cards)
      hand_totals["dealer"] = dealer_score
      print(f"DEALER HAND; {dealer_score}")

    # Annotate the frame with detection and scoring details
    annotated = annotate_frame_with_scores(frame.copy(), boxes, hands_dict, stable_labels, hand_totals)

    return annotated

  def run(self):
    """
    Runs the main application loop: reads video frames, processes them, and displays the annotated results.
    Exits the loop when the video ends or 'q' is pressed.
    """
    while True:
      ret, frame = self.cap.read()

      if not ret:
        break

      inference_frame = cv2.resize(frame, self.config.inference_frame_size)
      current_time = time.time()

      # Process the frame only if the inference interval has passed
      if current_time - self.last_update >= self.config.inference_interval:
        annotated_frame = self.process_frame(inference_frame)
        self.last_update = current_time
        print(f"DECK COMP; {self.deck.get_counts()}")
        print(f"RUNNING COUNT; {self.deck.get_running_count()} TRUE COUNT; {self.deck.get_true_count()}")
      else:
        annotated_frame = self.annotated_frame if self.annotated_frame is not None else inference_frame

      self.annotated_frame = annotated_frame

      display_frame = cv2.resize(annotated_frame, self.config.display_frame_size)
      cv2.imshow("Card Detection & Scoring", display_frame)

      # Exit on 'q' key press
      if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    self.cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
  config = Config()
  app = CardDetectionApp(config)
  app.run()