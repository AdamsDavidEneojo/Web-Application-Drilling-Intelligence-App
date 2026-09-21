"""
Axelrod - Drilling Intelligence Platform
FastAPI backend for ROP prediction and analysis
"""
import threading
from contextlib import asynccontextmanager
from collections import deque

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from config import (
    APP_TITLE,
    APP_VERSION,
    MODEL_ID,
    SCALER_ID,
    MODEL_PATH,
    SCALER_PATH,
    MAX_HISTORY_SIZE,
    STATIC_DIR,
)
from schemas import ROPInput, ROPOutput, HealthCheck, ModelInfo, APIInfo
from model_loader import load_models, is_model_ready
from predict_service import predict
from logger import setup_logger

logger = setup_logger(__name__)

# =========================
# HISTORY & THREAD SAFETY
# =========================
prediction_history = deque(maxlen=MAX_HISTORY_SIZE)
history_lock = threading.Lock()


# =========================
# STARTUP/SHUTDOWN
# =========================
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    # Startup
    logger.info(f"Starting {APP_TITLE} v{APP_VERSION}")
    model_thread = threading.Thread(
        target=load_models,
        args=(MODEL_ID, SCALER_ID, MODEL_PATH, SCALER_PATH),
        daemon=True,
        name="ModelLoader",
    )
    model_thread.start()
    logger.info("Model loader thread started")

    yield

    # Shutdown
    logger.info(f"Shutting down {APP_TITLE}")


# =========================
# APP INITIALIZATION
# =========================
app = FastAPI(
    title=APP_TITLE,
    version=APP_VERSION,
    description="Machine learning platform for drilling ROP prediction",
    lifespan=lifespan,
)

# =========================
# CORS MIDDLEWARE
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# STATIC FRONTEND
# =========================
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def page_response(path: str) -> FileResponse:
    """Serve a static HTML page with no-store cache control."""
    return FileResponse(path, headers={"Cache-Control": "no-store"})


@app.get("/", include_in_schema=False)
def home():
    """Home page - redirects to app."""
    return page_response(str(STATIC_DIR / "index.html"))


@app.get("/app", include_in_schema=False)
def app_ui():
    """Main predictor dashboard."""
    return page_response(str(STATIC_DIR / "index.html"))


@app.get("/welcome", include_in_schema=False)
def welcome_ui():
    """Welcome/overview page."""
    return page_response(str(STATIC_DIR / "welcome.html"))


@app.get("/results", include_in_schema=False)
def results_ui():
    """Results guide page."""
    return page_response(str(STATIC_DIR / "results.html"))


# =========================
# HEALTH & INFO ENDPOINTS
# =========================
@app.get("/health", response_model=HealthCheck, tags=["Status"])
def health() -> HealthCheck:
    """Check if model is loaded and ready."""
    status = "ready" if is_model_ready() else "loading"
    logger.debug(f"Health check: {status}")
    return HealthCheck(status=status)


@app.get("/model-info", response_model=ModelInfo, tags=["Status"])
def model_info() -> ModelInfo:
    """Get information about the model."""
    return ModelInfo(
        model="Random Forest Regressor",
        framework="scikit-learn",
        inputs=8,
        outputs=3,
        status="ready" if is_model_ready() else "loading",
    )


@app.get("/api", response_model=APIInfo, tags=["Status"])
def api_info() -> APIInfo:
    """Get API information and available endpoints."""
    return APIInfo(
        app=APP_TITLE,
        version=APP_VERSION,
        endpoints=[
            "/health",
            "/model-info",
            "/predict",
            "/history",
        ],
    )


# =========================
# PREDICTION ENDPOINT
# =========================
@app.post("/predict", response_model=ROPOutput, tags=["Prediction"])
def predict_rop(data: ROPInput) -> ROPOutput:
    """
    Run a single ROP prediction.

    Request body should contain 8 drilling signals:
    - ad_rop_sp, ad_torque_sp, accum_trip_in, datetime
    - depth_of_cut, hook_load, total_gas, wc_bit_weight

    Returns three ROP estimates: ROP_Average, ROP_Cut_Unit, ROP_Fast
    """
    try:
        if not is_model_ready():
            logger.warning("Prediction attempted while model still loading")
            raise HTTPException(
                status_code=503,
                detail="Model is still loading. Please try again in a few seconds.",
            )

        # Generate prediction
        result = predict(data)
        logger.info(f"Prediction completed: {data.ad_rop_sp} inputs")

        # Store in history
        with history_lock:
            prediction_history.append({
                "input": data.model_dump(),
                "output": result.model_dump(),
            })
            logger.debug(f"History size: {len(prediction_history)}")

        return result

    except HTTPException:
        raise
    except ValueError as e:
        logger.warning(f"Validation error in prediction: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Prediction runtime error: {e}")
        raise HTTPException(status_code=500, detail="Prediction failed internally")
    except Exception as e:
        logger.error(f"Unexpected error in predict endpoint: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


# =========================
# HISTORY ENDPOINT
# =========================
@app.get("/history", tags=["Data"])
def get_history() -> list:
    """
    Retrieve the last 20 predictions.

    Returns list of {input, output} objects.
    """
    with history_lock:
        data = list(prediction_history)
    logger.debug(f"History retrieved: {len(data)} entries")
    return data


# =========================
# ROOT ENDPOINT
# =========================
@app.get("/docs", include_in_schema=False)
def docs():
    """API documentation."""
    return FileResponse(str(STATIC_DIR / "index.html"))


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting {APP_TITLE} server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )
