"""
Application configuration.
All secrets/config come from environment variables (.env), never hard-coded.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite:///./truelens.db"

    JWT_SECRET_KEY: str = "insecure-dev-key-change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    MODEL_CHECKPOINT_PATH: str = "model/best_model.pt"
    MODEL_BACKBONE: str = "efficientnet_b0"
    MODEL_VERSION: str = "2.0-huggingface"

    UPLOAD_DIR: str = "uploads"
    HEATMAP_DIR: str = "heatmaps"
    MAX_UPLOAD_SIZE_MB: int = 10

    CORS_ORIGINS: str = "http://localhost:5173"

    HF_TOKEN: str = ""
    HF_MODEL: str = "prithivMLmods/AI-vs-Deepfake-vs-Real-Siglip2"
    HF_PROVIDER: str = "hf-inference"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


settings = Settings()
