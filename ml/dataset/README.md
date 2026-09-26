# Building the TrueLens AI Dataset

TrueLens AI trains a **3-class classifier** (REAL / AI_GENERATED / MANIPULATED)
by combining two established, legally-obtained open datasets. No dataset is
bundled with this repository — you must download each from its official
source and agree to its license.

## Required final folder structure

```
ml/dataset/
    train/
        REAL/            (.jpg/.png)
        AI_GENERATED/
        MANIPULATED/
    val/
        REAL/ AI_GENERATED/ MANIPULATED/
    test/
        REAL/ AI_GENERATED/ MANIPULATED/
```

Aim for a roughly 70/15/15 train/val/test split, done by **source video/image
group** (not by individual frame) to avoid near-duplicate frames leaking
across splits.

## 1. REAL class

**Source A — FaceForensics++ pristine (real) videos**
- Official repo & access request form: https://github.com/ondyari/FaceForensics
- License: research/academic use only; requires signing their EULA via the linked Google Form.
- Extract frames from the `original_sequences/youtube/c23/videos/` pristine videos
  (1 frame every ~15 frames avoids near-duplicates) into `REAL/`.

**Source B — CIFAKE real subset**
- Kaggle: https://www.kaggle.com/datasets/birdy654/cifake-real-and-ai-generated-synthetic-images
- License: as published on Kaggle (CC-style, free for research/education — check the page for current terms).
- Copy the `REAL` folder images directly into `REAL/`.

## 2. AI_GENERATED class

**Source — CIFAKE fake subset (Stable Diffusion generated)**
- Same Kaggle page as above; copy the `FAKE` folder into `AI_GENERATED/`.

**Optional, for a stronger/more modern dataset — GenImage**
- Official repo: https://github.com/GenImage-Dataset/GenImage
- License: research use, request access per their instructions.
- Contains images from multiple generators (Midjourney, SDv1.4/1.5, GLIDE, ADM, etc.)
  — using it alongside CIFAKE makes the AI_GENERATED class more diverse.

## 3. MANIPULATED class

**Source — FaceForensics++ manipulated subsets**
- Same access request as REAL Source A above.
- Use the four manipulation methods: `Deepfakes`, `Face2Face`, `FaceSwap`, `NeuralTextures`
  (folder: `manipulated_sequences/<method>/c23/videos/`).
- Extract frames the same way as the pristine videos, into `MANIPULATED/`.

## Frame extraction helper

Use `ml/dataset/extract_frames.py` (included) once you have downloaded the
FaceForensics++ videos to their official directory structure:

```bash
python ml/dataset/extract_frames.py --input_dir path/to/FaceForensics++/original_sequences/youtube/c23/videos --output_dir ml/dataset/train/REAL --every_n_frames 15
python ml/dataset/extract_frames.py --input_dir path/to/FaceForensics++/manipulated_sequences/Deepfakes/c23/videos --output_dir ml/dataset/train/MANIPULATED --every_n_frames 15
# repeat for Face2Face, FaceSwap, NeuralTextures into the same MANIPULATED/ folder
```

Then manually move ~15% of the images from each class into `val/` and `test/`
(split by original source video, not randomly by frame — a script for this,
`split_dataset.py`, is included).

## A note on class balance

`ml/training/train.py` already applies a `WeightedRandomSampler`, so you do
not need exactly equal image counts per class — but avoid extreme imbalance
(e.g. 50,000 REAL vs 500 MANIPULATED) since oversampling a tiny class too
aggressively causes overfitting to those few images. Aim for each class to
have at least a few thousand images if possible.
