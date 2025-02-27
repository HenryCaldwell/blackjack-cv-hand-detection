"""
Module for tracking card detections across frames.

This module provides a CardTracker class that encapsulates the logic for tracking detected cards over consecutive 
frames. It ensures that a card label is confirmed only after being stable for a specified number of frames, and 
manages detections that momentarily disappear.
"""

from python.detection.detection_utils import compute_overlap

class CardTracker:
  def __init__(self, confirmation_frames, disappear_frames, confidence_threshold, overlap_threshold, deck=None):
    """
    Initializes the CardTracker with the specified tracking parameters.
    
    Parameters:
      confirmation_frames (int): Number of consecutive frames required to confirm a card label.
      disappear_frames (int): Number of frames a card can be missing before it is forgotten.
      confidence_threshold (float): Minimum confidence required to start tracking a detection.
      overlap_threshold (float): Overlap threshold used to match boxes across frames.
    """
    self.confirmation_frames = confirmation_frames
    self.disappear_frames = disappear_frames
    self.confidence_threshold = confidence_threshold
    self.overlap_threshold = overlap_threshold
    self.deck = deck
    self.tracked_cards = {}  # Mapping: {box tuple: (stable_label, stable_confidence, frame_count, locked_flag)}

  def update(self, boxes, labels, confidences):
    """
    Updates the tracking of detected cards with the latest frame data.
    
    This method matches new detections to previously tracked cards based on overlap. If a detection is matched 
    and has been stable for the required number of frames, the stable label is used; otherwise, the new label is applied.
    It also handles detections that are temporarily missing.
    
    Parameters:
      boxes (list): List of bounding boxes for current detections.
      labels (list): List of labels corresponding to the boxes.
      confidences (list): List of confidence scores for each detection.
    
    Returns:
      list: A list of labels to display for the current detections, using stable labels when available.
    """
    new_tracked = {}  # Mapping: {box tuple: (stable_label, stable_confidence, frame_count)}
    displayed_labels = []  # Labels to display for the current frame

    # Update tracked cards with new detections
    for i, box in enumerate(boxes):
      label = labels[i]
      confidence = confidences[i]
      matched = False

      for prev_box in self.tracked_cards:
        if compute_overlap(box, list(prev_box)) >= self.overlap_threshold:
          prev_label, prev_conf, frame_count, locked_flag = self.tracked_cards[prev_box]

          if frame_count < self.confirmation_frames:
            frame_count += 1

            if frame_count >= self.confirmation_frames and not locked_flag and self.deck is not None:
              self.deck.remove_card(prev_label)
              locked_flag = True

          if frame_count >= self.confirmation_frames:
            label = prev_label

          matched = True
          new_tracked[tuple(box)] = (label, confidence, frame_count, locked_flag)

          break

      if not matched:
        new_tracked[tuple(box)] = (label, confidence, 1 if confidence >= self.confidence_threshold else 0, False)

    # Handle disappearing cards: keep them for a few extra frames before removing
    for prev_box in self.tracked_cards:
      if prev_box not in new_tracked:
        prev_label, prev_conf, frame_count, locked_flag = self.tracked_cards[prev_box]
        
        if frame_count < self.disappear_frames:
          new_tracked[prev_box] = (prev_label, prev_conf, frame_count + 1, locked_flag)
    
    self.tracked_cards = new_tracked

    # Build the list of labels to display based on tracking status
    for box in boxes:
      for tracked_box in self.tracked_cards:
        if compute_overlap(box, list(tracked_box)) >= self.overlap_threshold:
          stable_label, _, frame_count, _ = self.tracked_cards[tracked_box]

          if frame_count >= self.confirmation_frames:
            displayed_labels.append(stable_label)
          else:
            displayed_labels.append(labels[boxes.index(box)])

          break

      else:
        displayed_labels.append(labels[boxes.index(box)])

    return displayed_labels