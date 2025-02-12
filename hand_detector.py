"""
Module for hand detection and grouping.

This module provides functions to group detected cards into hands based on spatial relationships. It leverages
the overlap computation from the utils module to decide which cards belong together.
"""

from utils import compute_overlap

def group_cards(boxes, threshold=0.1):
  """
  Groups bounding boxes into hands based on their overlap.
  
  Each bounding box (expressed as [x1, y1, x2, y2]) is treated as a node in a graph. An edge is added between two
  nodes if their overlap (computed via compute_overlap) is at least the threshold. A depth-first search (DFS) is
  then used to find connected components, where each component represents a hand.
  
  Parameters:
    boxes (list): A list of bounding boxes.
    threshold (float, optional): Minimum overlap ratio to connect two boxes. Defaults to 0.1.
  
  Returns:
    list: A list of groups, where each group is a list of indices corresponding to bounding boxes that form a hand.
  """
  n = len(boxes)
  graph = {i: [] for i in range(n)}
  
  # Add edges between boxes with sufficient overlap
  for i in range(n):
    for j in range(i + 1, n):
      if compute_overlap(boxes[i], boxes[j]) >= threshold:
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

  return groups