# ⚡ URGENT FIX - Do This NOW

## Problem Identified
Pydantic-core needs Rust compilation on Render (filesystem is read-only)

## Solution Applied ✅
- Downgraded pydantic to 2.4.2 (pre-built wheel)
- Simplified all dependencies
- Updated render.yaml with correct config

**Changes pushed to GitHub**

---

## 🎯 DO THIS (5 Minutes)

### Step 1: Delete Old Service
1. Go: https://dashboard.render.com
2. Click: "axelrod" service
3. Click: **Settings** (scroll to bottom)
4. Click: **Delete Service**
5. Confirm

### Step 2: Create New Service
1. **New +** → **Web Service**
2. **Connect** your GitHub repo
3. **Name**: axelrod
4. **Python Version**: 3.11
5. **Build Command**: `pip install --no-cache-dir -r requirements.txt`
6. **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Add Environment Variables
Click **Advanced**:
```
LOG_LEVEL = INFO
MODEL_ID = 1HSGTNa48Ft3dgnhtDPufw321fphWf4kS
SCALER_ID = 1kPLWoJbFaU3jC3jSENalLo1dSRz25mjp
```

### Step 4: Deploy
Click **Create Web Service** and wait 5-10 min

---

## ✅ Success Signs

Look for:
```
Successfully installed fastapi uvicorn numpy scikit-learn pydantic...
Uvicorn running on http://0.0.0.0:10000
Model loaded successfully
```

Then green **Live** badge appears ✅

---

## ❌ If It Fails Again

Check **Logs** tab in Render real-time and tell me the error message.

---

**Do this now - fresh deployment should work!** 🚀
