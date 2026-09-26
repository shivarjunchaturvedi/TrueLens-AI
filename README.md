## ⚠️ Honesty Note Before You Demo This

TrueLens AI uses a pretrained Hugging Face image-authenticity classification model
(`prithivMLmods/Mirage-Photo-Classifier`) for image-level Real/Fake prediction.

The model provides an authenticity estimate and should not be treated as absolute
proof of whether an image is real or AI-generated.

### Current Detection

- Real image → `REAL`
- Fake/AI-generated image → `AI_GENERATED`
- Confidence score and probability distribution are displayed in the UI.
- The model is loaded automatically through Hugging Face Transformers.
- GPU inference is used when CUDA is available.

### Important Limitation

The current Mirage model is a binary Real/Fake classifier. It does **not**
reliably distinguish AI-generated images from traditional deepfakes/manipulated
images as separate classes.

Therefore, TrueLens AI should be presented as an **AI-based image authenticity
estimation system**, not as definitive forensic proof.
