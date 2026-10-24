"""Model loading and caching."""
import os
import tempfile
import joblib
from urllib.parse import parse_qs, urlparse
from threading import Event, Lock
from logger import setup_logger

logger = setup_logger(__name__)


def normalize_drive_id(value: str) -> str:
    """Accept either a bare Google Drive file ID or a sharing URL."""
    value = value.strip()
    if "drive.google.com" not in value:
        return value

    parsed = urlparse(value)
    query_id = parse_qs(parsed.query).get("id", [None])[0]
    if query_id:
        return query_id

    parts = parsed.path.strip("/").split("/")
    if "d" in parts:
        index = parts.index("d")
        if index + 1 < len(parts):
            return parts[index + 1]
    raise ValueError("Google Drive URL does not contain a recognizable file ID")

# Global state
model = None
scaler = None
model_ready = Event()
model_lock = Lock()


def download_file(file_id: str, output_path: str) -> None:
    """Download a Google Drive artifact atomically if it is not cached."""
    if os.path.isfile(output_path) and os.path.getsize(output_path) > 100:
        logger.info("Using cached model artifact: %s", output_path)
        return

    directory = os.path.dirname(os.path.abspath(output_path))
    os.makedirs(directory, exist_ok=True)
    fd, temporary_path = tempfile.mkstemp(prefix=".model-download-", dir=directory)
    os.close(fd)
    try:
        normalized_id = normalize_drive_id(file_id)
        logger.info("Downloading model artifact %s", normalized_id)
        import gdown

        result = gdown.download(id=normalized_id, output=temporary_path, quiet=True)
        if not result or not os.path.isfile(temporary_path) or os.path.getsize(temporary_path) <= 100:
            raise RuntimeError(f"Google Drive returned an empty or invalid download for {normalized_id}")
        os.replace(temporary_path, output_path)
        logger.info("Downloaded model artifact to %s", output_path)
    except Exception:
        logger.exception("Failed to download model artifact %s", file_id)
        raise
    finally:
        if os.path.exists(temporary_path):
            os.remove(temporary_path)


def load_models(model_id: str, scaler_id: str, model_path: str, scaler_path: str) -> None:
    """Load model and scaler from disk, downloading if necessary."""
    global model, scaler

    with model_lock:
        try:
            logger.info("Starting model initialization...")

            # Download files if needed
            download_file(model_id, model_path)
            download_file(scaler_id, scaler_path)

            # Load models
            logger.info("Loading model from disk...")
            model = joblib.load(model_path)
            logger.info("Model loaded successfully")

            logger.info("Loading scaler from disk...")
            scaler = joblib.load(scaler_path)
            logger.info("Scaler loaded successfully")

            model_ready.set()
            logger.info("Model initialization complete - model is ready for predictions")

        except Exception as e:
            logger.error(f"Model initialization failed: {e}", exc_info=True)
            model_ready.clear()


def is_model_ready() -> bool:
    """Check if model is ready for predictions."""
    return model_ready.is_set()


def get_model():
    """Get the loaded model (thread-safe)."""
    with model_lock:
        return model


def get_scaler():
    """Get the loaded scaler (thread-safe)."""
    with model_lock:
        return scaler
