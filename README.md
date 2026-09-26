# TrueLens AI — AI-Powered Image/Media Authenticity Detection System

TrueLens AI is a full-stack, CNN-based system that classifies an uploaded
image as **REAL**, **AI-GENERATED**, or **MANIPULATED/DEEPFAKE**, with a
confidence score and a Grad-CAM visual explanation of the decision.

Built as a B.Tech final-year project (Python/PyTorch + FastAPI + React).

## ⚠️ Honesty note before you demo this

This repository ships **working code**, not a working *trained model* — no
pretrained deepfake-detection weights are bundled (none can legally be
redistributed without proper licensing, and downloading one that "just
works" would misrepresent what the project does). Out of the box:

- The backend runs fully — auth, database, dashboard, history — using a
  CNN backbone with **ImageNet weights but an untrained classification
  head**, so predictions will not be meaningful until you train it.
- `is_trained_model` in the internal prediction result is `False` until
  you point `MODEL_CHECKPOINT_PATH` at a checkpoint produced by
  `ml/training/train.py`.
- Follow **Model Training** below with a real dataset before reporting any
  accuracy numbers in your project report or viva.

## Features

- JWT authentication (register/login/logout), bcrypt password hashing
- Image upload with validation (type, size, integrity, safe filenames)
- 3-class CNN inference (EfficientNet-B0 by default; Xception/ResNet-50/
  ConvNeXt-Tiny swappable via config)
- Grad-CAM explainability (original / heatmap / overlay)
- Scan history (view, inspect, delete)
- Dashboard with aggregate stats and charts
- SQLite by default, one-line swap to PostgreSQL

## Architecture

```
React (Vite) ──HTTP/JWT──▶ FastAPI ──▶ SQLAlchemy ──▶ SQLite/Postgres
                              │
                              ▼
                     ml/ package (in-process)
                     preprocessing → CNN → Grad-CAM
```

## Technology Stack

| Layer | Tech |
|---|---|
| ML | PyTorch, timm, OpenCV, pytorch-grad-cam |
| Backend | FastAPI, SQLAlchemy, python-jose, passlib |
| Frontend | React (Vite), Recharts, Axios, React Router |
| Database | SQLite (dev) / PostgreSQL (production-ready) |

## Requirements

- Python 3.10–3.12
- Node.js 18+
- ~4 GB free disk space (PyTorch + dependencies)
- GPU optional (CUDA auto-detected; CPU fallback always works)

## Installation (Windows)

See `docs/setup_windows.md` for exact copy-paste commands, including
troubleshooting. Quick summary:

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

## Dataset Setup

See `ml/dataset/README.md` for official dataset sources (FaceForensics++,
CIFAKE, GenImage), licenses, download instructions, and folder structure.

## Model Training

```powershell
python -m ml.training.train --backbone efficientnet_b0 --epochs 20 --batch-size 32
python -m ml.evaluation.evaluate --checkpoint model/best_model.pt --backbone efficientnet_b0
```

Outputs: `model/best_model.pt`, `model/training_history.json`,
`model/model_card.json`, `model/confusion_matrix.png`, `model/roc_curves.png`.

## Running the Project

Backend:
```powershell
cd backend
uvicorn app.main:app --reload --port 8000
```

Frontend (separate terminal):
```powershell
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`. API docs auto-generated at `http://localhost:8000/docs`.

## Environment Variables (.env)

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | SQLAlchemy connection string |
| `JWT_SECRET_KEY` | Secret for signing JWTs — change from the default |
| `JWT_EXPIRE_MINUTES` | Token lifetime |
| `MODEL_CHECKPOINT_PATH` | Path to trained model weights |
| `MODEL_BACKBONE` | efficientnet_b0 / xception / resnet50 / convnext_tiny |
| `UPLOAD_DIR` / `HEATMAP_DIR` | Storage folders |
| `MAX_UPLOAD_SIZE_MB` | Upload size limit |
| `CORS_ORIGINS` | Comma-separated allowed frontend origins |

## API Reference

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/auth/register` | No | Create account |
| POST | `/auth/login` | No | Get JWT |
| POST | `/predict` | Yes | Upload image, get prediction |
| GET | `/history` | Yes | List scan history |
| GET | `/history/{id}` | Yes | Get one scan |
| DELETE | `/history/{id}` | Yes | Delete a scan |
| GET | `/dashboard/stats` | Yes | Aggregate statistics |
| GET | `/health` | No | Health check |

Full request/response schemas: `http://localhost:8000/docs` (auto-generated
by FastAPI).

## Testing

```powershell
pytest tests/ -v
```

## Model Evaluation

Run `ml/evaluation/evaluate.py` after training — see **Model Training**
above. It reports accuracy, precision, recall, F1, ROC-AUC, and generates a
confusion matrix and ROC curve plots. See `docs/project_report.md` for how
to interpret each metric.

## Limitations

TrueLens AI provides an AI-based authenticity **estimate**, not absolute
proof of image origin. It is affected by dataset bias, unseen/newer
generative models, compression, resizing, adversarial manipulation, and
domain shift. False positives and false negatives are possible.

## Future Scope

- Video-level deepfake detection (temporal consistency)
- Ensemble of multiple backbones
- Active-learning pipeline to incorporate newly discovered generators
- Reverse-investigation module (evidence-based, not speculative, source
  attribution)

## License

This project's own code is provided for academic use. Datasets and
third-party models referenced here carry their own licenses — see
`ml/dataset/README.md`.
