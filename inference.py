"""
Module for YOLO inference for card detection.

This module provides functionality to run YOLO on an image frame and extract the 
detected bounding boxes along with their corresponding card labels. The detections
are processed to map the YOLO output classes to human-readable card labels using a
predefined card mapping.
"""

from ultralytics import YOLO

def run_inference(frame, model):
  """
  Runs YOLO inference on an input frame and maps detections to card labels.

  Parameters:
    frame (numpy.ndarray): The image frame to process.
    model (YOLO): A YOLO model instance configured for card detection.

  Returns:
    tuple: A tuple containing:
      - boxes (list): Detected bounding boxes formatted as [x1, y1, x2, y2].
      - labels (list): Card labels corresponding to each bounding box, mapped via a predefined card map.
  """
  results = model(frame, show=False) # Perform inference.
  last_results = results[0] # Get the most recent results.
  boxes = [] # Detected bounding boxes.
  labels = [] # Card labels.

  # Extract bounding boxes and labels from the results.
  if last_results is not None and last_results.boxes is not None:
    boxes = last_results.boxes.xyxy.cpu().numpy().tolist() # Get bounding boxes.

    if hasattr(last_results.boxes, 'cls'):
      class_indices = last_results.boxes.cls.cpu().numpy().tolist() # Get class indices.

      # Map class indices to card labels.
      card_map = {
        0: "A", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6",
        6: "7", 7: "8", 8: "9", 9: "10", 10: "J", 11: "Q", 12: "K"
      }

      labels = [card_map.get(int(idx), "?") for idx in class_indices] # Map class indices to card labels.

  return boxes, labels
