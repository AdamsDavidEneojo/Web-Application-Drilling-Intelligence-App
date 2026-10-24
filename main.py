"""
Axelrod - Drilling Intelligence Platform
FastAPI backend for ROP prediction and analysis
"""
import threading
import csv
import io
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from collections import deque

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse

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
from model_loader import load_models, is_model_ready, has_model_load_failed
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
    if is_model_ready():
        return HealthCheck(status="ready", message="Prediction model is ready.")
    if has_model_load_failed():
        return HealthCheck(
            status="error",
            message="The prediction model could not be loaded. Check the service logs.",
        )
    status = "loading"
    logger.debug(f"Health check: {status}")
    return HealthCheck(status=status, message="The prediction model is starting up.")


@app.get("/health/live", tags=["Status"])
def liveness() -> dict:
    """Confirm the web process is responsive, even while the model loads."""
    return {"status": "alive"}


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
            "/health/live",
            "/model-info",
            "/predict",
            "/predict/batch",
            "/history",
            "/history.csv",
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
                "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
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


@app.post("/predict/batch", response_model=list[ROPOutput], tags=["Prediction"])
def predict_batch(data: list[ROPInput]) -> list[ROPOutput]:
    """Predict up to 100 rows in one request and include them in history."""
    if not data:
        raise HTTPException(status_code=422, detail="At least one input row is required.")
    if len(data) > 100:
        raise HTTPException(status_code=422, detail="A batch can contain at most 100 rows.")
    if not is_model_ready():
        raise HTTPException(status_code=503, detail="Model is still loading. Please try again shortly.")

    try:
        results = [predict(row) for row in data]
    except (ValueError, RuntimeError) as exc:
        logger.exception("Batch prediction failed")
        raise HTTPException(status_code=500, detail="Batch prediction failed.") from exc

    with history_lock:
        prediction_history.extend(
            {
                "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "input": row.model_dump(),
                "output": result.model_dump(),
            }
            for row, result in zip(data, results)
        )
    return results


# =========================
# HISTORY ENDPOINT
# =========================
@app.get("/history", tags=["Data"])
def get_history(limit: int = 20) -> list:
    """
    Retrieve the last 20 predictions.

    Returns list of {input, output} objects.
    """
    if not 1 <= limit <= MAX_HISTORY_SIZE:
        raise HTTPException(status_code=422, detail=f"limit must be between 1 and {MAX_HISTORY_SIZE}.")
    with history_lock:
        data = list(prediction_history)[-limit:]
    logger.debug(f"History retrieved: {len(data)} entries")
    return data


@app.get("/history.csv", tags=["Data"])
def export_history():
    """Download recent predictions, inputs, and outputs as a CSV file."""
    with history_lock:
        entries = list(prediction_history)
    output = io.StringIO(newline="")
    input_fields = list(ROPInput.model_fields)
    output_fields = list(ROPOutput.model_fields)
    writer = csv.DictWriter(output, fieldnames=["created_at"] + input_fields + output_fields)
    writer.writeheader()
    for entry in entries:
        writer.writerow({"created_at": entry.get("created_at", ""), **entry["input"], **entry["output"]})
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=rop-prediction-history.csv"},
    )


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
