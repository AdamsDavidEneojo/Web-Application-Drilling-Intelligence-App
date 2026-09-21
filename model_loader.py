"""Model loading and caching."""
import os
import joblib
import gdown
from threading import Event, Lock
from logger import setup_logger

logger = setup_logger(__name__)

# Global state
model = None
scaler = None
model_ready = Event()
model_lock = Lock()


def download_file(file_id: str, output_path: str) -> None:
    """Download a file from Google Drive if it doesn't exist."""
    if os.path.exists(output_path):
        logger.info(f"File already exists: {output_path}")
        return

    try:
        logger.info(f"Downloading file {file_id} to {output_path}...")
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output_path, quiet=False)
        logger.info(f"Successfully downloaded: {output_path}")
    except Exception as e:
        logger.error(f"Failed to download {file_id}: {e}")
        raise


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
            logger.info("Model initialization complete - model is ready")

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
