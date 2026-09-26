"""
Splits images already sitting in ml/dataset/train/<CLASS>/ into val/ and test/
as well, grouping by *source video prefix* (the part of the filename before
"_frame") so frames from the same original video never end up split across
train/val/test — which would let the model "cheat" on near-duplicate frames.

Usage (run once per class, after extract_frames.py has filled train/<CLASS>/):
    python ml/dataset/split_dataset.py --class_name REAL --val_ratio 0.15 --test_ratio 0.15
"""
import argparse
import os
import random
import shutil
from collections import defaultdict


def group_by_source(files: list[str]) -> dict[str, list[str]]:
    groups = defaultdict(list)
    for f in files:
        source_key = f.split("_frame")[0] if "_frame" in f else f
        groups[source_key].append(f)
    return groups


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--class_name", required=True)
    parser.add_argument("--dataset_root", default="ml/dataset")
    parser.add_argument("--val_ratio", type=float, default=0.15)
    parser.add_argument("--test_ratio", type=float, default=0.15)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    train_dir = os.path.join(args.dataset_root, "train", args.class_name)
    val_dir = os.path.join(args.dataset_root, "val", args.class_name)
    test_dir = os.path.join(args.dataset_root, "test", args.class_name)
    os.makedirs(val_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    files = [f for f in os.listdir(train_dir) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    groups = group_by_source(files)
    group_keys = list(groups.keys())
    random.shuffle(group_keys)

    n_val_groups = int(len(group_keys) * args.val_ratio)
    n_test_groups = int(len(group_keys) * args.test_ratio)

    val_groups = set(group_keys[:n_val_groups])
    test_groups = set(group_keys[n_val_groups:n_val_groups + n_test_groups])

    moved_val, moved_test = 0, 0
    for key, group_files in groups.items():
        target_dir = val_dir if key in val_groups else (test_dir if key in test_groups else None)
        if target_dir is None:
            continue
        for f in group_files:
            shutil.move(os.path.join(train_dir, f), os.path.join(target_dir, f))
            moved_val += 1 if target_dir == val_dir else 0
            moved_test += 1 if target_dir == test_dir else 0

    print(f"Moved {moved_val} images to val/, {moved_test} images to test/ for class '{args.class_name}'")


if __name__ == "__main__":
    main()
