"""
Dataset loader for the 3-class TrueLens dataset.

Expected folder structure (see README / docs for how to build this from
FaceForensics++ + CIFAKE / GenImage):

    ml/dataset/
        train/
            REAL/            *.jpg
            AI_GENERATED/    *.jpg
            MANIPULATED/     *.jpg
        val/
            REAL/ AI_GENERATED/ MANIPULATED/
        test/
            REAL/ AI_GENERATED/ MANIPULATED/

This is a standard torchvision.datasets.ImageFolder-compatible layout, but we
implement it explicitly (rather than just using ImageFolder) so class order
is guaranteed to match ml.config.CLASS_NAMES exactly.
"""
import os
from collections import Counter

from PIL import Image
from torch.utils.data import Dataset

from ml.config import CLASS_NAMES

IMG_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


class TrueLensDataset(Dataset):
    def __init__(self, root_dir: str, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.samples: list[tuple[str, int]] = []

        for class_idx, class_name in enumerate(CLASS_NAMES):
            class_dir = os.path.join(root_dir, class_name)
            if not os.path.isdir(class_dir):
                raise FileNotFoundError(
                    f"Expected class folder not found: {class_dir}\n"
                    f"Build the dataset first — see ml/dataset/README.md"
                )
            for fname in sorted(os.listdir(class_dir)):
                if fname.lower().endswith(IMG_EXTENSIONS):
                    self.samples.append((os.path.join(class_dir, fname), class_idx))

        if len(self.samples) == 0:
            raise RuntimeError(f"No images found under {root_dir}")

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        image = Image.open(path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label

    def class_counts(self) -> Counter:
        return Counter(label for _, label in self.samples)
