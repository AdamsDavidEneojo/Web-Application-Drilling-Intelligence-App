#!/bin/bash
# push-to-github.sh
# Quick reference for pushing Axelrod to GitHub

# This is for reference - copy/paste commands into your terminal

# ============================================
# STEP 1: Initialize Git (first time only)
# ============================================
cd /path/to/rop_app
git init

# ============================================
# STEP 2: Configure Git (first time only)
# ============================================
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# ============================================
# STEP 3: Add All Files
# ============================================
git add .
git status  # Verify files (should NOT include .pkl files)

# ============================================
# STEP 4: Create Initial Commit
# ============================================
git commit -m "Initial commit: production-ready Axelrod v2.0.1

- Refactored backend into modular components
- Added structured logging
- Implemented Pydantic validation
- Optimized model loading with caching
- Removed authentication (login page)
- Added multi-stage Dockerfile
- Created docker-compose.yml
- Comprehensive README with deployment guides
- Ready for GitHub and Render deployment"

# ============================================
# STEP 5: Rename Branch to Main
# ============================================
git branch -M main

# ============================================
# STEP 6: Add GitHub Remote
# ============================================
# IMPORTANT: Replace YOUR_USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR_USERNAME/axelrod.git

# Verify remote was added
git remote -v

# ============================================
# STEP 7: Push to GitHub
# ============================================
git push -u origin main

# When prompted, enter your GitHub credentials:
# - Username: your_github_username
# - Password: your_personal_access_token (not your account password!)
#
# To create a personal access token:
# GitHub Settings → Developer settings → Personal access tokens → Generate new token
# Scopes: repo (full control of private repositories), read:user

# ============================================
# VERIFY ON GITHUB
# ============================================
# 1. Go to: https://github.com/YOUR_USERNAME/axelrod
# 2. You should see all files
# 3. Verify .pkl files are NOT there
# 4. README.md should display on main page

# ============================================
# FUTURE PUSHES (after initial commit)
# ============================================
# Make changes...
git add .
git commit -m "Your message here"
git push origin main

# ============================================
# QUICK COMMANDS
# ============================================
# Check status
git status

# View commit history
git log --oneline

# View remote
git remote -v

# Undo last commit (if needed)
git reset --soft HEAD~1

# ============================================
# FOR WINDOWS USERS (PowerShell)
# ============================================
# Replace && with semicolon for chaining:
# git add .; git commit -m "message"; git push origin main
