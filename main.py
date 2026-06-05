from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import joblib
import numpy as np

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# =====================
# LOAD MODEL
# =====================
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# =====================
# SIMPLE LOGIN SYSTEM
# =====================
users = {"admin": "admin123"}

@app.post("/login")
def login(data: dict):
    if users.get(data["username"]) == data["password"]:
        return {"status": "success"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

# =====================
# FRONTEND ROUTE
# =====================
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# =====================
# PREDICTION API (VERSIONED)
# =====================
@app.post("/api/v1/predict")
def predict(data: dict):

    features = np.array([[
        data["ad_rop_sp"],
        data["ad_torque_sp"],
        data["accum_trip_in"],
        data["datetime"],
        data["depth_of_cut"],
        data["hook_load"],
        data["total_gas"],
        data["wc_bit_weight"]
    ]])

    scaled = scaler.transform(features)
    pred = model.predict(scaled)[0]

    return {
        "ROP_Average": float(pred[0]),
        "ROP_Cut_Unit": float(pred[1]),
        "ROP_Fast": float(pred[2])
    }