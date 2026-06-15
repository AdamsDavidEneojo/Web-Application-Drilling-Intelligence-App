from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import numpy as np
import joblib
import os
import gdown
import threading
from threading import Event

# =========================
# APP INIT
# =========================
app = FastAPI(title="PIERCE AI - DepthIQ")

# =========================
# MODEL IDS (GOOGLE DRIVE)
# =========================
MODEL_ID = "1HSGTNa48Ft3dgnhtDPufw321fphWf4kS"
SCALER_ID = "1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp"

MODEL_PATH = "rop_model.pkl"
SCALER_PATH = "scaler.pkl"

model = None
scaler = None

model_ready = Event()

prediction_history = []

# =========================
# DOWNLOAD FUNCTION
# =========================
def download_file(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

# =========================
# LOAD MODEL (ASYNC SAFE)
# =========================
def load_models():
    global model, scaler

    download_file(MODEL_ID, MODEL_PATH)
    download_file(SCALER_ID, SCALER_PATH)

    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

    model_ready.set()

threading.Thread(target=load_models).start()

# =========================
# CORS
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
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")

# =========================
# HEALTH CHECK
# =========================
@app.get("/health")
def health():
    return {
        "status": "ready" if model_ready.is_set() else "loading"
    }

# =========================
# MODEL INFO (NEW)
# =========================
@app.get("/model-info")
def model_info():
    return {
        "model": "Random Forest Regressor",
        "framework": "scikit-learn",
        "inputs": 8,
        "outputs": 3,
        "status": "ready" if model_ready.is_set() else "loading"
    }

# =========================
# API INFO (NEW)
# =========================
@app.get("/api")
def api_info():
    return {
        "app": "PIERCE AI / DepthIQ",
        "version": "2.0",
        "endpoints": ["/predict", "/health", "/model-info", "/history"]
    }

# =========================
# INPUT SCHEMA
# =========================
class ROPInput(BaseModel):
    ad_rop_sp: float
    ad_torque_sp: float
    accum_trip_in: float
    datetime: float
    depth_of_cut: float
    hook_load: float
    total_gas: float
    wc_bit_weight: float

# =========================
# PREDICT ENDPOINT (UPGRADED)
# =========================
@app.post("/predict")
def predict(data: ROPInput):

    try:
        if not model_ready.is_set():
            return {"error": "Model still loading"}

        x = np.array([[

            data.ad_rop_sp,
            data.ad_torque_sp,
            data.accum_trip_in,
            data.datetime,
            data.depth_of_cut,
            data.hook_load,
            data.total_gas,
            data.wc_bit_weight

        ]])

        x = scaler.transform(x)
        pred = model.predict(x)

        result = {
            "ROP_Average": float(pred[0][0]),
            "ROP_Cut_Unit": float(pred[0][1]),
            "ROP_Fast": float(pred[0][2])
        }

        # save history
        prediction_history.append({
            "input": data.dict(),
            "output": result
        })

        return result

    except Exception as e:
        return {"error": str(e)}

# =========================
# HISTORY ENDPOINT (NEW)
# =========================
@app.get("/history")
def history():
    return prediction_history[-20:]

# =========================
# FRONTEND ENTRY
# =========================
@app.get("/app")
def app_ui():
    return FileResponse("static/index.html")