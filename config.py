"""
Module for configuration management.

This module provides a Config class that centralizes all configurable parameters used throughout the card
detection application. Parameters include thresholds for grouping, detection, and tracking, as well as file paths
and update intervals.
"""

class Config:
  def __init__(self):
    """
    Initializes a new configuration instance with default parameter values.
    
    Attributes:
      overlap_threshold (float): Threshold for grouping cards into hands.
      inference_overlap_threshold (float): Overlap threshold for non-max suppression and tracking.
      confidence_threshold (float): Minimum confidence required to consider a detection.

      confirmation_frames (int): Number of consecutive frames required to confirm a card label.
      disappear_frames (int): Number of frames a card can be missing before it is dropped.

      yolo_path (str): File path to the YOLO weights.
      video_path (str): File path to the input video.
      inference_interval (float): Seconds between inference updates.
    """
    # Webcam, video, and model parameters
    self.use_webcam = True # Use webcam stream vs video file
    self.webcam_index = 0 # Index of the webcam to use (0 for default)
    self.video_path = "C:/Users/User/Pictures/Camera Roll/WIN_20250217_01_42_20_Pro.mp4"  # Path to the video file
    self.inference_interval = 0.25  # Seconds between inference updates
    self.yolo_path = "resources/detection_weights.pt"  # Path to the YOLO weights file

    # Grouping & detection thresholds
    self.overlap_threshold = 0.1  # For grouping cards into hands
    self.inference_overlap_threshold = 0.9  # For non-max suppression and tracking
    self.confidence_threshold = 0.9  # Minimum confidence to consider a detection

    # Stability tracking parameters
    self.confirmation_frames = 5  # Number of frames to confirm a card label
    self.disappear_frames = 10  # Number of frames a card can be missing before it is dropped