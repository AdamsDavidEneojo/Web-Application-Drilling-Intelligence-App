# 🚀 FLY.IO - Quick Deploy (Free Forever)

## What You Need
- Flyctl installed
- Fly.io account (free)
- PowerShell

---

## Quick Commands

### 1. Install Flyctl
```
choco install flyctl
```

### 2. Login
```
flyctl auth login
```

### 3. Go to Project
```
cd C:\Users\Administrator\Desktop\rop_app
```

### 4. Launch
```
flyctl launch
```

Answers:
- App Name: `axelrod-app`
- Region: (press Enter)
- Database: `n`
- Staging: `n`
- Launch: `y`

### 5. Add Variables
```
flyctl secrets set LOG_LEVEL=INFO
flyctl secrets set MODEL_ID=1HSGTNa48Ft3dgnhtDPufw321fphWf4kS
flyctl secrets set SCALER_ID=1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp
```

### 6. Redeploy
```
flyctl deploy
```

### 7. Open
```
flyctl open
```

---

## ✅ Done!

Your app is:
- ✅ Live at: https://axelrod-app.fly.dev
- ✅ Free forever (no payment needed)
- ✅ Running 24/7
- ✅ Using Python 3.11 (from Dockerfile)

---

**See FLY_IO_DEPLOYMENT.md for detailed step-by-step guide with screenshots.**

Go run those commands now! 🎉
