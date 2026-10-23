"""
Application configuration.

Secrets and environment-specific values should be supplied through environment variables
or a local .env file. Never use the development JWT secret in production.
"""
import os
import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "sqlite:///./truelens.db"

    # Empty by default so deployments must explicitly configure their own signing key.
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60

    MODEL_CHECKPOINT_PATH: str = "model/best_model.pt"
    MODEL_BACKBONE: str = "efficientnet_b0"
    MODEL_VERSION: str = "2.0-mirage"

    UPLOAD_DIR: str = "uploads"
    HEATMAP_DIR: str = "heatmaps"
    MAX_UPLOAD_SIZE_MB: int = 10

    CORS_ORIGINS: str = "http://localhost:5173"

    HF_TOKEN: str = ""
    HF_MODEL: str = "prithivMLmods/AI-vs-Deepfake-vs-Real-Siglip2"
    HF_PROVIDER: str = "hf-inference"

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()

if not settings.JWT_SECRET_KEY:
    # A random per-process key is suitable only for local development; tokens will not
    # survive a restart. Configure JWT_SECRET_KEY in .env for stable local usage/deployments.
    settings.JWT_SECRET_KEY = secrets.token_urlsafe(48)

if settings.JWT_EXPIRE_MINUTES < 1:
    raise ValueError("JWT_EXPIRE_MINUTES must be at least 1.")

if settings.MAX_UPLOAD_SIZE_MB < 1:
    raise ValueError("MAX_UPLOAD_SIZE_MB must be at least 1.")
