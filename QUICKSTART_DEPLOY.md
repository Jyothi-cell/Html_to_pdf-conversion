# Quick Deployment Guide

## Files Ready for Streamlit Cloud ✅

Your app is ready to deploy! Here are all the necessary files:

### Core Files
- ✅ `streamlit_app.py` - Main app
- ✅ `html_to_pdf_standalone.py` - PDF converter
- ✅ `requirements.txt` - Python packages
- ✅ `packages.txt` - System dependencies
- ✅ `.streamlit/config.toml` - Streamlit settings
- ✅ `.gitignore` - Git ignore rules

## Deploy to Streamlit Cloud (3 Steps)

### Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "HTML to PDF Converter - Ready for deployment"

# Add your GitHub repository (create one first at github.com/new)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push
git push -u origin main
```

### Step 2: Go to Streamlit Cloud

1. Visit: https://share.streamlit.io
2. Sign in with your GitHub account
3. Click **"New app"**

### Step 3: Configure Deployment

Fill in the form:
- **Repository**: Select your repository
- **Branch**: `main`
- **Main file path**: `streamlit_app.py`

Click **"Deploy"**! 🚀

## That's It!

Streamlit Cloud will:
1. Install Python packages from `requirements.txt`
2. Install system packages from `packages.txt`
3. Apply settings from `.streamlit/config.toml`
4. Launch your app

Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

## Updating Your App

After deployment, just push changes to GitHub:

```bash
git add .
git commit -m "Updated spacing settings"
git push
```

Streamlit Cloud will automatically redeploy! ✨
