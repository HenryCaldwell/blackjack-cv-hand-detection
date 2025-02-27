"""
Module for running YOLO inference and applying Non-Maximum Suppression (NMS).

This module handles the execution of a YOLO model on an input frame to detect cards, then applies NMS to filter
out overlapping detections based on a specified overlap threshold.
"""

import numpy as np
from ultralytics import YOLO
from python.detection.detection_utils import compute_overlap

def run_inference(frame, model, overlap_threshold=0.9):
  """
  Runs YOLO inference on the given frame, applies NMS, and returns filtered detections.
  
  Parameters:
    frame (numpy.ndarray): The input image frame.
    model (YOLO): A YOLO model instance configured for card detection.
    overlap_threshold (float, optional): Overlap threshold for NMS. Defaults to 0.9.
  
  Returns:
    tuple: (filtered_boxes, filtered_labels, filtered_confidences)
  """
  results = model(frame, show=False)  # Run inference on the frame
  last_results = results[0]  # Get the latest results
  boxes, labels, confidences = [], [], []  # Initialize lists for boxes, labels, and confidences
  
  # Extract boxes, labels, and confidences from the results
  if last_results is not None and last_results.boxes is not None:
    boxes = last_results.boxes.xyxy.cpu().numpy().tolist()
    confidences = last_results.boxes.conf.cpu().numpy().tolist()

    # Map class indices to card labels
    if hasattr(last_results.boxes, 'cls'):
      class_indices = last_results.boxes.cls.cpu().numpy().tolist()

      card_map = {
          0: "A", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6",
          6: "7", 7: "8", 8: "9", 9: "10", 10: "J", 11: "Q", 12: "K"
      }

      labels = [card_map.get(int(idx), "?") for idx in class_indices]
  
  filtered_boxes, filtered_labels, filtered_confidences = apply_nms(boxes, labels, confidences, overlap_threshold)  # Apply NMS to filter detections
  return filtered_boxes, filtered_labels, filtered_confidences

def apply_nms(boxes, labels, confidences, overlap_threshold):
  """
  Applies Non-Maximum Suppression (NMS) to remove overlapping bounding boxes.
  
  Parameters:
    boxes (list): List of bounding boxes in the format [x1, y1, x2, y2].
    labels (list): List of labels corresponding to the boxes.
    confidences (list): List of confidence scores for each bounding box.
    overlap_threshold (float): Overlap threshold above which a box is suppressed.
  
  Returns:
    tuple: (filtered_boxes, filtered_labels, filtered_confidences)
  """
  if not boxes:
    return [], [], []
  
  boxes_np = np.array(boxes)
  confidences_np = np.array(confidences)
  indices = sorted(range(len(confidences_np)), key=lambda i: confidences_np[i], reverse=True)
  
  keep = []  # List to hold indices of boxes to keep

  # Iterate through indices and apply NMS
  while indices:
    i = indices.pop(0)
    keep.append(i)
    indices = [j for j in indices if compute_overlap(boxes_np[i], boxes_np[j]) < overlap_threshold]
  
  filtered_boxes = [boxes_np[i].tolist() for i in keep]
  filtered_labels = [labels[i] for i in keep]
  filtered_confidences = [confidences_np[i] for i in keep]
  
  return filtered_boxes, filtered_labels, filtered_confidences