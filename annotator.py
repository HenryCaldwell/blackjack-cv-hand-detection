"""
Module for annotating frames with detection and scoring information.

This module provides functionality to visually annotate an image frame by drawing 
bounding boxes around detected cards and overlaying text labels that include the 
card value, hand grouping, and total score for each hand.
"""

import cv2

def annotate_frame_with_scores(frame, boxes, groups, labels, hand_totals):
  """
  Annotates the given frame by drawing bounding boxes with labels in the format:
  
    Value of card (HAND X, Y)
    
  where X is the hand number and Y is the total score for that hand.
  
  Parameters:
    frame (numpy.ndarray): The input video frame.
    boxes (list): A list of bounding boxes [x1, y1, x2, y2].
    groups (list): A list of groups (hands), each a list of indices.
    labels (list): A list of card labels corresponding to each bounding box.
    hand_totals (dict): A mapping from hand number (starting at 1) to its total score.
  
  Returns:
    numpy.ndarray: The annotated frame.
  """
  colors = [(255, 255, 255)] # Color palette options for the hands.
  box_to_hand = {} # Mapping from box index to hand number.

  # Assign each box to a hand.
  for hand_num, group in enumerate(groups, start=1):
    for idx in group:
      box_to_hand[idx] = hand_num

  # Annotate the frame with bounding boxes and labels.
  for idx, box in enumerate(boxes):
    hand_num = box_to_hand.get(idx, 0) # Hand number for the box.
    card = labels[idx] if idx < len(labels) else "" # Card label for the box.

    # Include hand number and total score if available.
    if hand_num:
      total = hand_totals.get(hand_num, 0)
      text = f"{card} (HAND {hand_num}, {total})"
    else:
      text = card  # In case the card isn't grouped.

    x1, y1, x2, y2 = map(int, box) # Bounding box coordinates.
    color = colors[(hand_num - 1) % len(colors)] if hand_num else (0, 255, 0) # Color for the box (Iterates through available colors).
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=4) # Draw bounding box.
    cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2) # Add label.

  return frame