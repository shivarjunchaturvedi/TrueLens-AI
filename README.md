#TrueLens AI

> AI-powered image authenticity detection system.

TrueLens AI is a full-stack web application that analyzes images and provides an AI-based estimate of whether an image appears to be **Real or AI-generated/Fake**.

## ✨ Features

- 🖼️ Image authenticity detection
- 🤖 AI-powered Real/Fake classification
- 📊 Confidence score and probability distribution
- 👤 User registration and login
- 🔐 JWT authentication
- 📜 Detection history
- 📈 Dashboard
- ⚡ GPU acceleration with CUDA
- 🌐 Responsive React frontend
- 🚀 FastAPI backend
- 🗄️ SQLite database
- 🤗 Hugging Face model integration

## 🤖 AI Model

Current model:

```text
prithivMLmods/Mirage-Photo-Classifier

The model performs binary classification:

Real
Fake

TrueLens AI maps these results to:

REAL
AI_GENERATED

The model is loaded using PyTorch and Hugging Face Transformers.

🛠️ Tech Stack
Frontend
React
Vite
JavaScript
Axios
React Router
Backend
Python
FastAPI
Uvicorn
SQLAlchemy
Pydantic
JWT Authentication
Machine Learning
PyTorch
Hugging Face Transformers
Hugging Face Hub
SigLIP2
Pillow
Database
SQLite
📁 Project Structure
TrueLens-AI/
├── backend/
├── frontend/
├── ml/
├── model/
├── uploads/
├── heatmaps/
├── tests/
├── docs/
├── requirements.txt
├── README.md
└── .env.example
🚀 Installation
1. Clone Repository
git clone https://github.com/shivarjunchaturvedi/TrueLens-AI.git
cd TrueLens-AI
2. Create Python Environment
python -m venv .venv

For Windows:

.\.venv\Scripts\activate
3. Install Backend Dependencies
pip install -r requirements.txt
4. Install Frontend Dependencies
cd frontend
npm install
▶️ Run the Project
Backend

From the project root:

uvicorn app.main:app --app-dir backend --reload --host 0.0.0.0 --port 8000

Backend:

http://localhost:8000

FastAPI documentation:

http://localhost:8000/docs
Frontend

Open another terminal:

cd frontend
npm run dev

Frontend:

http://localhost:5173
🔬 Detection Process
Upload Image
     ↓
File Validation
     ↓
Image Processing
     ↓
AI Model
     ↓
Real / Fake Prediction
     ↓
Confidence Calculation
     ↓
Result Display
     ↓
Scan History
📊 Results

TrueLens AI displays:

Prediction
Confidence percentage
Probability distribution
Model name
Model version
Processing time
Uploaded image

Example:

Prediction: REAL

Confidence: 98.98%

Real:           98.98%
AI Generated:    1.02%
Manipulated:     0.00%

Confidence values are model estimates and should not be treated as absolute proof.

⚠️ Limitations

The current model is a binary Real/Fake classifier.

It does not reliably distinguish between:

AI-generated images
Traditional deepfakes
Other manipulated images

Therefore, TrueLens AI provides an AI-based image authenticity estimate, not definitive forensic proof.

Results can be affected by:

Image quality
Compression
Resizing
Unseen generation techniques
Image manipulation
Differences between training data and real-world images
🧠 Machine Learning

The repository also contains ML training and experimentation code under:

ml/
├── model.py
├── config.py
├── inference/
├── preprocessing/
├── training/
└── dataset/

The project architecture supports the following conceptual classes:

REAL
AI_GENERATED
MANIPULATED

The current application inference system uses the pretrained Mirage model for Real/Fake classification.

🧪 Testing

Run backend tests with:

pytest

Test files are located in:

tests/
🔒 Security

TrueLens AI includes:

JWT authentication
Protected API endpoints
File validation
Upload size limits
User-specific scan history
Database-backed user management

For production deployment, additional security measures are recommended.

🔮 Future Improvements
🎯 Dedicated AI-generated image detector
🎭 Dedicated deepfake detector
🧠 Multi-model ensemble
🔥 Better visual explainability
📊 Precision / Recall / F1 evaluation
🎥 Video deepfake detection
🎙️ Audio deepfake detection
☁️ Cloud deployment
📱 Improved mobile support
⚡ Optimized inference
🔐 Production-grade security
👥 Team Project

TrueLens AI is a collaborative software engineering and machine-learning project combining:

Full-stack development
Machine learning
Image processing
Authentication
Database management
UI/UX
API development
Testing
Deployment
⚠️ Disclaimer

TrueLens AI is an experimental AI-based system.

Its predictions should not be treated as definitive proof of image authenticity or used as the sole basis for legal, financial, security, journalistic, or other high-stakes decisions.

👨‍💻 Developer

Shivarjun Chaturvedi

🔗 GitHub:
https://github.com/shivarjunchaturvedi

⭐ TrueLens AI — Detect. Analyze. Understand.

