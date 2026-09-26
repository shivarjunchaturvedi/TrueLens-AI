"""
Grad-CAM explainability using the `pytorch-grad-cam` library (MIT license).

Produces a heatmap over the input image showing which regions most influenced
the CNN's predicted class — used on the Detection Result page so users (and
the viva panel) can see *why* the model made its decision, not just the
number.
"""
import cv2
import numpy as np
import torch
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

from ml.model import get_target_layer_for_gradcam


def generate_gradcam_overlay(
    model: torch.nn.Module,
    backbone: str,
    input_tensor: torch.Tensor,
    original_image_rgb_float: np.ndarray,
    target_class: int,
    device: torch.device,
) -> np.ndarray:
    """
    Args:
        model: the trained CNN (eval mode).
        backbone: backbone name, used to pick the correct conv layer.
        input_tensor: preprocessed (normalized) input, shape (1, 3, H, W).
        original_image_rgb_float: original image resized to model input size,
            RGB, float32, values in [0, 1] — used as the background for the overlay.
        target_class: the predicted class index to explain.
        device: torch device.

    Returns:
        RGB uint8 image (H, W, 3) — the heatmap overlaid on the original image.
    """
    target_layer = get_target_layer_for_gradcam(model, backbone)
    cam = GradCAM(model=model, target_layers=[target_layer])

    from pytorch_grad_cam.utils.model_targets import ClassifierOutputTarget
    grayscale_cam = cam(input_tensor=input_tensor.to(device), targets=[ClassifierOutputTarget(target_class)])
    grayscale_cam = grayscale_cam[0, :]  # (H, W), values 0-1

    overlay = show_cam_on_image(original_image_rgb_float, grayscale_cam, use_rgb=True)
    return overlay


def save_gradcam_result(overlay_rgb: np.ndarray, output_path: str) -> None:
    """Saves the RGB overlay array to disk as a JPEG."""
    overlay_bgr = cv2.cvtColor(overlay_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite(output_path, overlay_bgr)
