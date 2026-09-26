from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routes import auth, predict, history, dashboard, health

app = FastAPI(
    title="TrueLens AI",
    description="AI-Powered Image/Media Authenticity Detection System",
    version=settings.MODEL_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


# Serve uploaded images and generated heatmaps so the frontend can display them
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
app.mount("/heatmaps", StaticFiles(directory=settings.HEATMAP_DIR), name="heatmaps")

app.include_router(health.router)
app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(history.router)
app.include_router(dashboard.router)
