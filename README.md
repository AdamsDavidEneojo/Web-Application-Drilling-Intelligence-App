# Axelrod - Drilling Intelligence Platform

Axelrod is a production-ready machine learning web application for predicting rate of penetration (ROP) metrics from drilling operation inputs. It features a FastAPI backend with structured logging, a responsive dashboard for predictions, and Docker support for seamless deployment.

## Features

**Machine Learning**
- Multi-output ROP prediction using Random Forest (scikit-learn)
- Three prediction metrics: ROP Average, ROP Cut Unit, ROP Fast
- Automatic model download from Google Drive at startup

**Dashboard**
- Operational dashboard with 8 drilling signal inputs
- Real-time model status monitoring
- Predicted vs. actual value comparison with Chart.js visualization
- Recent prediction history (last 20 predictions)
- Responsive design for desktop and mobile

**Backend**
- FastAPI with automatic API documentation (`/docs`)
- Structured logging with configurable levels
- Thread-safe model loading and caching
- Comprehensive error handling and validation
- Health checks and model info endpoints

**DevOps**
- Multi-stage Dockerfile for optimized image size
- Docker Compose for local development
- Environment variable configuration
- Production-ready with healthchecks

## Tech Stack

**Backend**
- FastAPI (modern async web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- scikit-learn & NumPy (ML framework)

**Frontend**
- HTML5, CSS3, JavaScript (vanilla)
- Chart.js (data visualization)

**DevOps**
- Docker & Docker Compose
- Python 3.11 slim image

## Quick Start

### Local Development (No Docker)

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/axelrod.git
   cd axelrod
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the dashboard**
   Open `http://localhost:8000` in your browser

### Docker Compose (Recommended)

1. **Clone and navigate**
   ```bash
   git clone https://github.com/yourusername/axelrod.git
   cd axelrod
   ```

2. **Start services**
   ```bash
   docker compose up --pull always
   ```

3. **Access the dashboard**
   Open `http://localhost:8000` in your browser

4. **Stop services**
   ```bash
   docker compose down
   ```

### Docker Single Image

```bash
docker build -t axelrod:latest .
docker run -p 8000:8000 axelrod:latest
```

## Configuration

### Environment Variables

Create a `.env` file (or use `.env.example` as template):

```env
LOG_LEVEL=INFO
MODEL_ID=1HSGTNa48Ft3dgnhtDPufw321fphWf4kS
SCALER_ID=1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp
```

**Available Options**
- `LOG_LEVEL`: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)
- `MODEL_ID`: Google Drive file ID for the model pickle
- `SCALER_ID`: Google Drive file ID for the scaler pickle

## API Endpoints

### Status Endpoints

**GET `/health`**
Check if model is ready for predictions.
```json
{ "status": "ready" }
```

**GET `/model-info`**
Get model metadata.
```json
{
  "model": "Random Forest Regressor",
  "framework": "scikit-learn",
  "inputs": 8,
  "outputs": 3,
  "status": "ready"
}
```

**GET `/api`**
Get API information.
```json
{
  "app": "Axelrod",
  "version": "2.0.1",
  "endpoints": ["/health", "/model-info", "/predict", "/history"]
}
```

### Prediction Endpoint

**POST `/predict`**
Run a single prediction.

Request:
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

Response:
```json
{
  "ROP_Average": 309.86,
  "ROP_Cut_Unit": 259.72,
  "ROP_Fast": 420.15
}
```

### History Endpoint

**GET `/history`**
Retrieve the last 20 predictions.
```json
[
  {
    "input": { "ad_rop_sp": 10, ... },
    "output": { "ROP_Average": 309.86, ... }
  }
]
```

## Project Structure

```
axelrod/
├── main.py                 # FastAPI application and routes
├── config.py               # Configuration and constants
├── schemas.py              # Pydantic data models
├── logger.py               # Logging setup
├── model_loader.py         # Model download and caching
├── predict_service.py      # Prediction business logic
├── requirements.txt        # Python dependencies
├── Dockerfile              # Multi-stage Docker build
├── docker-compose.yml      # Docker Compose configuration
├── .dockerignore            # Docker build exclusions
├── .env.example             # Environment template
├── .gitignore               # Git exclusions
├── README.md                # This file
└── static/
    ├── index.html           # Main dashboard
    ├── welcome.html         # Welcome/overview page
    ├── results.html         # Results guide
    └── logo.jpg             # Axelrod logo
```

## Deployment

### Render.com (or Similar Platform)

1. **Push to GitHub** (see GitHub Setup below)
2. **Connect repository** to Render
3. **Configure build & start commands**
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Add environment variables** from `.env.example`
5. **Deploy** — model files auto-download on startup

### Kubernetes

```bash
# Create ConfigMap for static files
kubectl create configmap axelrod-static --from-file=static/

# Apply deployment and service
kubectl apply -f deployment.yaml
```

### AWS ECS / Google Cloud Run / Azure Container Instances

Push Docker image to container registry:
```bash
docker build -t your-registry/axelrod:latest .
docker push your-registry/axelrod:latest
```

Then deploy using platform-specific instructions.

## GitHub Setup

1. **Create repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: production-ready Axelrod"
   git branch -M main
   git remote add origin https://github.com/yourusername/axelrod.git
   git push -u origin main
   ```

2. **Add to .gitignore** (already included):
   - `rop_model.pkl`, `scaler.pkl` (downloaded at runtime)
   - `__pycache__/`, `*.pyc`, `.pytest_cache/`
   - `venv/`, `.env` (keep `.env.example`)

3. **Recommended: Add GitHub Actions CI/CD**
   ```yaml
   # .github/workflows/docker.yml
   name: Build and Push
   on: [push]
   jobs:
     build:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         - uses: docker/setup-buildx-action@v2
         - uses: docker/build-push-action@v4
           with:
             context: .
             push: true
             tags: your-registry/axelrod:latest
   ```

## Development

### Adding Logging

The logger is already set up. Use it in any module:

```python
from logger import setup_logger

logger = setup_logger(__name__)
logger.info("Application started")
logger.error("An error occurred", exc_info=True)
```

### Adding New Input Fields

1. Update `config.py` `INPUT_FIELDS`
2. Add field to `schemas.ROPInput`
3. Update HTML form in `static/index.html`
4. Update `predict_service.py` array construction

### Testing Locally

```bash
# Test prediction endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "ad_rop_sp": 10,
    "ad_torque_sp": 5,
    "accum_trip_in": 3,
    "datetime": 1781524800000,
    "depth_of_cut": 2,
    "hook_load": 50,
    "total_gas": 20,
    "wc_bit_weight": 15
  }'

# Check health
curl http://localhost:8000/health

# View API docs
open http://localhost:8000/docs
```

## Troubleshooting

### Model Takes a Long Time to Load
- First startup downloads ~50-100MB from Google Drive
- Subsequent startups use cached files (5-10s)
- Check logs: `docker compose logs axelrod`

### Port Already in Use
```bash
# Find and kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or use different port
docker compose up -e PORT=8001
```

### Prediction Returns 503 Error
- Model is still loading. Wait 30-60 seconds and try again.
- Check `/health` endpoint to confirm status.
- Review logs for download errors.

### Docker Build Fails
```bash
# Clear build cache
docker builder prune

# Rebuild
docker compose build --no-cache
```

## Performance Notes

- **Cold start**: ~60 seconds (first-time model download)
- **Warm start**: ~5 seconds (model cached)
- **Single prediction**: <100ms (after model loaded)
- **History limit**: 20 predictions (deque auto-discards oldest)

## Security Notes

- ✅ CORS enabled (suitable for development/internal use)
- ✅ No authentication required (add if serving public)
- ✅ Input validation on all endpoints (Pydantic)
- ⚠️ **Production**: Add authentication, rate limiting, HTTPS
- ⚠️ Model files downloaded from Google Drive (verify integrity in production)

## License

Created by Adams David. Refer to LICENSE file for details.

## Support

For issues, questions, or contributions:
1. Check the troubleshooting section above
2. Review `/docs` API documentation
3. Check application logs: `docker compose logs -f`
4. Open an issue on GitHub

---

**Ready to deploy?** Start with `docker compose up --pull always` or push to GitHub and connect to Render/Cloud Run.
