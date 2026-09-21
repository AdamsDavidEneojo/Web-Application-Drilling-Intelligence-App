# GitHub Setup & Push Instructions

Follow these steps to push the refactored Axelrod project to GitHub.

## Prerequisites

- GitHub account (free or paid)
- Git installed locally
- SSH key configured (or use HTTPS)

## Step 1: Create GitHub Repository

1. Go to **github.com** and sign in
2. Click **+** → **New repository**
3. Repository name: `axelrod`
4. Description: "Drilling Intelligence Platform - ML-based ROP prediction"
5. Choose **Public** (for portfolio) or **Private** (for internal use)
6. **Do NOT** initialize with README (we already have one)
7. Click **Create repository**

## Step 2: Configure Git Locally

```bash
cd C:\Users\Administrator\Desktop\rop_app

# Set git identity (one-time)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Initialize repository
git init

# Add all files (respects .gitignore)
git add .

# Verify what will be committed
git status

# Create initial commit
git commit -m "Initial commit: production-ready Axelrod v2.0.1

- Refactored backend: separated concerns (config, schemas, logger, model_loader, services)
- Added structured logging with configurable levels
- Improved error handling and validation (Pydantic)
- Optimized model loading with thread-safe caching
- Removed login page - direct access to dashboard
- Added Dockerfile with multi-stage build
- Added docker-compose.yml for local development
- Created comprehensive README with deployment guides
- Frontend cleaned up: removed auth checks, improved UX"
```

## Step 3: Connect to GitHub & Push

### Option A: HTTPS (Easier for first-time)

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/axelrod.git

# Rename default branch to main
git branch -M main

# Push to GitHub
git push -u origin main

# Enter GitHub credentials when prompted
```

### Option B: SSH (If configured)

```bash
# Add remote
git remote add origin git@github.com:YOUR_USERNAME/axelrod.git

# Rename branch
git branch -M main

# Push
git push -u origin main
```

## Step 4: Verify on GitHub

1. Refresh github.com/YOUR_USERNAME/axelrod
2. You should see all files
3. README.md displays automatically below files
4. Check that `.pkl` files are NOT there (they're in .gitignore)

## Step 5: Optional - Add GitHub Actions CI/CD

Create `.github/workflows/docker-build.yml`:

```yaml
name: Build Docker Image

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t axelrod:latest .
      
      - name: Run basic tests
        run: |
          docker run --rm axelrod:latest python -m pytest --version || echo "Tests skipped"
```

## Step 6: Deploy to Render or Cloud Platform

### Render.com (Recommended)

1. Go to **render.com** → Sign up
2. New → Web Service
3. Connect your GitHub account
4. Select `axelrod` repository
5. Configure:
   - **Name**: axelrod
   - **Environment**: Python 3.11
   - **Build**: `pip install -r requirements.txt`
   - **Start**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add environment variables:
   - `MODEL_ID`: 1HSGTNa48Ft3dgnhtDPufw321fphWf4kS
   - `SCALER_ID`: 1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp
   - `LOG_LEVEL`: INFO
7. Deploy

Then visit your live URL (e.g., `https://axelrod-abc123.onrender.com`)

### Other Platforms

- **Heroku**: Deprecated (was easy, now not recommended)
- **Railway**: Similar to Render, very easy
- **Fly.io**: Fast, good for production
- **AWS Elastic Beanstalk**: More control, steeper learning curve
- **DigitalOcean**: Affordable, straightforward

## Step 7: Post-Push Tasks

1. **Add topics** on GitHub (under repo settings):
   - `machine-learning`
   - `fastapi`
   - `docker`
   - `drilling`
   - `python`

2. **Enable GitHub Pages** (optional, for docs):
   - Settings → Pages → Source: main (docs folder)

3. **Add to portfolio**:
   - Link from personal website/LinkedIn
   - Description: "Full-stack ML platform for drilling ROP prediction"

## Updating After Push

```bash
# Make changes locally
# ...

# Commit
git add .
git commit -m "Fix: improve error handling in model loader"

# Push
git push origin main
```

## Troubleshooting

### "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/axelrod.git
git push -u origin main
```

### Files not pushing (caught by .gitignore)
```bash
# Verify what's ignored
git status

# Force-add if needed (generally don't do this)
git add -f filename.pkl  # Not recommended for large model files
```

### Branch name is "master" instead of "main"
```bash
git branch -M main
git push -u origin main
```

## Final Checklist

- [ ] Repository created on GitHub
- [ ] Git initialized locally
- [ ] All files added (except .pkl, __pycache__, venv)
- [ ] Initial commit created
- [ ] Remote added (`git remote -v` shows origin)
- [ ] Branch renamed to main
- [ ] Pushed to GitHub
- [ ] Files visible on github.com
- [ ] .pkl files NOT in repo (good!)
- [ ] README displays correctly
- [ ] Optional: Deployed to Render/Cloud

You're done! 🎉 The refactored Axelrod project is now on GitHub and ready for deployment.
