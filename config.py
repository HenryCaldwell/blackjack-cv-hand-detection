"""
Module for configuration management.

This module provides a Config class that centralizes all configurable parameters used throughout the card
detection application. Parameters include thresholds for grouping, detection, and tracking, as well as file paths,
update intervals, and frame sizes.
"""

class Config:
  def __init__(self):
    """
    Initializes a new configuration instance with default parameter values.
    
    Attributes:
      yolo_path (str): File path to the YOLO weights.

      use_webcam (bool): Flag to use webcam stream vs video file.
      webcam_index (int): Index of the webcam to use (0 for default).
      video_path (str): File path to the input video.
      inference_interval (float): Seconds between inference updates.
      inference_frame_size (tuple): Resolution (width, height) for the frame used during inference.

      overlap_threshold (float): Threshold for grouping cards into hands.
      inference_overlap_threshold (float): Overlap threshold for non-max suppression and tracking.
      confidence_threshold (float): Minimum confidence required to consider a detection.

      confirmation_frames (int): Number of consecutive frames required to confirm a card label.
      disappear_frames (int): Number of frames a card can be missing before it is dropped.

      deck_size (int): Number of decks in play.

      display_frame_size (tuple): Resolution (width, height) for the frame used during user display.
    """
    # File paths
    self.yolo_path = "resources/detection_weights.pt"  # Path to the YOLO weights file
    self.video_path = "example/video/path.mp4"  # Path to the video file

    # Webcam parameters
    self.use_webcam = True # Use webcam stream vs video file
    self.webcam_index = 0 # Index of the webcam to use (0 for default)

    # Inference parameters
    self.inference_interval = 0.25  # Seconds between inference updates
    self.inference_frame_size = (1920, 1080)  # Resolution for the frame used during inference

    # Detection & grouping thresholds
    self.overlap_threshold = 0.1  # For grouping cards into hands
    self.inference_overlap_threshold = 0.9  # For non-max suppression and tracking
    self.confidence_threshold = 0.9  # Minimum confidence to consider a detection

    # Stability tracking parameters
    self.confirmation_frames = 5  # Number of frames to confirm a card label
    self.disappear_frames = 10  # Number of frames a card can be missing before it is dropped

    # Deck & counting parameters
    self.deck_size = 1  # Number of decks in play

    # UI parameters
    self.display_frame_size = (1280, 720) # Resolution for the frame used during display