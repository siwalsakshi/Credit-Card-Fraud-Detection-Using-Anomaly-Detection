# Credit Card Fraud Detection Using Anomaly Detection

**Domain:** Digital-Data-AI / AIML  
**Project Track:** HCL AIML Project  
**Techniques:** Unsupervised Anomaly Detection, SMOTE Augmentation, Behavioral Feature Engineering, Algorithmic Fairness  

---

## 📌 Project Overview

This repository provides an end-to-end Machine Learning pipeline for detecting credit card fraud using **Anomaly Detection** techniques. By modeling baseline behavioral patterns across continuous transaction streams, our unsupervised and semi-supervised models isolate anomalous spending patterns (such as rapid velocity surges, unusual merchant categories, and micro-charge card testing) while preserving smooth financial access for legitimate cardholders.

---

## 📁 Repository Structure

```text
HCL-AIML PROJECT/
├── app.py                       # Full-Stack Web Application Server (REST API + UI)
├── web/                         # Interactive Dark-Mode Frontend Dashboard
│   ├── index.html               # Real-Time Fraud Simulator & Analytics UI
│   ├── styles.css               # Glassmorphism Design System
│   └── app.js                   # Client-side Logic & Radial Gauge Animation
├── dataset.csv                  # Complete 5,000-row transaction dataset (3.5% fraud)
├── dataset_additional_4500.csv  # Calibrated 4,500 additional rows (rows 501–5000)
├── dataset_500_original.csv     # Baseline 500 rows
├── data_dictionary.csv          # Field types, nullability, ranges & business rules
├── anomaly_detection.py         # 4-Model ML Pipeline (IF, LOF, Autoencoder, SVM)
├── eda_analysis.py              # Visualisation generator script
├── eda_notebook.ipynb           # Interactive EDA analysis notebook
├── generate_architecture_diagram.py # DFD Level 0 & System Architecture generator
├── create_project_synopsis.py   # Synopsis compiler script
├── Project_Synopsis_Saksham.docx# Official filled submission document
├── PROJECT_SYNOPSIS.md          # Markdown mirror of project synopsis
├── benchmark_metrics.csv        # Comparative evaluation metrics
├── models/                      # Serialized models & preprocessing artifacts
│   ├── isolation_forest.joblib
│   ├── lof_model.joblib
│   ├── autoencoder.joblib
│   ├── one_class_svm.joblib
│   ├── scaler.joblib
│   ├── feature_columns.joblib
│   └── ae_threshold.joblib
├── visualizations/              # 5 Publication-quality charts & architecture DFD
├── progress.md                  # Milestone tracking, roadmap & task status
├── PROJECT_REPORT.md            # Comprehensive 8+ page report
└── requirements.txt             # Python dependencies
```

---

## 📊 Dataset Specifications

The dataset schema mirrors real-world production payment gateway formats:

| Column | Type | Example | Description |
| :--- | :--- | :--- | :--- |
| `trans_id` | String | `TXN_00001` | Sequential primary key for transaction auditing. |
| `timestamp` | Datetime | `2026-09-01 08:11:22` | Formatted `YYYY-MM-DD HH:MM:SS` sequential timestamps. |
| `card_token` | String | `4864-XXXX-XXXX-8846` | Masked PCI-DSS compliant card token. |
| `amount` | Float | `142.43` | Monetary transaction amount ($). |
| `merchant_category` | String | `online_retail` | Industry classification (10 categories). |
| `is_fraud` | Integer | `0` or `1` | Binary ground truth (3.5% calibrated fraud rate). |
| `merchant_id` | String | `MCH_RET_022` | Registered vendor identifier (176 distinct merchants). |
| `card_type` | String | `Visa` | Network brand (Visa, MasterCard, Amex, Discover, RuPay). |

---

## 🚀 Quick Start Guide

### 1. Prerequisites & Environment Setup
Clone or navigate to the repository directory and install dependencies:
```bash
python -m pip install -r requirements.txt
```

### 2. Launch Interactive Web Dashboard & Real-Time Detector (Frontend + Backend)
Start the unified production web application and REST API server:
```bash
python app.py
```
Open **`http://localhost:5000`** in any browser to access:
- 🚀 **Live Anomaly Simulator:** Interactive parameter adjustments with radial risk gauges and multi-model voting.
- ⚡ **Preset Attack & Routine Scenarios:** Instantly test nocturnal probing, high-value spikes, and normal grocery shopping.
- 📋 **Streaming Transaction Explorer:** Search and filter all 5,000 real rows with "Test in Sim" actions.
- 📊 **Model Comparison Grid:** Benchmarks across all 4 project brief algorithms.
- 🛡️ **Demographic Fairness Monitor:** Live False Positive Rate tracking by card type.

### 3. Run Offline ML Pipeline Benchmark & Retrain Models
To run the full pipeline, train all 4 algorithms, execute the fairness audit, and export metrics:
```bash
python anomaly_detection.py
```

The script will:
1. Load `dataset.csv` and perform temporal cyclical feature engineering and logarithmic amount scaling.
2. Train **Isolation Forest**, **Local Outlier Factor (LOF)**, and **One-Class SVM**.
3. Compute Precision, Recall, F1-Score, ROC-AUC, PR-AUC, and Confusion Matrix.
4. Execute an **Ethical Fairness Audit** breaking down False Positive Rates across card types.
5. Export serialized model artifacts to `models/` and metrics to `benchmark_metrics.csv`.

---

## 📈 Model Performance Benchmark

| Model | Precision | Recall | F1-Score | FPR | ROC-AUC | PR-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Local Outlier Factor (LOF)** | **0.1389** | 0.1143 | **0.1254** | **0.0257** | **0.6111** | **0.0659** |
| **One-Class SVM** | 0.1192 | **0.1314** | 0.1250 | 0.0352 | 0.5530 | 0.0568 |
| **Isolation Forest** | 0.0686 | 0.0686 | 0.0686 | 0.0338 | 0.5241 | 0.0483 |

---

## ⚖️ Ethical AI & Fairness Principles

- **Financial Inclusion:** Unsupervised models must minimize False Positive Rates (FPR) on legitimate purchases to avoid locking cardholders out of essential funds.
- **Brand & Demographic Neutrality:** Card brand attributes must be audited to ensure minority card brands (e.g., RuPay, Discover) are not disproportionately isolated by density-based estimators due to smaller market share.
- **Contestability:** High-scoring transactions trigger stepped-up dynamic authentication (SMS OTP / Biometric challenge) rather than immediate card termination.

---

## 📚 Detailed Documentation

- **Deployment & Cloud Hosting Guide:** See [`DEPLOYMENT.md`](DEPLOYMENT.md)
- **Project Milestones & Task Roadmap:** See [`progress.md`](progress.md)
- **Mathematical Formulations & Complete Synopsis:** See [`content.md`](content.md)
