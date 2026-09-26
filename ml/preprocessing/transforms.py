"""
Preprocessing pipeline shared between training and inference so the model
always sees images prepared exactly the same way.
"""
from torchvision import transforms

from ml.config import IMAGE_SIZE, IMAGENET_MEAN, IMAGENET_STD


def get_inference_transform():
    """Deterministic preprocessing used at prediction time (no augmentation)."""
    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def get_train_transform():
    """Training-time preprocessing with data augmentation for generalization."""
    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.RandomApply([transforms.GaussianBlur(kernel_size=3)], p=0.15),
        transforms.ToTensor(),
        transforms.Normalize(mean=IMAGENET_MEAN, std=IMAGENET_STD),
    ])


def get_val_transform():
    """Validation/test preprocessing — same as inference, no augmentation."""
    return get_inference_transform()
