# QUICK START: Push to GitHub in 5 Minutes

## Do This Now

```bash
# 1. Open PowerShell/Terminal in rop_app folder

cd C:\Users\Administrator\Desktop\rop_app

# 2. Initialize Git
git init

# 3. Configure Git (first time only)
git config --global user.name "Your Full Name"
git config --global user.email "your.email@example.com"

# 4. Add all files
git add .

# 5. Verify (check that .pkl files are NOT listed)
git status

# 6. Commit
git commit -m "Initial commit: production-ready Axelrod v2.0.1"

# 7. Go to GitHub.com and create new public repo called 'axelrod'
# (Do NOT initialize with README)

# 8. Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/axelrod.git

# 9. Push to GitHub
git branch -M main
git push -u origin main

# When prompted for password, use a GitHub Personal Access Token:
# - Go to: github.com/settings/tokens
# - Click: Generate new token (classic)
# - Check: repo (full control of repositories)
# - Copy token and paste when prompted
```

## What Gets Pushed

✅ **All Python modules** (config, schemas, logger, etc.)  
✅ **Frontend files** (index.html, welcome.html, results.html, logo.jpg)  
✅ **Docker files** (Dockerfile, docker-compose.yml, .dockerignore)  
✅ **Documentation** (README, GITHUB_SETUP, RENDER_DEPLOYMENT)  
✅ **Config files** (.gitignore, .env.example, requirements.txt)  

❌ **NOT pushed:**
- `rop_model.pkl` (large model file)
- `scaler.pkl` (large scaler file)
- `__pycache__/` (Python cache)
- `.env` (secrets, if created)
- `venv/` (virtual environment)

## After GitHub Push

### Option A: Deploy to Render (Easiest)

```
1. Go to render.com → Sign up with GitHub
2. New → Web Service → Select axelrod repo
3. Configure:
   - Build: pip install -r requirements.txt
   - Start: uvicorn main:app --host 0.0.0.0 --port $PORT
   - Add env vars: LOG_LEVEL, MODEL_ID, SCALER_ID
4. Deploy
5. Wait 5-10 min → Your URL is live!
```

See **RENDER_DEPLOYMENT.md** for detailed instructions.

### Option B: Run Locally with Docker

```bash
docker compose up

# Visit http://localhost:8000
```

### Option C: Run Locally without Docker

```bash
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

## Verify on GitHub

1. Go to `https://github.com/YOUR_USERNAME/axelrod`
2. You should see all files
3. README.md displays below file list
4. Check: `.pkl` files should NOT be there ✅

## Troubleshooting

**"fatal: remote origin already exists"**
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/axelrod.git
```

**"Permission denied (publickey)"**
- Use HTTPS instead: `https://github.com/USERNAME/axelrod.git`
- Not SSH: `git@github.com:USERNAME/axelrod.git`

**"Your branch is ahead of origin/main"**
```bash
git push origin main
```

## Files in This Project

**Python Backend**
- `main.py` - FastAPI app & routes
- `config.py` - Configuration
- `schemas.py` - Data validation
- `logger.py` - Logging
- `model_loader.py` - Model management
- `predict_service.py` - Prediction logic

**Frontend**
- `static/index.html` - Dashboard
- `static/welcome.html` - Overview
- `static/results.html` - Results guide
- `static/logo.jpg` - Logo

**Docker & DevOps**
- `Dockerfile` - Multi-stage build
- `docker-compose.yml` - Local development
- `.dockerignore` - Build exclusions
- `.gitignore` - Git exclusions
- `requirements.txt` - Python dependencies

**Documentation**
- `README.md` - Complete guide
- `GITHUB_SETUP.md` - Detailed GitHub steps
- `RENDER_DEPLOYMENT.md` - Render deployment
- `REFACTOR_SUMMARY.md` - What changed
- `PUSH_COMMANDS.sh` - Command reference

## Next Steps After Deploy

1. Test at your live URL
2. Share with team: `https://your-axelrod-url.onrender.com`
3. Make changes locally, push to GitHub → auto-deploys
4. Monitor logs in Render dashboard

---

**That's it! You're ready to go! 🚀**

Copy the bash commands above, paste into PowerShell, follow the prompts. Your Axelrod project will be on GitHub in 5 minutes.
