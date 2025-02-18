# Blackjack Computer Vision Analyzer

This project is a Python computer vision application that uses deep learning to detect playing cards in real time. The system processes video streams to locate cards, groups them into hands using spatial clustering, computes scores based on standard card values, and overlays detailed annotations directly on the video frames for immediate analysis.

---

## Overview

The application integrates several key modules to transform raw video data into an annotated output:

- Detection: A YOLO-based model identifies playing cards in each frame.
- Grouping: Detected cards are clustered into hands by analyzing spatial overlap.
- Scoring: Hand scores are calculated by summing card values (with special handling for Aces).
- Annotation: Visual cues, including bounding boxes, card labels, hand numbers, and scores, are drawn on the frames.

---

## Example Usage

During execution, the program will:

1. Load the YOLO model from the specified weights.
2. Open the designated video file or camera feed.
3. Process each frame to detect, track, and group cards.
4. Compute scores for each detected hand.
5. Display the annotated frame with real-time detection and scoring information.

Press q at any time to exit the application.

---

## Project Structure

```
blackjack-cv-hand-detector/
├── annotator.py # Annotates frames with detection boxes and hand scores.
├── card_tracker.py # Tracks card detections across frames for stable label display.
├── config.py # Central configuration for thresholds, file paths, and update intervals.
├── deck.py # Manages the deck of cards, including counting via the Hi-Lo system.
├── hand_detector.py # Groups detected cards into hands using spatial analysis.
├── inference.py # Runs YOLO inference and applies Non-Maximum Suppression.
├── main.py # Main entry point that integrates all components and runs the application.
├── scorer.py # Calculates scores for hands based on standard card values.
└── utils.py # Utility functions (e.g., computing overlap) used across modules.
```

---

## Configuration

All settings are centralized in config.py. You can adjust:

- File Paths:
  - yolo_path: Path to the YOLO weights.
  - video_path: Path to the video input.
- Webcam Settings:
  - use_webcam: Set to True to use a webcam stream.
  - webcam_index: Index of the webcam to use.
- Inference Parameters:
  - inference_interval: Seconds between inference updates.
  - inference_frame_size: Resolution for the frame used during inference.
- Detection and Grouping Thresholds:
  - overlap_threshold: Threshold for grouping cards into hands.
  - inference_overlap_threshold: Overlap threshold for non-maximum supression and tracking.
  - confidence_threshold: Minimum confidence required to consider a detection.
- Tracking Settings:
  - confirmation_frames: Number of consecutive frames required to confirm a card label.
  - disappear_frames: Number of frames a card can be missing before it is dropped.
- Deck & Counting Parameters:
  - deck_size: Number of decks in play.
- UI Parameters:
  - display_frame_size: Resolution for the frame used during user display.
