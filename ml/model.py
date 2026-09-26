"""
CNN model factory.

Uses `timm` to load an ImageNet-pretrained backbone and replaces its
classification head with a 3-class head (REAL / AI_GENERATED / MANIPULATED).

Swapping architectures is a one-line change (the `backbone` argument), so the
same training/inference code works for EfficientNet-B0, Xception, ResNet-50,
or ConvNeXt-Tiny — this lets the project report include a backbone comparison
table without touching any other code.
"""
import timm
import torch.nn as nn

from ml.config import NUM_CLASSES

SUPPORTED_BACKBONES = ["efficientnet_b0", "xception", "resnet50", "convnext_tiny"]


def build_model(backbone: str = "efficientnet_b0", pretrained: bool = True) -> nn.Module:
    if backbone not in SUPPORTED_BACKBONES:
        raise ValueError(f"Unsupported backbone '{backbone}'. Choose from {SUPPORTED_BACKBONES}")

    model = timm.create_model(backbone, pretrained=pretrained, num_classes=NUM_CLASSES)
    return model


def get_target_layer_for_gradcam(model: nn.Module, backbone: str):
    """
    Returns the last convolutional layer of the given backbone — the layer
    Grad-CAM needs hooks on to compute class activation maps.
    """
    if backbone == "efficientnet_b0":
        return model.conv_head
    if backbone == "xception":
        return model.conv4
    if backbone == "resnet50":
        return model.layer4[-1]
    if backbone == "convnext_tiny":
        return model.stages[-1].blocks[-1]
    raise ValueError(f"No known Grad-CAM target layer for backbone '{backbone}'")
