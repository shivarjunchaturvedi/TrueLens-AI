"""
TrueLensPredictor: loads a trained checkpoint (or falls back to an
ImageNet-pretrained backbone with a randomly-initialized head if no
checkpoint exists yet) and runs the full inference pipeline for one image.

IMPORTANT HONESTY NOTE (read before demoing):
If MODEL_CHECKPOINT_PATH does not exist, this class still runs — it uses the
ImageNet-pretrained backbone with an UNTRAINED classification head, purely so
the rest of the application (API, frontend, dashboard, history) is testable
before Phase-3 training completes. In that fallback mode, `is_trained` is
False and the API will not claim otherwise. Do NOT report the fallback mode's
"confidence" numbers as real model results — train the model first (see
ml/training/train.py) and point MODEL_CHECKPOINT_PATH at the resulting
model/best_model.pt.
"""
import os
import time

import cv2
import numpy as np
import torch
import torch.nn.functional as F

from ml.config import CLASS_NAMES, IMAGE_SIZE
from ml.model import build_model
from ml.preprocessing.transforms import get_inference_transform
from ml.preprocessing.face_detect import detect_and_crop_face
from ml.explainability.gradcam import generate_gradcam_overlay, save_gradcam_result

from PIL import Image


class TrueLensPredictor:
    def __init__(self, checkpoint_path: str, backbone: str = "efficientnet_b0", model_version: str = "1.0"):
        self.backbone = backbone
        self.model_version = model_version
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = get_inference_transform()
        self.is_trained = os.path.exists(checkpoint_path)

        self.model = build_model(backbone=backbone, pretrained=True)

        if self.is_trained:
            state_dict = torch.load(checkpoint_path, map_location=self.device)
            self.model.load_state_dict(state_dict)

        self.model.to(self.device)
        self.model.eval()

    def predict(self, image_path: str, heatmap_output_path: str | None = None) -> dict:
        start_time = time.time()

        image_bgr = cv2.imread(image_path)
        if image_bgr is None:
            raise ValueError(f"Could not read image at {image_path}")

        # Try face-crop (helps deepfake-path artifacts); falls back to full image
        # automatically if no face detector model files or no face is found.
        cropped_bgr = detect_and_crop_face(image_bgr)
        cropped_rgb = cv2.cvtColor(cropped_bgr, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cropped_rgb)

        input_tensor = self.transform(pil_image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(input_tensor)
            probabilities = F.softmax(logits, dim=1).squeeze(0).cpu().numpy()

        predicted_idx = int(np.argmax(probabilities))
        predicted_class = CLASS_NAMES[predicted_idx]
        confidence = float(probabilities[predicted_idx] * 100)

        heatmap_generated = False
        if heatmap_output_path:
            try:
                resized_for_display = cv2.resize(cropped_rgb, (IMAGE_SIZE, IMAGE_SIZE)).astype(np.float32) / 255.0
                overlay = generate_gradcam_overlay(
                    model=self.model,
                    backbone=self.backbone,
                    input_tensor=input_tensor,
                    original_image_rgb_float=resized_for_display,
                    target_class=predicted_idx,
                    device=self.device,
                )
                save_gradcam_result(overlay, heatmap_output_path)
                heatmap_generated = True
            except Exception as e:
                # Grad-CAM failing should never break a prediction response.
                print(f"[TrueLensPredictor] Grad-CAM generation failed: {e}")

        processing_time = time.time() - start_time

        return {
            "prediction": predicted_class,
            "confidence": round(confidence, 2),
            "probabilities": {
                "real": round(float(probabilities[0] * 100), 2),
                "ai_generated": round(float(probabilities[1] * 100), 2),
                "manipulated": round(float(probabilities[2] * 100), 2),
            },
            "model_name": self.backbone,
            "model_version": self.model_version,
            "processing_time_seconds": round(processing_time, 3),
            "heatmap_generated": heatmap_generated,
            "is_trained_model": self.is_trained,
        }
