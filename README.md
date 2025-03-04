# Blackjack Computer Vision Analyzer

The Blackjack Vision Analyzer is a computer vision and decision-support system designed for real-time blackjack analysis. It integrates a Python-based YOLO detection pipeline with a Java-based expected value (EV) engine to determine optimal blackjack actions (stand, hit, double, split) based on live card detection.

## Features

- Real-Time Card Detection: Utilizes a YOLO model to detect playing cards from video streams (webcam or video file).
- Blackjack Hand Evaluation: Calculates hand scores and uses a Java EV engine (accessed via JPype) to evaluate potential actions.
- Deck Management & Card Counting: Maintains the current deck composition and computes Hi-Lo running and true counts.
- Configurable: Centralized configurations for detection parameters, UI display, and game rules.
- Seamless Java-Python Integration: Leverages JPype to call Java methods from Python, combining the strengths of both ecosystems.

## Project Structure

```
root/
├── build/
│   └── EVEngine.jar  # Compiled Java JAR containing EV engine classes
├── jsrc/
│   └── evaluation/
│       ├── Config.java  # Java configuration or game rules class
│       ├── EVEngine.java       *CODE* (Java EV engine logic)
│       └── StateKey.java       *CODE* (Java class for memoization)
```
