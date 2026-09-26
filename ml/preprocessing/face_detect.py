"""
Face detection using OpenCV's DNN face detector (res10 SSD, Caffe, BSD license).

Deepfake manipulation (Face2Face, FaceSwap, NeuralTextures, etc.) alters faces
specifically, so cropping to the face before classification focuses the CNN
on the region where manipulation artifacts actually live. If no face is
found (e.g. the image isn't a portrait — could be a fully AI-generated scene),
we fall back to using the full image, since AI-generation artifacts are not
face-specific.

Model download (run once, not committed to git — see README):
  https://github.com/opencv/opencv/blob/master/samples/dnn/face_detector/deploy.prototxt
  https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
"""
import os

import cv2
import numpy as np

from ml.config import FACE_DETECTOR_PROTO, FACE_DETECTOR_MODEL, FACE_DETECTION_CONFIDENCE

_net = None


def _load_net():
    global _net
    if _net is None:
        if not (os.path.exists(FACE_DETECTOR_PROTO) and os.path.exists(FACE_DETECTOR_MODEL)):
            return None
        _net = cv2.dnn.readNetFromCaffe(FACE_DETECTOR_PROTO, FACE_DETECTOR_MODEL)
    return _net


def detect_and_crop_face(image_bgr: np.ndarray) -> np.ndarray:
    """
    Attempts to detect the most prominent face and crop to it with margin.
    Returns the original image unchanged if no face detector is available
    or no face is confidently detected.
    """
    net = _load_net()
    if net is None:
        return image_bgr

    h, w = image_bgr.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image_bgr, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()

    best_confidence = 0.0
    best_box = None
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > best_confidence and confidence > FACE_DETECTION_CONFIDENCE:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            best_box = box.astype("int")
            best_confidence = confidence

    if best_box is None:
        return image_bgr

    x1, y1, x2, y2 = best_box
    margin_x, margin_y = int((x2 - x1) * 0.3), int((y2 - y1) * 0.3)
    x1, y1 = max(0, x1 - margin_x), max(0, y1 - margin_y)
    x2, y2 = min(w, x2 + margin_x), min(h, y2 + margin_y)

    cropped = image_bgr[y1:y2, x1:x2]
    if cropped.size == 0:
        return image_bgr
    return cropped
