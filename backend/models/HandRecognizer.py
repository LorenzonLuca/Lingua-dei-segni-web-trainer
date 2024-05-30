import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class HandRecognizer:
    def __init__(self, logger):
        self.logger = logger

        self.base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
        self.options = vision.HandLandmarkerOptions(base_options=self.base_options)
        self.detector = vision.HandLandmarker.create_from_options(self.options)

    def detect_hand(self, img):
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(img))
        detection_result = self.detector.detect(image)
        try:
            return detection_result
        except:
            return 'none'
