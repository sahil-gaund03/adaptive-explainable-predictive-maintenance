# Multi-Cloud Deployment Guide

This guide provides instructions for deploying the **Adaptive Explainable Predictive Maintenance Platform** across target cloud environments.

---

## 1. Streamlit Community Cloud Deployment
- **Repository**: Connect GitHub repo `https://github.com/sahil-gaund03/adaptive-explainable-predictuve-maintenance.git`
- **Main File Path**: `src/dashboard/app.py`
- **Python Version**: `3.10`
- **Config**: Automatically reads theme settings from `.streamlit/config.toml`.

---

## 2. Docker & Docker Compose Deployment
```bash
# Build and launch FastAPI (:8000), Streamlit (:8501), and MLflow (:5000)
docker-compose up --build -d

# Verify Container Health
docker-compose ps
```

---

## 3. Render / Railway Container Deployment
- **Render**: Reads configuration from `render.yaml`. Connect GitHub repo and deploy as a Web Service.
- **Railway**: Reads configuration from `railway.json`. Healthcheck configured on `/health`.

---

## 4. Environment Variables Checklist
Ensure `.env` is populated with operational parameters:
```env
APP_ENV=production
HOST=0.0.0.0
PORT=8000
MLFLOW_TRACKING_URI=mlruns
```
