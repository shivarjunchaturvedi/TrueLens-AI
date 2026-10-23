"""
Hugging Face image-classification inference used by the active API route.

The configured Mirage Photo Classifier is treated as a binary real/fake model.
The API schema retains a manipulated field for compatibility, so this implementation
reports that field as 0 rather than pretending the model predicts a third class.
"""
import os
import time
from functools import lru_cache

import torch
from PIL import Image
from transformers import AutoImageProcessor, AutoModelForImageClassification

from app.config import settings

MODEL_ID = "prithivMLmods/Mirage-Photo-Classifier"


@lru_cache(maxsize=1)
def get_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    processor = AutoImageProcessor.from_pretrained(MODEL_ID)
    model = AutoModelForImageClassification.from_pretrained(MODEL_ID)
    model = model.to(device)
    model.eval()
    return processor, model


def _label_for(model, index: int) -> str:
    labels = getattr(model.config, "id2label", {}) or {}
    return str(labels.get(index, labels.get(str(index), f"class_{index}"))).strip().lower()


def run_prediction(image_path: str, heatmap_output_path: str | None = None) -> dict:
    start = time.perf_counter()
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    processor, model = get_model()
    device = next(model.parameters()).device

    with Image.open(image_path) as opened:
        image = opened.convert("RGB")

    inputs = processor(images=image, return_tensors="pt")
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.inference_mode():
        outputs = model(**inputs)
        probs = torch.softmax(outputs.logits, dim=-1)[0].detach().cpu().tolist()

    labels = [_label_for(model, i) for i in range(len(probs))]
    real_indices = [i for i, label in enumerate(labels) if "real" in label]
    fake_indices = [i for i, label in enumerate(labels) if any(term in label for term in ("fake", "synthetic", "generated", "artificial"))]

    # Refuse to silently return all-zero confidence if the upstream model label map changes.
    if not real_indices or not fake_indices:
        raise RuntimeError(
            "The configured model labels could not be mapped to Real/Fake classes. "
            f"Received labels: {labels!r}"
        )

    real = sum(float(probs[i]) for i in real_indices)
    fake = sum(float(probs[i]) for i in fake_indices)
    total = real + fake
    if total <= 0:
        raise RuntimeError("The model returned invalid class probabilities.")

    # Normalize across the mapped binary classes in case the upstream model includes
    # additional labels that are outside the current application's output schema.
    real /= total
    fake /= total
    prediction = "REAL" if real >= fake else "AI_GENERATED"
    confidence = max(real, fake) * 100

    return {
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "probabilities": {
            "real": round(real * 100, 2),
            "ai_generated": round(fake * 100, 2),
            "manipulated": 0.0,
        },
        "model_name": MODEL_ID,
        "model_version": settings.MODEL_VERSION,
        "processing_time_seconds": round(time.perf_counter() - start, 3),
        "heatmap_generated": False,
    }
