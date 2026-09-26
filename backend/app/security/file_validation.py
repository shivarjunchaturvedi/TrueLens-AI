"""
Upload validation: file type (by real content, not just extension),
file size, and safe filename generation.
"""
import os
import uuid

from fastapi import HTTPException, UploadFile, status
from PIL import Image

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_PIL_FORMATS = {"JPEG", "PNG", "WEBP"}


def validate_and_save_upload(file: UploadFile, upload_dir: str, max_size_mb: int) -> tuple[str, str]:
    """
    Validates an uploaded image and saves it under a random, safe filename.
    Returns (stored_path, safe_filename).
    Raises HTTPException on any validation failure.
    """
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file extension '{ext}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}",
        )

    contents = file.file.read()
    max_bytes = max_size_mb * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max allowed size is {max_size_mb} MB.",
        )
    if len(contents) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file uploaded.")

    # Verify the file is actually a valid image (not a renamed script/executable)
    os.makedirs(upload_dir, exist_ok=True)
    safe_filename = f"{uuid.uuid4().hex}{ext}"
    stored_path = os.path.join(upload_dir, safe_filename)

    with open(stored_path, "wb") as f:
        f.write(contents)

    try:
        with Image.open(stored_path) as img:
            img.verify()
        with Image.open(stored_path) as img:
            if img.format not in ALLOWED_PIL_FORMATS:
                raise ValueError(f"Detected format {img.format} not allowed")
    except Exception:
        os.remove(stored_path)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not a valid image.",
        )

    return stored_path, safe_filename
