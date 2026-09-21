# Deployment Guide - Render.com

Complete step-by-step guide to deploy Axelrod to Render.com for free.

## Why Render?

✅ Free tier available (limited but sufficient for testing)  
✅ GitHub integration (auto-deploy on push)  
✅ No credit card required for free tier  
✅ Auto-download model files at startup  
✅ Built-in health checks  
✅ Easy SSL/HTTPS  

## Prerequisites

- Axelrod GitHub repository (public)
- Render.com account (free signup)
- GitHub account with push access

## Step 1: Create Render Account

1. Go to **render.com**
2. Click **Sign up** → Choose **GitHub**
3. Authorize Render to access your GitHub account
4. Complete signup

## Step 2: Create New Web Service

1. Dashboard → **New +** → **Web Service**
2. **Connect repository**:
   - Search for "axelrod"
   - Select `your-username/axelrod`
   - Click **Connect**

3. **Configure web service**:

   | Setting | Value |
   |---------|-------|
   | **Name** | axelrod |
   | **Environment** | Python 3.11 |
   | **Build Command** | `pip install -r requirements.txt` |
   | **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
   | **Plan** | Free (or Starter) |

4. Click **Advanced** and add **Environment Variables**:

   ```
   LOG_LEVEL = INFO
   MODEL_ID = 1HSGTNa48Ft3dgnhtDPufw321fphWf4kS
   SCALER_ID = 1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp
   ```

5. Click **Create Web Service**

## Step 3: Wait for Deployment

The build will start automatically:

- **Stage 1**: Install dependencies (~2-3 min)
- **Stage 2**: Model download from Google Drive (~1-2 min, first time only)
- **Stage 3**: App startup (~30 sec)

**Total first build: ~5-10 minutes**

You'll see a log output like:

```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Starting model initialization...
INFO:     Downloading file... (status bar)
INFO:     Model loaded successfully
INFO:     Scaler loaded successfully
INFO:     Model initialization complete - model is ready
```

## Step 4: Access Your App

After deployment completes:

1. You'll see a **live URL** like: `https://axelrod-abc123.onrender.com`
2. Click the URL or visit it in your browser
3. Dashboard appears → Model loads (may take 30-60s first time)

## Step 5: Auto-Deploy on GitHub Push

Every time you push to GitHub:

```bash
git commit -am "Fix: improve validation"
git push origin main
```

Render automatically triggers a rebuild. Watch logs in Render dashboard.

## Monitoring & Logs

**View logs in real-time:**
- Render dashboard → Services → axelrod → Logs

**Common entries:**
```
Starting axelrod v2.0.1
Starting model initialization...
Downloading file 1HSGTNa48... (first time)
Model loaded successfully
Health check passed
GET /health 200 (polling from dashboard)
POST /predict 200 (user made a prediction)
```

## Troubleshooting

### "Model is still loading" Error

**Cause**: Model download taking longer than expected  
**Solution**: Wait 2-3 minutes, refresh browser, try again

```bash
# Check status
curl https://your-axelrod-url.onrender.com/health
# Returns: {"status":"loading"} → wait
# Returns: {"status":"ready"} → good
```

### Service keeps restarting

**Cause**: Out of memory or crash during model loading  
**Solution**:
1. Check logs for errors
2. Verify Google Drive file IDs in environment variables
3. Consider upgrading to Starter plan (more memory)

### Build takes >15 minutes

**Cause**: Slow internet or Render infrastructure  
**Solution**:
1. This is normal on free tier
2. First build is slowest (model download)
3. Subsequent builds are ~2-3 minutes

### "Build failed: Command exited with non-zero status"

**Cause**: Dependency installation error  
**Solution**:
1. Check `requirements.txt` for version conflicts
2. Try: `pip install -U pip setuptools`
3. Verify Python 3.11 is selected

## Performance on Free Tier

| Metric | Performance |
|--------|-------------|
| Cold startup | ~60 sec (first time) |
| Warm startup | ~5 sec |
| Prediction latency | <100ms |
| Concurrent users | ~5-10 (free tier) |
| Auto-sleep | After 15 min inactivity |

**Note**: Free tier services sleep after 15 minutes of inactivity. First request wakes them (30-60 sec).

## Upgrading to Paid Plan

If you need better performance:

1. Dashboard → Services → axelrod
2. Settings → Instance Type → **Starter** ($7/month)
   - 0.5 CPU, 512MB RAM
   - No auto-sleep
   - Better performance

3. Or **Professional** ($12/month)
   - 1 CPU, 1GB RAM
   - Recommended for production

## Adding Custom Domain

1. Render dashboard → Settings → Custom Domain
2. Enter your domain (e.g., `rop.yourdomain.com`)
3. Add CNAME record to your DNS pointing to Render's URL
4. SSL certificate auto-provisioned

## Best Practices

**✅ DO:**
- Push only tested code to main branch
- Monitor logs regularly
- Use environment variables for secrets
- Set up GitHub branch protection rules

**❌ DON'T:**
- Hard-code API keys or model IDs in code
- Push large model files to GitHub
- Use free tier for production (unreliable)

## Additional Resources

- [Render Docs](https://render.com/docs)
- [FastAPI on Render](https://render.com/docs/deploy-fastapi)
- [Custom Domains](https://render.com/docs/custom-domains)
- [Environment Variables](https://render.com/docs/environment-variables)

## Example Deployed Dashboard

Once live, your dashboard will be at:

```
https://axelrod-YOUR_ID.onrender.com/

/app         - Main dashboard
/welcome     - Welcome page
/results     - Results guide
/health      - Health check API
/docs        - FastAPI documentation
/predict     - Prediction API endpoint
/history     - Prediction history
```

## Quick Reference: Render CLI (Optional)

If you prefer command-line deployment:

```bash
# Install Render CLI
npm install -g render-cli

# Deploy
render deploy

# View logs
render logs axelrod
```

## Support

Having issues? Check these in order:

1. **Logs**: Always check Render logs first
2. **GitHub Issues**: Search existing issues
3. **Documentation**: Check README.md in repo
4. **Render Support**: support@render.com

---

**Ready?** Follow steps 1-5 above. Your Axelrod dashboard will be live in 5-10 minutes! 🚀
