import os
from pathlib import Path
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]
MAX_UPLOAD_BYTES = int(float(os.getenv("MAX_UPLOAD_MB", "5")) * 1024 * 1024)
LOW_CONFIDENCE = float(os.getenv("LOW_CONFIDENCE_THRESHOLD", "0.6"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cleantech.db")
MODEL_DIR = Path(os.getenv("MODEL_DIR", Path(__file__).resolve().parents[3] / "ml" / "models"))
ALLOWED_TYPES = {"image/jpeg", "image/png"}
