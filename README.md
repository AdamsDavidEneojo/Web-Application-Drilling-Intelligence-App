#  DepthIQ – Drilling Intelligence Platform

**DepthIQ** is a machine learning-powered web application designed to predict **Rate of Penetration (ROP)** in drilling operations using real-time input parameters.

It combines **petroleum engineering knowledge** with **AI/ML models** to provide fast, accurate, and actionable insights for drilling optimization.

---

##  Live Demo

👉 https://alpha-rop-ai.onrender.com

---

##  Key Features

*  **ROP Prediction (Multi-output)**

  * ROP Average
  * ROP Cut Unit
  * ROP Fast

* 📊 **Interactive Dashboard**

  * Real-time predictions
  * Visual comparison (Predicted vs Actual)
  * Dynamic charts using Chart.js

* ⚡ **FastAPI Backend**

  * High-performance API
  * Clean architecture
  * Scalable deployment

* ☁️ **Cloud Deployment**

  * Hosted on Render
  * Model served via API
  * Google Drive integration for large ML files

---

##  Tech Stack

**Frontend**

* HTML, CSS, JavaScript
* Chart.js

**Backend**

* FastAPI
* Uvicorn

**Machine Learning**

* Scikit-learn
* NumPy
* Joblib

**Deployment**

* Render
* GitHub

---

## 📂 Project Structure

```
DepthIQ/
│── main.py              # FastAPI backend
│── requirements.txt    # Dependencies
│── static/
│   └── index.html      # Frontend UI
│── .gitignore
```

---

##  Installation (Run Locally)

### 1. Clone repo

```bash
git clone https://github.com/AdamssDavidEneojo/DepthIQ.git
cd DepthIQ
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run app

```bash
python -m uvicorn main:app --reload
```

### 4. Open in browser

```
http://127.0.0.1:8000
```

---

##  API Usage

### Endpoint:

```
POST /predict
```

### Sample Request:

```json
{
  "ad_rop_sp": 10,
  "ad_torque_sp": 5,
  "accum_trip_in": 3,
  "datetime": 1,
  "depth_of_cut": 2,
  "hook_load": 50,
  "total_gas": 20,
  "wc_bit_weight": 15
}
```

### Response:

```json
{
  "ROP_Average": 309.86,
  "ROP_Cut_Unit": 259.72,
  "ROP_Fast": 420.15
}
```

---

##  Model Info

* Model: Multi-output Regression (Random Forest)
* Inputs: 8 drilling parameters
* Output: 3 ROP metrics
* Preprocessing: StandardScaler

---

##  Deployment

Deployed on Render using:

```
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port 10000
```

---

## ⚠️ Notes

* Large model files are not stored in GitHub
* Models are downloaded dynamically via Google Drive using `gdown`

---

## 📌 Future Improvements

* 📡 Real-time drilling data integration
* 📈 ROP vs Depth visualization
* 📄 Export reports (PDF)
* 🔐 Authentication system
* 🌍 Multi-well analytics dashboard

---

## 👨‍💻 Author

**Adams David**
Data Scientist | Petroleum Engineering

---

## ⭐ Acknowledgment

This project was developed as part of a **petroleum engineering + machine learning research initiative** focusing on drilling optimization.

---

## 📢 License

MIT License
