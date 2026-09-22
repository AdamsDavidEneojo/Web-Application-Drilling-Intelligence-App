# 🚀 Deploy to Railway - Complete Step-by-Step Guide

## Step 1: Go to Railway
Open: https://railway.app

## Step 2: Sign Up
- Click **"Start Free"** or **"Sign Up"**
- Click **"Continue with GitHub"**
- Click **"Authorize Railway"**
- It will ask permissions - click **"Authorize"**

## Step 3: Create New Project
- After login, you see your dashboard
- Click **"+ New Project"** button (top right)
- Click **"Deploy from GitHub repo"**

## Step 4: Connect Your Repository
- A list appears showing your GitHub repos
- Search for: `Web-Application-Drilling-Intelligence-App`
- Click on it when you find it
- Click **"Deploy Now"** button

## Step 5: Wait for Auto-Detection
Railway automatically:
- Detects your Dockerfile ✅
- Uses Python 3.11 ✅
- Reads requirements.txt ✅
- Starts building ✅

You'll see: **"Building..."** in the logs

## Step 6: Add Environment Variables
While it's building:

1. In the left sidebar, look for your service name (might say "axelrod" or "web")
2. Click on it
3. Look for **"Variables"** tab (or **"Environment"** tab)
4. Click **"+ New Variable"**
5. Add these THREE variables:

**First Variable:**
- Name: `LOG_LEVEL`
- Value: `INFO`
- Click "Add"

**Second Variable:**
- Name: `MODEL_ID`
- Value: `1HSGTNa48Ft3dgnhtDPufw321fphWf4kS`
- Click "Add"

**Third Variable:**
- Name: `SCALER_ID`
- Value: `1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp`
- Click "Add"

## Step 7: Deploy
- After adding variables, Railway should auto-redeploy
- Watch the logs - you'll see:
  ```
  Building from Dockerfile...
  Using Python 3.11.x
  Installing dependencies...
  Successfully installed fastapi uvicorn numpy scikit-learn...
  Starting application...
  Uvicorn running on 0.0.0.0:8000
  Model loaded successfully
  ```

## Step 8: Get Your Live URL
- When build completes, look at top right
- You'll see a URL like: `https://your-app-name.up.railway.app`
- Click it to open your dashboard ✅

## ✅ Success Indicators
- ✅ Green status (Active or Deployed)
- ✅ No error messages in logs
- ✅ URL appears
- ✅ Click URL → Dashboard loads

## 📊 Expected Build Time
- 1-2 minutes: Downloading files
- 1-2 minutes: Installing dependencies
- 30 seconds: Starting app
- **Total: 3-5 minutes**

## 🎉 Test Your App
Once live:
1. Open the Railway URL
2. You see the Axelrod dashboard
3. Fill in drilling parameters
4. Click "Run Prediction"
5. See 3 ROP metrics ✅

---

## 📞 If Something Goes Wrong

### Check Logs
- Click your service
- Look for **"Logs"** or **"Deployments"** tab
- Watch the real-time output
- Tell me what error you see

### Common Issues

**Issue: Build still running**
- Just wait 2-3 more minutes
- Building takes time on first deploy

**Issue: Build failed**
- Check the error in logs
- Usually it's environment variable related
- Tell me the error

**Issue: Can't find Variables tab**
- Click your service name in left sidebar
- Look for tabs: Deployments, Logs, Variables, Settings
- If not visible, scroll right in the tab bar

---

## 🚀 TL;DR - Quick Version

1. https://railway.app
2. Sign up with GitHub
3. + New Project → Deploy from GitHub
4. Select your repo
5. Add 3 environment variables (LOG_LEVEL, MODEL_ID, SCALER_ID)
6. Wait 5 minutes
7. Click the URL → Live! ✅

---

**That's it! Railway will handle everything else.** 🎉
