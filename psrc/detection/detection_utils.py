"""
Module for detection utilities.

This module provides helper functions for card detection tasks, including computing the overlap ratio between 
bounding boxes and grouping detected cards into hands based on spatial relationships.
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

def group_cards(boxes, overlap_threshold=0.1):
  """
  Groups bounding boxes into hands based on their overlap.
  
  Each bounding box (expressed as [x1, y1, x2, y2]) is treated as a node in a graph. An edge is added between two
  nodes if their overlap (computed via compute_overlap) is at least the overlap threshold. A depth-first search
  (DFS) is then used to find connected components, where each component represents a hand.
  
  Parameters:
    boxes (list): A list of bounding boxes.
    overlap_threshold (float, optional): Minimum overlap ratio to connect two boxes. Defaults to 0.1.
  
  Returns:
    list: A list of groups, where each group is a list of indices corresponding to bounding boxes that form a hand.
  """
  n = len(boxes)
  graph = {i: [] for i in range(n)}
  
  # Add edges between boxes with sufficient overlap
  for i in range(n):
    for j in range(i + 1, n):
      if compute_overlap(boxes[i], boxes[j]) >= overlap_threshold:
        graph[i].append(j)
        graph[j].append(i)
  
  visited = [False] * n
  groups = []

  # Find connected components using DFS
  for i in range(n):
    if not visited[i]:
      stack = [i]
      group = []

      while stack:
        node = stack.pop()

        if not visited[node]:
          visited[node] = True
          group.append(node)
          stack.extend(graph[node])

      groups.append(group)

  # Separate groups into player hands and dealer hand
  player_hands = []
  dealer_hand = []

  for group in groups:
    if len(group) == 1:
      dealer_hand.extend(group)
    else:
      player_hands.append(group)

  if not dealer_hand:
    dealer_hand = None

  return {"player_hands": player_hands, "dealer_hand": dealer_hand}