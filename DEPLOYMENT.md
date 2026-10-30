# Deployment Guide — Credit Card Fraud Anomaly Detection Platform

This repository is fully containerized and configured for zero-friction cloud deployment. Follow any of the options below to deploy the unified web dashboard and REST API.

---

## 🚀 Option 1: 1-Click Cloud Deployment via Render (Recommended Free Tier)

1. Fork or push this repository to your GitHub account:  
   `https://github.com/siwalsakshi/Credit-Card-Fraud-Detection-Using-Anomaly-Detection`
2. Go to **[Render.com](https://render.com/)** and log in with GitHub.
3. Click **New +** -> **Web Service** (or **Blueprint** to use the bundled [`render.yaml`](render.yaml)).
4. Select your repository.
5. Render will automatically detect the settings:
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
   - **Health Check Path:** `/api/status`
6. Click **Create Web Service**. Your live public application will be available at:  
   `https://shield-ai-fraud-detection.onrender.com`

---

## ⚡ Option 2: 1-Click Deployment via Railway

1. Go to **[Railway.app](https://railway.app/)** and log in.
2. Click **New Project** -> **Deploy from GitHub repo**.
3. Select this repository.
4. Railway will automatically detect the bundled [`Procfile`](Procfile) and [`requirements.txt`](requirements.txt) or [`Dockerfile`](Dockerfile).
5. Railway assigns a public domain under **Settings -> Networking -> Generate Domain**.

---

## 🤗 Option 3: Deploy to Hugging Face Spaces

1. Go to **[Hugging Face Spaces](https://huggingface.co/spaces)** and click **Create new Space**.
2. Set Space SDK to **Docker** (Blank) or **Gradio/Streamlit**.
3. Push or sync this repository. The provided [`Dockerfile`](Dockerfile) will build and serve the application automatically on Hugging Face Spaces.

---

## 🐳 Option 4: Production Container Deployment (Docker)

To run the application inside a standalone Docker container locally or on any VPS (AWS EC2, DigitalOcean, Google Cloud Compute):

```bash
# 1. Build the Docker image
docker build -t shield-ai-fraud-detection:latest .

# 2. Run the container on port 5000
docker run -d -p 5000:5000 --name fraud-detection shield-ai-fraud-detection:latest

# 3. Check container logs
docker logs -f fraud-detection
```

Access the platform at `http://localhost:5000`.

---

## 📡 Exposed API Endpoints

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `/` | `GET` | Interactive Dark-Mode Web Dashboard |
| `/api/status` | `GET` | Health check & model initialization state |
| `/api/stats` | `GET` | Summary statistics of the 5,000-row dataset |
| `/api/benchmark` | `GET` | Benchmark evaluation metrics across 4 models |
| `/api/fairness` | `GET` | Ethical audit metrics by card network brand |
| `/api/transactions` | `GET` | Paginated transaction explorer API (`?limit=15&offset=0&filter=all`) |
| `/api/predict` | `POST` | Live inference scoring across multi-model ensemble |
