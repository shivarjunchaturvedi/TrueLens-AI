import os
import time

import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

from app.config import settings


MODEL_ID = "prithivMLmods/Mirage-Photo-Classifier"

_processor = None
_model = None


def get_model():
    global _processor, _model

    if _model is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"

        _processor = AutoImageProcessor.from_pretrained(MODEL_ID)
        _model = AutoModelForImageClassification.from_pretrained(MODEL_ID)
        _model = _model.to(device)
        _model.eval()

    return _processor, _model


def run_prediction(image_path: str, heatmap_output_path: str) -> dict:
    start = time.perf_counter()

    if not os.path.exists(image_path):
        raise FileNotFoundError(image_path)

    processor, model = get_model()
    device = next(model.parameters()).device

    image = Image.open(image_path).convert("RGB")

    inputs = processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=-1)[0]

    labels = model.config.id2label

    real = 0.0
    fake = 0.0

    for i, probability in enumerate(probabilities):
        label = labels[i].lower()
        score = float(probability)

        if "real" in label:
            real = score
        elif "fake" in label:
            fake = score

    prediction = "REAL" if real >= fake else "AI_GENERATED"
    confidence = max(real, fake) * 100

    return {
        "prediction": prediction,
        "confidence": confidence,
        "probabilities": {
            "real": real,
            "ai_generated": fake,
            "manipulated": 0.0,
        },
        "model_name": MODEL_ID,
        "model_version": "2.0-mirage",
        "processing_time_seconds": round(time.perf_counter() - start, 3),
        "heatmap_generated": False,
    }