"""
Shared constants for the ml/ package — used by training, inference, and evaluation
so they never drift out of sync with each other.
"""

CLASS_NAMES = ["REAL", "AI_GENERATED", "MANIPULATED"]
NUM_CLASSES = len(CLASS_NAMES)

IMAGE_SIZE = 224          # standard input size for EfficientNet-B0 / Xception / ResNet-50 transfer learning
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

# OpenCV DNN face detector files (Caffe, BSD-licensed, from opencv/opencv_3rdparty)
FACE_DETECTOR_PROTO = "ml/preprocessing/face_detector/deploy.prototxt"
FACE_DETECTOR_MODEL = "ml/preprocessing/face_detector/res10_300x300_ssd_iter_140000.caffemodel"
FACE_DETECTION_CONFIDENCE = 0.6
