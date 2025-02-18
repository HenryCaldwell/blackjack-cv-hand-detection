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

- Detection and Grouping Thresholds: e.g., overlap_threshold and inference_overlap_threshold.
- Tracking Settings: Such as the number of frames required to confirm or drop a detection.
- File Paths: For the YOLO model and the video input.
- Webcam Settings: Support for a configureable webcam index.
- Update Intervals: The time gap between successive frame analyses.
- Deck & Counting Parameters: e.g., deck_size for controlling the number of decks in play.
