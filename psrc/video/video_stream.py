"""
Module for reading video streams using OpenCV.

This module defines the VideoStreamReader class, which encapsulates the functionality to open a video source
(e.g., webcam or video file), read frames from it, and release the resource when done.
"""

import cv2
import numpy as np
from typing import Union, Optional
from debugging.logger import setup_logger

logger = setup_logger(__name__)

class VideoStreamReader:
  """
  A class to manage video capture from a given source using OpenCV.

  The class provides methods to initialize the video source, read individual frames, and release the resource
  once video processing is complete.
  """

  def __init__(self, source: Union[int, str] = 0) -> None:
    """
    Initializes the VideoStreamReader instance.

    Sets up the video capture using OpenCV with the specified source. The source can be an integer (for webcam
    index) or a string (file path).

    Parameters:
      source (int or str): The video source index (e.g., 0 for default webcam) or file path.

    Raises:
      IOError: If the video source cannot be opened.
    """
    self.cap = cv2.VideoCapture(source)  # Create a VideoCapture object for the given source

    # Check if the video source has been opened successfully
    if not self.cap.isOpened():
      raise IOError(f"Unable to open video source: {source}")
    
    logger.info("Video source opened: %s", source)
    
  def read_frame(self) -> Optional[np.ndarray]:
    """
    Reads a single frame from the video capture source.

    Attempts to read a frame using the VideoCapture object. It logs a warning if the frame could not be captured.

    Returns:
      frame (numpy.ndarray or None): The captured frame if successful, otherwise None.
    """
    ret, frame = self.cap.read()

    # If reading the frame fails, log a warning and return None
    if not ret:
      logger.warning("Failed to read frame from video source")
      return None
    
    return frame
  
  def release(self) -> None:
    """
    Releases the video capture resource.

    Ensures that the video source is properly released, which is important for freeing system resources and
    avoiding potential conflicts with other applications.
    """
    if self.cap is not None:
      self.cap.release()
      logger.info("Video source released")
