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
from inference import run_inference
from hand_detector import group_cards
from scorer import calculate_hand_score
from annotator import annotate_frame_with_scores
from config import Config
from deck import CardDeck
from card_tracker import CardTracker

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
    self.deck = CardDeck()
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

    stable_labels = self.tracker.update(boxes, labels, confidences)  # # Update tracker to obtain stable labels
    groups = group_cards(boxes, threshold=self.config.overlap_threshold) if boxes else []  # Group cards based on spatial overlap
    hand_totals = {}  # Dictionary to store total scores for each hand

    # Calculate scores for each hand and print the results
    for hand_num, group in enumerate(groups, start=1):
      hand_cards = [stable_labels[idx] for idx in group if idx < len(stable_labels)]
      score = calculate_hand_score(hand_cards)
      hand_totals[hand_num] = score
      print(f"Detected hand {hand_num} has score: {score}")

    # Annotate the frame with detection and scoring details
    annotated = annotate_frame_with_scores(frame.copy(), boxes, groups, stable_labels, hand_totals)

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

      frame = cv2.resize(frame, (1280, 720))
      current_time = time.time()

      # Process the frame only if the inference interval has passed
      if current_time - self.last_update >= self.config.inference_interval:
        annotated_frame = self.process_frame(frame)
        self.last_update = current_time
        print("Deck Composition: ", self.deck.get_counts())
      else:
        annotated_frame = self.annotated_frame if self.annotated_frame is not None else frame

      self.annotated_frame = annotated_frame
      cv2.imshow("Card Detection & Scoring", annotated_frame)

      # Exit on 'q' key press
      if cv2.waitKey(1) & 0xFF == ord("q"):
        break

    self.cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
  config = Config()
  app = CardDetectionApp(config)
  app.run()