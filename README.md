# Blackjack Computer Vision Analyzer

A python computer vision application that uses deep learning to detect playing cards in real time. The system processes video streams to locate cards, groups them into hands using spatial clustering, computes scores based on standard card values, and overlays detailed annotations directly on the video frames for immediate analysis.

---

## Overview

- Detection: A YOLO-based model identifies playing cards in each frame.
- Grouping: Detected cards are clustered into hands by analyzing spatial overlap.
- Scoring: Hand scores are calculated by summing card values (with special handling for aces).
- Annotation: Visual cues, including bounding boxes, card labels, hand numbers, and scores, are drawn on the frames.
- Evaluation (Java): A Java evaluation engine (compiled separately) computes expected values (EV) for various actions. Integrated into the Python application via JPype.

---

## Example Usage

During execution, the program will:

1. Load YOLO weights and initialize the detection model.
2. Start video capture from a designated video file or webcam.
3. Process each frame to detect, track, and group cards.
4. Compute scores, computer counts, and evaluate best play for each detected hand.
5. Annotate the frame with bounding boxes, card labels, hand numbers (player hands and dealer hand), and scores.
6. Display the annotated frame in real time.

Press q at any time to exit the application.

---

## Project Structure

```
blackjack-cv-hand-detection/
├── java/
│   └── evaluation/
│       ├── EVEngine.java  # Java evaluation engine for computing expected values (EV).
│       ├── GameRules.java  # Configurable game rules for evaluation.
│       └── StateKey.java  # Utility class for memoization state keys.
├── python/
│   ├── config/
│   │   └── config.py  # Central configuration for file paths, thresholds, and UI parameters.
│   ├── detection/
│   │   ├── annotator.py  # Annotates frames with detection boxes, labels, and scores.
│   │   ├── card_tracker.py  # Tracks card detections across frames to confirm labels.
│   │   ├── detection_utils.py  # Utility functions (e.g., computing overlap) used across detection modules.
│   │   ├── hand_detector.py  # Groups detected cards into hands; merges singletons into the dealer hand.
│   │   └── inference.py  # Runs YOLO inference and applies Non-Maximum Suppression.
│   └── blackjack/
│       ├── deck.py  # Manages the deck of cards and counting (Hi-Lo system).
│       └── blackjack_utils.py  # Helper functions for evaluating blackjack hands (e.g., scoring).
├── resources/
│   └── detection_weights.pt  # My custom trained YOLO model weights (you're welcome).
├── main.py  # Main entry point that integrates Python detection/annotation and Java evaluation via JPype.
└── README.md  # This file.

```

---

## Configuration

All detection settings are centralized in config.py. You can adjust:

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
