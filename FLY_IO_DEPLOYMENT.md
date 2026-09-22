# 🚀 Deploy to Fly.io - Complete Step-by-Step Guide

## Why Fly.io?
✅ Free tier (truly free, forever)
✅ Respects Dockerfile (Python 3.11)
✅ No credit card needed
✅ Stays online 24/7

---

## Step 1: Install Flyctl (CLI Tool)

### On Windows:
1. Go to: https://fly.io/docs/hands-on/install-flyctl/
2. Download **flyctl for Windows**
3. Run the installer
4. Open PowerShell and test:
   ```
   flyctl version
   ```
   (Should show version number)

### Or use Chocolatey:
```
choco install flyctl
```

---

## Step 2: Sign Up on Fly.io

Go to: https://fly.io

- Click **"Sign Up"**
- Click **"Sign up with GitHub"**
- Authorize Fly.io to access GitHub
- Create account

---

## Step 3: Login with Flyctl

Open PowerShell and run:
```
flyctl auth login
```

- Browser opens
- Click **"Authorize"**
- Confirms in PowerShell

---

## Step 4: Prepare Your App

Open PowerShell in your project folder:
```
cd C:\Users\Administrator\Desktop\rop_app
```

Create Fly config file:
```
flyctl launch
```

Flyctl asks questions:

**"App Name?"** 
- Enter: `axelrod-app` (or any unique name)
- Press Enter

**"Choose region?"**
- Pick closest to you (or press Enter for default)

**"Would you like to set up a Postgresql database?"**
- Type: `n` (no)
- Press Enter

**"Would you like to set up an upstaging deployment?"**
- Type: `n` (no)
- Press Enter

**"Launch now?"**
- Type: `y` (yes)
- Press Enter

Flyctl deploys! Wait 2-3 minutes...

---

## Step 5: Add Environment Variables

After deploy, add your 3 variables:

```
flyctl secrets set LOG_LEVEL=INFO
flyctl secrets set MODEL_ID=1HSGTNa48Ft3dgnhtDPufw321fphWf4kS
flyctl secrets set SCALER_ID=1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp
```

Each command runs and confirms: "Secrets updated"

---

## Step 6: Redeploy with Variables

```
flyctl deploy
```

Wait 2-3 minutes for new deployment with environment variables.

---

## Step 7: Get Your URL

```
flyctl open
```

This opens your app in browser! 🎉

Or view status:
```
flyctl status
```

You'll see:
- App name
- URL (like: https://axelrod-app.fly.dev)
- Status (Running)

---

## ✅ Success Indicators

You should see:
```
Releasing new machine image...
Machine started successfully
Listening on 0.0.0.0:8000
Model loaded successfully
```

Then:
- Dashboard appears in browser ✅
- Form displays ✅
- You can make predictions ✅

---

## 🎉 Test Your App

1. Open the URL (from `flyctl open`)
2. See Axelrod dashboard
3. Fill in drilling parameters
4. Click "Run Prediction"
5. See 3 ROP metrics ✅

---

## 📊 Useful Flyctl Commands

### View logs in real-time:
```
flyctl logs
```

### Check app status:
```
flyctl status
```

### Redeploy after GitHub changes:
```
flyctl deploy
```

### Stop the app:
```
flyctl scale count=0
```

### Restart the app:
```
flyctl scale count=1
```

### View secrets:
```
flyctl secrets list
```

---

## 🚀 TL;DR - Quick Version

```powershell
# Install flyctl
choco install flyctl

# Login
flyctl auth login

# Go to project
cd C:\Users\Administrator\Desktop\rop_app

# Launch
flyctl launch
# Answer: axelrod-app, n, n, y

# Add variables
flyctl secrets set LOG_LEVEL=INFO
flyctl secrets set MODEL_ID=1HSGTNa48Ft3dgnhtDPufw321fphWf4kS
flyctl secrets set SCALER_ID=1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp

# Redeploy
flyctl deploy

# Open
flyctl open
```

Done! Your app is live and free forever ✅

---

## ❓ Troubleshooting

### "flyctl: command not found"
- Restart PowerShell after installing flyctl

### "Authentication failed"
- Run `flyctl auth login` again

### "Build failed"
- Check: `flyctl logs`
- Usually means env variables not set

### "App running but returns 502 error"
- Give it 30 seconds to fully start
- Refresh browser

### "Out of resources"
- Free tier is enough for this app
- If issues, check: `flyctl status`

---

**That's it! Your app is free and online 24/7 on Fly.io** 🚀
