import os
import yaml

class DetectionSettings:
  def __init__(self, config_file="config.yaml"):
    if not os.path.isfile(config_file):
      raise FileNotFoundError("Configuration file not found: " + config_file)
    with open(config_file, "r") as f:
      config_data = yaml.safe_load(f)
    
    detection = config_data["detection_settings"]

    self.yolo_path = detection["yolo_path"]
    self.video_path = detection["video_path"]

    self.use_webcam = detection["use_webcam"]
    self.webcam_index = detection["webcam_index"]

    self.inference_interval = detection["inference_interval"]
    self.inference_frame_size = tuple(detection["inference_frame_size"])

    self.overlap_threshold = detection["overlap_threshold"]
    self.inference_overlap_threshold = detection["inference_overlap_threshold"]
    self.confidence_threshold = detection["confidence_threshold"]

    self.confirmation_frames = detection["confirmation_frames"]
    self.disappear_frames = detection["disappear_frames"]

    self.deck_size = detection["deck_size"]
    self.display_frame_size = tuple(detection["display_frame_size"])