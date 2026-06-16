# Axelrod - Drilling Intelligence Platform

Axelrod is a machine learning web application for predicting rate of penetration (ROP) metrics from drilling operation inputs. It pairs a FastAPI backend with a lightweight dashboard for predictions, field-value comparison, and recent prediction review.

## Live Demo

Add your Render URL here after deployment.

## Features

- Multi-output ROP prediction:
  - ROP Average
  - ROP Cut Unit
  - ROP Fast
- Operational dashboard with input validation, model status, and Chart.js visualization.
- Login and overview page before the predictor.
- Results guide page explaining prediction outputs and predicted-vs-actual comparison.
- Predicted vs actual comparison for field checks.
- Recent prediction history served by the API.
- Google Drive model download support for large model artifacts.

## Tech Stack

Frontend:
- HTML
- CSS
- JavaScript
- Chart.js

Backend:
- FastAPI
- Uvicorn
- Pydantic

Machine learning:
- Scikit-learn
- NumPy
- Joblib

## Project Structure

```text
Axelrod/
|-- main.py
|-- requirements.txt
|-- static/
|   |-- index.html
|   |-- login.html
|   |-- results.html
|   |-- logo.jpg
|   `-- welcome.html
|-- .gitignore
`-- README.md
```

## Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API and dashboard:

```bash
python -m uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

## API

### `GET /health`

Returns whether the model is ready or still loading.

### `POST /predict`

Example request:

```json
{
  "ad_rop_sp": 10,
  "ad_torque_sp": 5,
  "accum_trip_in": 3,
  "datetime": 1781524800000,
  "depth_of_cut": 2,
  "hook_load": 50,
  "total_gas": 20,
  "wc_bit_weight": 15
}
```

Example response:

```json
{
  "ROP_Average": 309.86,
  "ROP_Cut_Unit": 259.72,
  "ROP_Fast": 420.15
}
```

### `GET /history`

Returns the 20 most recent predictions.

## Deployment

This repo includes `render.yaml` for Render blueprint deployments.

If you are using an existing GitHub-connected Render web service, use these settings in the Render dashboard:

```text
Build Command: pip install -r requirements.txt
Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

## Notes

- Large model files are downloaded at runtime and are not stored in Git.
- The dashboard disables prediction while the model is loading.
- `rop_model.pkl`, `scaler.pkl`, partial downloads, and Python cache files are ignored by Git.
- For production authentication, replace the demo `static/login.html` flow with server-side auth.

## Author

Adams David
