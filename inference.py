import numpy as np
from ultralytics import YOLO
from hand_detector import compute_overlap

# Global dictionary to track stable detections
tracked_cards = {}  # Format: {box: (stable_label, stable_confidence, frame_count)}
CONFIRMATION_FRAMES = 5  # Number of consecutive frames required to confirm a card label
DISAPPEAR_FRAMES = 5  # Number of frames a card can disappear before being forgotten

def run_inference(frame, model, overlap_threshold=0.9, confidence_threshold=0.9):
  """
  Runs YOLO inference and ensures stable card detection by confirming consistent labels over multiple frames.
  Bounding boxes appear immediately, but labels are locked in only after stability is confirmed.

  Parameters:
    frame (numpy.ndarray): The image frame to process.
    model (YOLO): A YOLO model instance configured for card detection.
    overlap_threshold (float, optional): Overlap threshold for persistence. Defaults to 0.9.
    confidence_threshold (float, optional): Minimum confidence to track detections persistently. Defaults to 0.9.

  Returns:
    tuple: (filtered_boxes, displayed_labels)
  """
  global tracked_cards

  results = model(frame, show=False)  # Perform inference
  last_results = results[0]  # Get the most recent results

  boxes, labels, confidences = [], [], []

  # Extract bounding boxes, labels, and confidence scores
  if last_results is not None and last_results.boxes is not None:
    boxes = last_results.boxes.xyxy.cpu().numpy().tolist()  # Get bounding boxes
    confidences = last_results.boxes.conf.cpu().numpy().tolist()  # Get confidence scores

    if hasattr(last_results.boxes, 'cls'):
      class_indices = last_results.boxes.cls.cpu().numpy().tolist()  # Get class indices

      # Mapping from class index to card labels
      card_map = {
        0: "A", 1: "2", 2: "3", 3: "4", 4: "5", 5: "6",
        6: "7", 7: "8", 8: "9", 9: "10", 10: "J", 11: "Q", 12: "K"
      }

      labels = [card_map.get(int(idx), "?") for idx in class_indices]

  # Apply Non-Max Suppression (NMS)
  filtered_boxes, filtered_labels, filtered_confidences = apply_nms(boxes, labels, confidences, overlap_threshold)

  # Apply stability tracking for labels
  displayed_labels = apply_stability_tracking(filtered_boxes, filtered_labels, filtered_confidences, confidence_threshold, overlap_threshold)

  return filtered_boxes, displayed_labels


def apply_nms(boxes, labels, confidences, overlap_threshold):
  """
  Applies Non-Maximum Suppression (NMS) to remove overlapping bounding boxes.

  Parameters:
    boxes (list): List of bounding boxes [x1, y1, x2, y2].
    labels (list): List of labels corresponding to each box.
    confidences (list): Confidence scores of the boxes.
    overlap_threshold (float): Overlap ratio threshold for suppression.

  Returns:
    tuple: (filtered_boxes, filtered_labels, filtered_confidences)
  """
  if not boxes:
    return [], [], []

  boxes = np.array(boxes)
  confidences = np.array(confidences)
  indices = sorted(range(len(confidences)), key=lambda i: confidences[i], reverse=True)

  keep = []
  while indices:
    i = indices.pop(0)
    keep.append(i)

    # Compare with remaining boxes
    indices = [
      j for j in indices if compute_overlap(boxes[i], boxes[j]) < overlap_threshold
    ]

  # Keep only the selected boxes
  filtered_boxes = [boxes[i].tolist() for i in keep]
  filtered_labels = [labels[i] for i in keep]
  filtered_confidences = [confidences[i] for i in keep]

  return filtered_boxes, filtered_labels, filtered_confidences


def apply_stability_tracking(boxes, labels, confidences, confidence_threshold, overlap_threshold):
  """
  Ensures that card labels are confirmed only after being stable for a certain number of frames.
  Bounding boxes update in real-time, but labels become stable only after CONFIRMATION_FRAMES.

  Parameters:
    boxes (list): List of detected bounding boxes.
    labels (list): List of labels.
    confidences (list): List of confidence scores.
    confidence_threshold (float): Minimum confidence to store stable values.
    overlap_threshold (float): Overlap ratio to consider a box the "same" over frames.

  Returns:
    list: Displayed labels (stable if confirmed, real-time otherwise)
  """
  global tracked_cards

  new_tracked_cards = {}
  displayed_labels = []

  for i, box in enumerate(boxes):
    label = labels[i]
    confidence = confidences[i]
    matched = False

    for prev_box in tracked_cards:
      prev_label, prev_confidence, frame_count = tracked_cards[prev_box]

      if compute_overlap(box, prev_box) >= overlap_threshold:
        # If stable for enough frames, use locked-in label
        if frame_count >= CONFIRMATION_FRAMES:
          label = prev_label  # Use the stored stable label
        else:
          frame_count += 1  # Increase counter until confirmation

        matched = True
        new_tracked_cards[tuple(box)] = (label, confidence, frame_count)
        break

    if not matched:
      # Start tracking this new detection
      new_tracked_cards[tuple(box)] = (label, confidence, 1 if confidence >= confidence_threshold else 0)

  # Handle disappearing cards (give them a few frames before removing)
  for prev_box in tracked_cards:
    prev_label, prev_confidence, frame_count = tracked_cards[prev_box]
    if prev_box not in new_tracked_cards:
      if frame_count >= DISAPPEAR_FRAMES:
        continue  # Forget the card completely
      else:
        # Reduce count but keep it in memory
        new_tracked_cards[prev_box] = (prev_label, prev_confidence, frame_count + 1)

  # Update global storage
  tracked_cards = new_tracked_cards

  # Generate displayed labels
  for i, box in enumerate(boxes):
    for tracked_box in tracked_cards:
      if compute_overlap(box, tracked_box) >= overlap_threshold:
        stable_label, _, frame_count = tracked_cards[tracked_box]
        if frame_count >= CONFIRMATION_FRAMES:
          displayed_labels.append(stable_label)  # Use stable label
        else:
          displayed_labels.append(labels[i])  # Show real-time detection label
        break
    else:
      displayed_labels.append(labels[i])  # If no match, show YOLO label

  return displayed_labels