import os
import random
import shutil

SOURCE = "ml/dataset/deepfake/train_extracted/train/fake"
DEST = "ml/dataset"

random.seed(42)

images = [
    f for f in os.listdir(SOURCE)
    if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
]

random.shuffle(images)

total = len(images)
train_end = int(total * 0.70)
val_end = int(total * 0.85)

splits = {
    "train": images[:train_end],
    "val": images[train_end:val_end],
    "test": images[val_end:]
}

print(f"MANIPULATED: {total} images")

for split, split_images in splits.items():
    dest_dir = os.path.join(DEST, split, "MANIPULATED")
    os.makedirs(dest_dir, exist_ok=True)

    print(f"{split}: {len(split_images)} images")

    for i, filename in enumerate(split_images, 1):
        src = os.path.join(SOURCE, filename)
        dst = os.path.join(dest_dir, filename)
        shutil.copy2(src, dst)

        if i % 1000 == 0:
            print(f"  copied {i}/{len(split_images)}")

print("\n================================")
print("MANIPULATED DATASET READY")
print("================================")
