"""
Module for hand detection and grouping.

This module provides functions to compute overlaps between bounding boxes,
group detected cards into hands based on spatial relationships, and perform
domain-specific operations related to hand detection. It abstracts the logic
of determining which detected cards belong together, allowing for clear separation
of concerns in the overall processing pipeline.
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
  
  # No overlap.
  if x_right < x_left or y_bottom < y_top:
    return 0.0

  intersection_area = (x_right - x_left) * (y_bottom - y_top) # Area of intersection rectangle.
  areaA = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1]) # Area of box A.
  areaB = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1]) # Area of box B.
  min_area = min(areaA, areaB)

  # Prevent division by zero.
  if min_area == 0:
    return 0.0

  # Intersection over smallest box area.
  return intersection_area / min_area

def group_cards(boxes, threshold=0.1):
  """
  Groups bounding boxes into hands based on their overlap.
  
  Each bounding box (expressed as [x1, y1, x2, y2]) is treated as a node in a graph. An edge is added between
  two nodes if their overlap (via compute_overlap) is at least the threshold. A DFS then finds connected
  components; each connected component represents a hand.
  
  Parameters:
    boxes (list): A list of bounding boxes.
    threshold (float, optional): Minimum overlap ratio to connect two boxes. Defaults to 0.1.
  
  Returns:
    list: A list of groups. Each group is a list of indices corresponding to boxes that form a hand.
  """
  n = len(boxes) # Number of boxes.
  graph = {i: [] for i in range(n)} # Graph as an adjacency list.

  # Add edges between boxes with sufficient overlap.
  for i in range(n):
    for j in range(i + 1, n):
      if compute_overlap(boxes[i], boxes[j]) >= threshold:
        graph[i].append(j) # Add edge i -> j.
        graph[j].append(i) # Add edge j -> i.
  
  visited = [False] * n # Track visited nodes.
  groups = [] # List of groups (hands).

  # Perform DFS to find connected components.
  for i in range(n):
    if not visited[i]:
      stack = [i]
      group = []

      # DFS traversal.
      while stack:
        node = stack.pop()

        # Skip if already visited.
        if not visited[node]:
          visited[node] = True
          group.append(node)
          stack.extend(graph[node])

      groups.append(group) # Add connected component to groups.

  return groups
