# Windows Setup Guide

## 1. Python virtual environment

```powershell
cd TrueLens-AI
python -m venv venv
venv\Scripts\activate
```

## 2. Install backend/ML dependencies

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

If PyTorch fails to install via the normal command (rare on Windows without
a matching CUDA setup), install the CPU build explicitly:

```powershell
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## 3. Environment variables

```powershell
copy .env.example .env
```
Edit `.env` and set a real `JWT_SECRET_KEY` (any long random string).

## 4. Database setup

No manual step needed — tables are created automatically on first backend
startup (SQLite file `truelens.db` appears in the project root).

## 5. Face detector model files (for deepfake-path face cropping)

```powershell
mkdir ml\preprocessing\face_detector
curl -o ml\preprocessing\face_detector\deploy.prototxt https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
curl -o ml\preprocessing\face_detector\res10_300x300_ssd_iter_140000.caffemodel https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
```
(If these files are absent, the pipeline still runs — it just skips the
face-crop step and uses the full image, as documented in
`ml/preprocessing/face_detect.py`.)

## 6. Backend startup

```powershell
cd backend
uvicorn app.main:app --reload --port 8000
```
Visit `http://localhost:8000/docs` to confirm it's running.

## 7. Frontend startup (new terminal)

```powershell
cd frontend
npm install
npm run dev
```
Visit `http://localhost:5173`.

## 8. Dataset setup

See `ml/dataset/README.md`.

## 9. Training command

```powershell
python -m ml.training.train --backbone efficientnet_b0 --epochs 20 --batch-size 32
```

## 10. Evaluation command

```powershell
python -m ml.evaluation.evaluate --checkpoint model/best_model.pt --backbone efficientnet_b0
```

## 11. Inference test (no server needed)

```powershell
python -c "from ml.inference.predictor import TrueLensPredictor; p = TrueLensPredictor('model/best_model.pt'); print(p.predict('path\\to\\test.jpg', 'test_heatmap.jpg'))"
```

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'app'` | Run uvicorn from inside `backend/`, not the project root |
| `email-validator is not installed` | `pip install email-validator` (already in requirements.txt) |
| bcrypt `__about__` AttributeError | `pip install "bcrypt==4.0.1"` (version pin, passlib compatibility issue) |
| `no such table: users` | Make sure the backend actually started (tables are created on FastAPI startup) — check the console for errors |
| CORS errors in browser console | Check `CORS_ORIGINS` in `.env` matches your frontend URL exactly (including port) |
| Torch install fails / very slow | Use the CPU-only index URL shown in step 2 |
| Grad-CAM heatmap missing on result page | Check backend console — Grad-CAM failures are logged but don't block the prediction response |
