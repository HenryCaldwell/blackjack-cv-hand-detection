"""
Main module for card detection, hand grouping, scoring, and annotation.

This module loads a YOLO model, reads a video file, and processes each frame by:
  - Running YOLO inference to detect cards.
  - Grouping detected cards into hands.
  - Calculating scores for each hand.
  - Annotating the frame with the card values, hand numbers, and scores.

Configuration variables at the bottom allow you to set the YOLO weights path, video path, and update interval.
"""

import os
import cv2
import time
from ultralytics import YOLO
from inference import run_inference
from hand_detector import group_cards
from scorer import calculate_hand_score
from annotator import annotate_frame_with_scores

def main(yolo_path, video_path, update_interval):
  """
  Main function that runs the video stream, processes each frame using the YOLO model,
  detects and groups cards into hands, calculates each hand's score, and annotates the frame
  with labels in the format:

    Value of card (HAND X, Y)

  Parameters:
    yolo_path (str): Path to the YOLO weights file.
    video_path (str): Path to the video file to process.
    update_interval (float): Time interval (in seconds) between inference updates.
  """
  # Error check for YOLO weights file.
  if not os.path.exists(yolo_path):
    print(f"Error: YOLO weights file not found at '{yolo_path}'.")
    return
  
  model = YOLO(yolo_path)
  cap = cv2.VideoCapture(video_path)

  #  Error check for video file.
  if not cap.isOpened():
    print(f"Error: video file not found at '{video_path}'.")
    return

  last_update = 0.0
  annotated_frame = None

  # Process each frame of the video stream.
  while True:
    ret, frame = cap.read() # Read the next frame.

    # Break if no frame is read.
    if not ret:
      break

    frame = cv2.resize(frame, (1280, 720)) # Resize the frame for display.
    current_time = time.time() # Get the current time.

    # Perform inference and update the frame if the interval has elapsed.
    if current_time - last_update >= update_interval:
      boxes, labels = run_inference(frame, model) # Run YOLO inference.
      last_update = current_time # Update the last update time.
      groups = group_cards(boxes, threshold=0.1) if boxes else [] # Group detected cards into hands.
      hand_totals = {} # Mapping from hand number to total score.

      # Calculate the score for each hand.
      for hand_num, group in enumerate(groups, start=1):
        hand_cards = [labels[idx] for idx in group if idx < len(labels)] # Extract card labels for the hand.
        score = calculate_hand_score(hand_cards) # Calculate the hand score.
        hand_totals[hand_num] = score # Store the hand score.
        print(f"Detected hand {hand_num} has score: {score}")

      annotated_frame = annotate_frame_with_scores(frame.copy(), boxes, groups, labels, hand_totals) # Annotate the frame.
    else:
      annotated_frame = annotated_frame if annotated_frame is not None else frame # Use the previous frame if no update.

    cv2.imshow("Basic Hand Detection & Scoring", annotated_frame)

    # Break if 'q' is pressed.
    if cv2.waitKey(1) & 0xFF == ord("q"):
      break

  cap.release()
  cv2.destroyAllWindows()

# Configuration variables defined outside main.
yolo_path = "detection_weights.pt" # Path to YOLO weights file.
video_path = "test_video.mov" # Path to video file.
inference_interval = 0.25  # seconds between inference updates

if __name__ == "__main__":
  main(yolo_path, video_path, inference_interval)
