"""
Module for annotating frames with detection and scoring information.

This module provides functionality to visually annotate an image frame by drawing bounding boxes around detected
cards and overlaying text labels that include the card value, hand grouping, and total score for each hand. This
visualization helps in real-time monitoring of detection and scoring performance.
"""

import cv2

def annotate_frame_with_scores(frame, boxes, groups, labels, hand_totals):
  """
  Annotates the given frame with bounding boxes and labels.
  
  For each detected card, a bounding box is drawn along with a text label in the format:
  
    Value of card (HAND X, Y)
  
  where X is the hand number and Y is the total score for that hand.
  
  Parameters:
    frame (numpy.ndarray): The image frame to annotate.
    boxes (list): List of bounding boxes in the format [x1, y1, x2, y2].
    groups (list): List of groups (hands), where each group is a list of box indices.
    labels (list): List of card labels corresponding to each bounding box.
    hand_totals (dict): Dictionary mapping hand number to its total score.
  
  Returns:
    numpy.ndarray: The annotated frame.
  """
  colors = [(255, 255, 255)]  # Color palette for the hands
  box_to_hand = {}  # Map each box index to its hand number

  # Map each bounding box to its corresponding hand
  for hand_num, group in enumerate(groups, start=1):
    for idx in group:
      box_to_hand[idx] = hand_num

  # Draw bounding boxes and overlay labels
  for idx, box in enumerate(boxes):
    hand_num = box_to_hand.get(idx, 0)
    card = labels[idx] if idx < len(labels) else ""

    if hand_num:
      total = hand_totals.get(hand_num, 0)
      text = f"{card} (HAND {hand_num}, {total})"
    else:
      text = card

    x1, y1, x2, y2 = map(int, box)
    color = colors[(hand_num - 1) % len(colors)] if hand_num else (0, 255, 0)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=4)
    cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
  
  return frame