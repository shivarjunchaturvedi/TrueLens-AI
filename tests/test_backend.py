"""
Integration tests for the FastAPI backend.

Run from project root:
    pytest tests/ -v

Note: the /predict test will use whatever model is currently loaded
(trained checkpoint if present, otherwise the untrained fallback — see
ml/inference/predictor.py's honesty note). It only checks the API contract
(status codes, response shape), not model accuracy.
"""
import io
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

import pytest
from fastapi.testclient import TestClient
from PIL import Image

os.environ["DATABASE_URL"] = "sqlite:///./test_truelens.db"

from app.main import app  # noqa: E402

# Using TestClient as a context manager triggers FastAPI's startup event
# (which creates the DB tables), exactly like a real app boot would.
_client_cm = TestClient(app)
client = _client_cm.__enter__()


@pytest.fixture(scope="module", autouse=True)
def cleanup():
    yield
    _client_cm.__exit__(None, None, None)
    if os.path.exists("test_truelens.db"):
        os.remove("test_truelens.db")


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_register_and_login():
    register_resp = client.post("/auth/register", json={
        "username": "testuser1",
        "email": "testuser1@example.com",
        "password": "SecurePass123",
    })
    assert register_resp.status_code == 201

    login_resp = client.post("/auth/login", json={
        "username": "testuser1",
        "password": "SecurePass123",
    })
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()


def test_duplicate_register_fails():
    client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dup@example.com",
        "password": "SecurePass123",
    })
    resp = client.post("/auth/register", json={
        "username": "dupuser",
        "email": "dup@example.com",
        "password": "SecurePass123",
    })
    assert resp.status_code == 409


def test_predict_requires_auth():
    fake_image = io.BytesIO()
    Image.new("RGB", (100, 100)).save(fake_image, format="JPEG")
    fake_image.seek(0)

    resp = client.post("/predict", files={"file": ("test.jpg", fake_image, "image/jpeg")})
    assert resp.status_code == 401


def test_predict_and_history_flow():
    client.post("/auth/register", json={
        "username": "flowuser",
        "email": "flow@example.com",
        "password": "SecurePass123",
    })
    login_resp = client.post("/auth/login", json={"username": "flowuser", "password": "SecurePass123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    fake_image = io.BytesIO()
    Image.new("RGB", (224, 224), color=(120, 130, 140)).save(fake_image, format="JPEG")
    fake_image.seek(0)

    predict_resp = client.post(
        "/predict", files={"file": ("test.jpg", fake_image, "image/jpeg")}, headers=headers
    )
    assert predict_resp.status_code == 200
    body = predict_resp.json()
    assert body["prediction"] in ["REAL", "AI_GENERATED", "MANIPULATED"]
    assert 0 <= body["confidence"] <= 100

    history_resp = client.get("/history", headers=headers)
    assert history_resp.status_code == 200
    assert len(history_resp.json()) >= 1

    stats_resp = client.get("/dashboard/stats", headers=headers)
    assert stats_resp.status_code == 200
    assert stats_resp.json()["total_scans"] >= 1

    scan_id = body["scan_id"]
    delete_resp = client.delete(f"/history/{scan_id}", headers=headers)
    assert delete_resp.status_code == 204


def test_predict_rejects_bad_file_type():
    login_resp = client.post("/auth/login", json={"username": "flowuser", "password": "SecurePass123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    bad_file = io.BytesIO(b"not an image")
    resp = client.post(
        "/predict", files={"file": ("malware.exe", bad_file, "application/octet-stream")}, headers=headers
    )
    assert resp.status_code == 400
