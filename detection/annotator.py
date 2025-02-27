"""
Module for annotating frames with detection and scoring information.

This module provides functionality to visually annotate an image frame by drawing bounding boxes around detected
cards and overlaying text labels that include the card value, hand grouping, and total score for each hand. This
visualization helps in real-time monitoring of detection and scoring performance.
"""

import cv2

def annotate_frame_with_scores(frame, boxes, hands_dict, labels, hand_totals):
  """
  Annotates the given frame with bounding boxes and labels, taking into account the new grouping format.
  
  The hands_dict is expected to be a dictionary with two keys:
    - "player_hands": A list of groups (lists of indices) for player hands.
    - "dealer_hand": A list of indices for the dealer hand (or None).
  
  For each detected card, a bounding box is drawn along with a label. If the detection belongs to a player hand,
  the label is formatted as "card (HAND X, total)". If it belongs to the dealer hand (merged singleton group),
  it is labeled as "card (DEALER, total)".
  
  Parameters:
    frame (numpy.ndarray): The image frame to annotate.
    boxes (list): List of bounding boxes in the format [x1, y1, x2, y2].
    hands_dict (dict): Dictionary with keys "player_hands" and "dealer_hand" from the grouping function.
    labels (list): List of card labels corresponding to each bounding box.
    hand_totals (dict): Dictionary mapping hand number (or "dealer") to its total score.
  
  Returns:
    numpy.ndarray: The annotated frame.
  """
  colors = [(255, 255, 255)]  # Color palette for the hands
  box_to_hand = {}  # Map each box index to its hand number

  hand_num = 1

  # Assign player hand numbers
  for group in hands_dict.get("player_hands", []):
    for idx in group:
      box_to_hand[idx] = hand_num
    hand_num += 1

  # Assign the dealer hand a special number (e.g., 0) if it exists
  if hands_dict.get("dealer_hand") is not None:
    for idx in hands_dict["dealer_hand"]:
      box_to_hand[idx] = 0

  # Draw bounding boxes and overlay labels
  for idx, box in enumerate(boxes):
    assigned_hand = box_to_hand.get(idx, None)
    card = labels[idx] if idx < len(labels) else ""

    if assigned_hand is not None:
      if assigned_hand == 0:
        total = hand_totals.get("dealer", 0)
        text = f"{card} (DEALER, {total})"
      else:
        total = hand_totals.get(assigned_hand, 0)
        text = f"{card} (HAND {assigned_hand}, {total})"
    else:
      text = card

    x1, y1, x2, y2 = map(int, box)
    color = colors[(assigned_hand - 1) % len(colors)] if assigned_hand and assigned_hand != 0 else (0, 255, 0)
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=4)
    cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
  
  return frame