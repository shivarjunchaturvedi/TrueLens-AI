"""
Evaluate a trained checkpoint on the held-out test set.

Run from project root:
    python -m ml.evaluation.evaluate --checkpoint model/best_model.pt --backbone efficientnet_b0

Produces:
    model/confusion_matrix.png
    model/roc_curves.png
    model/training_curves.png   (if model/training_history.json exists)
    model/evaluation_report.json
"""
import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.metrics import (
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)
from sklearn.preprocessing import label_binarize
from torch.utils.data import DataLoader

from ml.config import CLASS_NAMES
from ml.model import build_model
from ml.preprocessing.transforms import get_val_transform
from ml.training.dataset import TrueLensDataset


def plot_confusion_matrix(cm, output_path):
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(CLASS_NAMES)))
    ax.set_yticks(range(len(CLASS_NAMES)))
    ax.set_xticklabels(CLASS_NAMES, rotation=45, ha="right")
    ax.set_yticklabels(CLASS_NAMES)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix — TrueLens AI")
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                     color="white" if cm[i, j] > cm.max() / 2 else "black")
    fig.colorbar(im)
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_roc_curves(y_true_bin, y_prob, output_path):
    fig, ax = plt.subplots(figsize=(6, 5))
    for i, cls in enumerate(CLASS_NAMES):
        fpr, tpr, _ = roc_curve(y_true_bin[:, i], y_prob[:, i])
        auc = roc_auc_score(y_true_bin[:, i], y_prob[:, i])
        ax.plot(fpr, tpr, label=f"{cls} (AUC={auc:.3f})")
    ax.plot([0, 1], [0, 1], "k--", linewidth=0.8)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC Curves — One-vs-Rest")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def plot_training_curves(history_path, output_path):
    if not os.path.exists(history_path):
        return
    with open(history_path) as f:
        history = json.load(f)

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(history["train_loss"], label="Train Loss")
    axes[0].plot(history["val_loss"], label="Val Loss")
    axes[0].set_title("Loss")
    axes[0].set_xlabel("Epoch")
    axes[0].legend()

    axes[1].plot(history["train_acc"], label="Train Acc")
    axes[1].plot(history["val_acc"], label="Val Acc")
    axes[1].set_title("Accuracy")
    axes[1].set_xlabel("Epoch")
    axes[1].legend()

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default="model/best_model.pt")
    parser.add_argument("--backbone", default="efficientnet_b0")
    parser.add_argument("--data-dir", default="ml/dataset")
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--output-dir", default="model")
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    test_ds = TrueLensDataset(os.path.join(args.data_dir, "test"), transform=get_val_transform())
    test_loader = DataLoader(test_ds, batch_size=args.batch_size, shuffle=False)

    model = build_model(backbone=args.backbone, pretrained=False)
    model.load_state_dict(torch.load(args.checkpoint, map_location=device))
    model.to(device).eval()

    all_labels, all_preds, all_probs = [], [], []
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            probs = torch.softmax(outputs, dim=1).cpu().numpy()
            preds = probs.argmax(axis=1)

            all_labels.extend(labels.numpy())
            all_preds.extend(preds)
            all_probs.extend(probs)

    all_labels = np.array(all_labels)
    all_preds = np.array(all_preds)
    all_probs = np.array(all_probs)

    report = classification_report(all_labels, all_preds, target_names=CLASS_NAMES, output_dict=True)
    cm = confusion_matrix(all_labels, all_preds)

    y_true_bin = label_binarize(all_labels, classes=list(range(len(CLASS_NAMES))))
    try:
        roc_auc_macro = roc_auc_score(y_true_bin, all_probs, average="macro", multi_class="ovr")
    except ValueError:
        roc_auc_macro = None

    os.makedirs(args.output_dir, exist_ok=True)
    plot_confusion_matrix(cm, os.path.join(args.output_dir, "confusion_matrix.png"))
    plot_roc_curves(y_true_bin, all_probs, os.path.join(args.output_dir, "roc_curves.png"))
    plot_training_curves(
        os.path.join(args.output_dir, "training_history.json"),
        os.path.join(args.output_dir, "training_curves.png"),
    )

    result = {
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
        "roc_auc_macro": roc_auc_macro,
    }
    with open(os.path.join(args.output_dir, "evaluation_report.json"), "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(report, indent=2))
    print(f"Macro ROC-AUC: {roc_auc_macro}")
    print(f"Saved plots and evaluation_report.json to {args.output_dir}/")


if __name__ == "__main__":
    main()
