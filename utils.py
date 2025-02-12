"""
Utility functions for common tasks.

This module provides utility functions that are shared across different parts of the card detection application.
It includes common operations such as computing the overlap ratio between two bounding boxes.
"""

def compute_overlap(boxA, boxB):
  """
  Computes the overlap ratio between two axis-aligned bounding boxes.
  
  Each bounding box is defined as [x1, y1, x2, y2]. The function returns the ratio of the intersection area to 
  the area of the smaller box.
  
  Parameters:
    boxA (list or tuple of float): Coordinates [x1, y1, x2, y2] for the first box.
    boxB (list or tuple of float): Coordinates [x1, y1, x2, y2] for the second box.
  
  Returns:
    float: Overlap ratio ranging from 0.0 (no overlap) to 1.0 (complete overlap relative to the smaller box).
  """
  x_left = max(boxA[0], boxB[0])
  y_top = max(boxA[1], boxB[1])
  x_right = min(boxA[2], boxB[2])
  y_bottom = min(boxA[3], boxB[3])
  
  # No overlap
  if x_right < x_left or y_bottom < y_top:
    return 0.0

  # Compute intersection area and the area of the smaller box
  intersection_area = (x_right - x_left) * (y_bottom - y_top)
  areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
  areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
  min_area = min(areaA, areaB)

  # Prevent division by zero
  if min_area == 0:
    return 0.0

  return intersection_area / min_area