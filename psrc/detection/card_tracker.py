"""
Module for tracking cards detected in video frames.

This module defines the CardTracker class, which encapsulates the functionality to track card objects across
consecutive frames based on detection boxes. It manages confirmation of tracked cards, removal of cards that
disappear, and can trigger a callback when a card is locked.
"""

from typing import List, Dict, Callable, Optional, Any
from detection.detection_utils import compute_overlap

class CardTracker:
  """
  A class to track card objects across video frames based on detection boxes.

  The CardTracker maintains tracking information for cards detected in consecutive frames. It confirms a card
  when it appears consistently for a set number of frames and removes cards that disappear for too long. A
  callback can be triggered when a card is locked.
  """
  
  def __init__(
    self, confirmation_frames: int, 
    disappear_frames: int, confidence_threshold: float, 
    overlap_threshold: float, on_lock_callback: Optional[Callable[[str], None]] = None
  ) -> None:
    """
    Initialize the CardTracker instance.

    Parameters:
      confirmation_frames (int): Number of consecutive frames required to confirm and lock tracking for a card.
      disappear_frames (int): Number of frames allowed for a card to not be detected before it is removed.
      confidence_threshold (float): The minimum confidence required to start tracking a new card.
      overlap_threshold (float): The minimum overlap ratio between boxes to consider them as the same card.
      on_lock_callback (callable, optional): A function to be called when a card becomes locked.
    """
    self.confirmation_frames = confirmation_frames
    self.disappear_frames = disappear_frames
    self.confidence_threshold = confidence_threshold
    self.overlap_threshold = overlap_threshold
    self.on_lock_callback = on_lock_callback
    self.tracked_cards = {}

  def update(
    self, boxes: List[List[float]],
    labels: List[str], confidences: List[float]
  ) -> List[str]:
    """
    Update the tracked cards based on new detection boxes.

    Compares the incoming detection boxes with the existing tracked cards. It increments frame counts for matched
    cards, locks them when confirmed, and handles cards that are not detected in the current frame.

    Parameters:
      boxes (list): List of bounding boxes for detected cards.
      labels (list): List of corresponding labels for each box.
      confidences (list): List of detection confidence scores.

    Returns:
      list: A list of labels to be displayed for the current frame.
    """
    new_tracked = {}
    displayed_labels = []

    # Iterate over each detected box
    for i, box in enumerate(boxes):
      label = labels[i]
      confidence = confidences[i]
      matched = False
      
      # Compare current box with previously tracked cards
      for prev_box, info in self.tracked_cards.items():
        if compute_overlap(box, list(prev_box)) >= self.overlap_threshold:
          info["frame_count"] += 1  # If match is found, update the frame count

          # Lock the card if confirmed and not already locked
          if info["frame_count"] >= self.confirmation_frames and not info["locked"]:
            if self.on_lock_callback:
              self.on_lock_callback(info["label"])

            info["locked"] = True

          new_tracked[tuple(box)] = info
          matched = True
          break

      # If no existing card matches, add a new card to tracking if confidence is sufficient
      if not matched:
        initial_count = 1 if confidence >= self.confidence_threshold else 0
        new_tracked[tuple(box)] = {
          "label": label,
          "confidence": confidence,
          "frame_count": initial_count,
          "locked": False
        }

    # Process tracked cards that were not detected in the current frame
    for prev_box, info in self.tracked_cards.items():
      if prev_box not in new_tracked:
        info["frame_count"] += 1

        if info["frame_count"] < self.disappear_frames:
          new_tracked[prev_box] = info

    self.tracked_cards = new_tracked  # Update the tracked cards with new tracking information

    # Prepare labels for display based on the updated tracking info
    for box in boxes:
      found = False

      for tracked_box, info in self.tracked_cards.items():
        if compute_overlap(box, list(tracked_box)) >= self.overlap_threshold:
          displayed_labels.append(info["label"] if info["frame_count"] >= self.confirmation_frames else labels[boxes.index(box)])
          found = True
          break

      if not found:
        displayed_labels.append(labels[boxes.index(box)])

    return displayed_labels