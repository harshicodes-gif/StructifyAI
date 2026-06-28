from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

UPLOAD_DIR = PROJECT_ROOT / "uploads"

OUTPUT_DIR = PROJECT_ROOT / "outputs"

CACHE_DIR = PROJECT_ROOT / "cache"

DATABASE_PATH = PROJECT_ROOT / "database" / "structify.db"

MODEL_DIR = PROJECT_ROOT / "models"