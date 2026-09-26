"""
Train the TrueLens AI CNN.

Run from the project root:
    python -m ml.training.train --backbone efficientnet_b0 --epochs 20 --batch-size 32

Requires the dataset to already exist under ml/dataset/{train,val,test}/<CLASS>/
(see ml/training/dataset.py and docs/dataset_setup.md for how to build it).

Automatically uses CUDA if available, CPU otherwise — never hard-coded.
"""
import argparse
import json
import os
import time

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, WeightedRandomSampler

from ml.config import CLASS_NAMES
from ml.model import build_model
from ml.preprocessing.transforms import get_train_transform, get_val_transform
from ml.training.dataset import TrueLensDataset


def build_weighted_sampler(dataset: TrueLensDataset) -> WeightedRandomSampler:
    """Class balancing: oversamples minority classes so the loss isn't dominated
    by whichever class happens to have the most images."""
    counts = dataset.class_counts()
    class_weights = {cls: 1.0 / count for cls, count in counts.items()}
    sample_weights = [class_weights[label] for _, label in dataset.samples]
    return WeightedRandomSampler(sample_weights, num_samples=len(sample_weights), replacement=True)


def run_epoch(model, loader, criterion, optimizer, device, train: bool):
    model.train() if train else model.eval()
    total_loss, correct, total = 0.0, 0, 0

    torch.set_grad_enabled(train)
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)

        if train:
            optimizer.zero_grad()

        outputs = model(images)
        loss = criterion(outputs, labels)

        if train:
            loss.backward()
            optimizer.step()

        total_loss += loss.item() * images.size(0)
        preds = outputs.argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    return total_loss / total, correct / total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backbone", default="efficientnet_b0",
                         choices=["efficientnet_b0", "xception", "resnet50", "convnext_tiny"])
    parser.add_argument("--data-dir", default="ml/dataset")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-4)
    parser.add_argument("--patience", type=int, default=5, help="Early stopping patience (epochs)")
    parser.add_argument("--output-dir", default="model")
    parser.add_argument("--num-workers", type=int, default=2)
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    os.makedirs(args.output_dir, exist_ok=True)

    train_ds = TrueLensDataset(os.path.join(args.data_dir, "train"), transform=get_train_transform())
    val_ds = TrueLensDataset(os.path.join(args.data_dir, "val"), transform=get_val_transform())

    print(f"Train class distribution: { {CLASS_NAMES[k]: v for k, v in train_ds.class_counts().items()} }")

    sampler = build_weighted_sampler(train_ds)
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, sampler=sampler, num_workers=args.num_workers)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, shuffle=False, num_workers=args.num_workers)

    model = build_model(backbone=args.backbone, pretrained=True).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2)

    best_val_loss = float("inf")
    epochs_without_improvement = 0
    history = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}

    checkpoint_path = os.path.join(args.output_dir, "best_model.pt")

    for epoch in range(1, args.epochs + 1):
        t0 = time.time()
        train_loss, train_acc = run_epoch(model, train_loader, criterion, optimizer, device, train=True)
        val_loss, val_acc = run_epoch(model, val_loader, criterion, optimizer, device, train=False)
        scheduler.step(val_loss)

        history["train_loss"].append(train_loss)
        history["val_loss"].append(val_loss)
        history["train_acc"].append(train_acc)
        history["val_acc"].append(val_acc)

        print(f"Epoch {epoch}/{args.epochs} ({time.time()-t0:.1f}s) | "
              f"train_loss={train_loss:.4f} train_acc={train_acc:.4f} | "
              f"val_loss={val_loss:.4f} val_acc={val_acc:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_without_improvement = 0
            torch.save(model.state_dict(), checkpoint_path)
            print(f"  -> New best model saved to {checkpoint_path}")
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= args.patience:
                print(f"Early stopping: no improvement for {args.patience} epochs.")
                break

    with open(os.path.join(args.output_dir, "training_history.json"), "w") as f:
        json.dump(history, f, indent=2)

    model_card = {
        "backbone": args.backbone,
        "classes": CLASS_NAMES,
        "best_val_loss": best_val_loss,
        "epochs_trained": len(history["train_loss"]),
        "final_train_acc": history["train_acc"][-1],
        "final_val_acc": history["val_acc"][-1],
    }
    with open(os.path.join(args.output_dir, "model_card.json"), "w") as f:
        json.dump(model_card, f, indent=2)

    print("Training complete. Run ml/evaluation/evaluate.py on the test set for final metrics.")


if __name__ == "__main__":
    main()
