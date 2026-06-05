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

app = FastAPI(title="DepthIQ")

# =========================
# MODEL IDS
# =========================
MODEL_ID = "1HSGTNa48Ft3dgnhtDPufw321fphWf4kS"
SCALER_ID = "1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp"

MODEL_PATH = "rop_model.pkl"
SCALER_PATH = "scaler.pkl"

model = None
scaler = None

# =========================
# DOWNLOAD FUNCTION
# =========================
def download_file(file_id, output):
    if not os.path.exists(output):
        url = f"https://drive.google.com/uc?id={file_id}"
        gdown.download(url, output, quiet=False)

# =========================
# LOAD MODELS (ASYNC SAFE)
# =========================
def load_models():
    global model, scaler
    download_file(MODEL_ID, MODEL_PATH)
    download_file(SCALER_ID, SCALER_PATH)
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

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
# FRONTEND
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
    return {"status": "loading" if model is None else "ready"}

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
# PREDICT
# =========================
@app.post("/predict")
def predict(data: ROPInput):

    if model is None:
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

    return {
        "ROP_Average": float(pred[0][0]),
        "ROP_Cut_Unit": float(pred[0][1]),
        "ROP_Fast": float(pred[0][2])
    }