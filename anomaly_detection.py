"""
Credit Card Fraud Detection - Machine Learning Pipeline
Project: Credit Card Fraud Detection Using Anomaly Detection
Domain : Digital-Data-AI / AIML
Project No: 32 (HCLTech Career Shaper Programme)
Algorithms: Isolation Forest, Local Outlier Factor (LOF), Autoencoder (Neural Reconstruction), One-Class SVM, and SMOTE Augmentation
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime
import joblib
import warnings
warnings.filterwarnings('ignore')

from sklearn.ensemble import IsolationForest
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import (
    precision_score, recall_score, f1_score,
    roc_auc_score, average_precision_score,
    confusion_matrix
)
from imblearn.over_sampling import SMOTE

def load_and_preprocess_data(csv_path="dataset.csv"):
    """
    Loads dataset.csv and performs feature engineering:
    - Parses timestamps into cyclical time features
    - Applies logarithmic scaling to transaction amounts
    - One-hot encodes categorical fields (merchant_category, card_type)
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset file '{csv_path}' not found. Run generate_dataset.py first.")
        
    print(f"Loading dataset from: {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df):,} transactions. Fraud cases: {df['is_fraud'].sum()} ({df['is_fraud'].mean()*100:.2f}%)")

    # 1. Temporal Feature Engineering
    df['datetime'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['datetime'].dt.hour
    df['day_of_week'] = df['datetime'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

    # Cyclical encoding for hours (24-hour cycle)
    df['hour_sin'] = np.sin(2 * np.pi * df['hour'] / 24.0)
    df['hour_cos'] = np.cos(2 * np.pi * df['hour'] / 24.0)

    # 2. Amount Log Transformation
    df['log_amount'] = np.log1p(df['amount'])

    # 3. Categorical Encoding
    cat_columns = ['merchant_category', 'card_type']
    df_encoded = pd.get_dummies(df[cat_columns], drop_first=True, dtype=float)

    # Assemble feature matrix
    numeric_features = ['log_amount', 'hour_sin', 'hour_cos', 'is_weekend']
    X = pd.concat([df[numeric_features], df_encoded], axis=1)

    # Scale continuous numerical features
    scaler = RobustScaler()
    X[['log_amount']] = scaler.fit_transform(X[['log_amount']])

    y = df['is_fraud'].values

    return df, X, y, scaler

def evaluate_predictions(y_true, y_pred, model_name, anomaly_scores=None):
    """
    Computes precision, recall, f1-score, FPR, ROC-AUC, and PR-AUC.
    """
    prec = precision_score(y_true, y_pred, zero_division=0)
    rec = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

    roc_auc = roc_auc_score(y_true, anomaly_scores) if anomaly_scores is not None else np.nan
    pr_auc = average_precision_score(y_true, anomaly_scores) if anomaly_scores is not None else np.nan

    metrics = {
        'Model': model_name,
        'Precision': round(prec, 4),
        'Recall': round(rec, 4),
        'F1-Score': round(f1, 4),
        'FPR': round(fpr, 4),
        'ROC-AUC': round(roc_auc, 4) if not np.isnan(roc_auc) else "N/A",
        'PR-AUC': round(pr_auc, 4) if not np.isnan(pr_auc) else "N/A",
        'True Positives (TP)': tp,
        'False Positives (FP)': fp,
        'False Negatives (FN)': fn,
        'True Negatives (TN)': tn
    }

    return metrics

def audit_fairness_by_card(df, y_pred, model_name="Best Model"):
    """
    Audits False Positive Rate across different card brands to verify fair treatment.
    """
    df_audit = df.copy()
    df_audit['pred_fraud'] = y_pred

    print("\n" + "-"*65)
    print(f"ETHICAL FAIRNESS AUDIT: False Positive Rate by Card Network ({model_name})")
    print("-"*65)

    audit_records = []
    for ctype, group in df_audit.groupby('card_type'):
        legit_group = group[group['is_fraud'] == 0]
        total_legit = len(legit_group)
        fp_count = (legit_group['pred_fraud'] == 1).sum()
        fpr = fp_count / total_legit if total_legit > 0 else 0.0
        audit_records.append({
            'Card Type': ctype,
            'Legitimate Txns': total_legit,
            'False Positives': fp_count,
            'False Positive Rate (FPR)': f"{fpr*100:.2f}%"
        })

    df_fairness = pd.DataFrame(audit_records)
    print(df_fairness.to_string(index=False))
    print("-"*65)

def main():
    print("="*75)
    print("HCLTech Career Shaper Programme - Project No. 32")
    print("CREDIT CARD FRAUD ANOMALY DETECTION BENCHMARK")
    print("="*75)

    # 1. Load and prepare features
    df, X, y, scaler = load_and_preprocess_data("dataset.csv")
    contamination = float(y.mean())
    print(f"Feature matrix shape: {X.shape} | Anomaly ratio: {contamination:.4f}")

    # SMOTE Demonstration
    print("\n[SMOTE] Demonstrating SMOTE oversampling for balanced training...")
    smote = SMOTE(sampling_strategy='auto', random_state=42)
    X_smote, y_smote = smote.fit_resample(X, y)
    print(f"Original shape: {X.shape} (Fraud: {y.sum()}) -> SMOTE Balanced shape: {X_smote.shape} (Fraud: {y_smote.sum()})")

    results = []

    # 2. Model 1: Isolation Forest
    print("\n[1/4] Training Isolation Forest...")
    iforest = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42,
        n_jobs=-1
    )
    iforest.fit(X)
    iforest_raw = iforest.predict(X)
    iforest_pred = (iforest_raw == -1).astype(int)
    iforest_scores = -iforest.decision_function(X)
    results.append(evaluate_predictions(y, iforest_pred, "Isolation Forest", iforest_scores))

    # 3. Model 2: Local Outlier Factor (LOF)
    print("[2/4] Training Local Outlier Factor (LOF)...")
    lof = LocalOutlierFactor(
        n_neighbors=25,
        contamination=contamination,
        novelty=True,
        n_jobs=-1
    )
    lof.fit(X)
    lof_raw = lof.predict(X)
    lof_pred = (lof_raw == -1).astype(int)
    lof_scores = -lof.decision_function(X)
    results.append(evaluate_predictions(y, lof_pred, "Local Outlier Factor (LOF)", lof_scores))

    # 4. Model 3: Neural Network Bottleneck Autoencoder
    print("[3/4] Training Neural Network Bottleneck Autoencoder (MLP Reconstruction)...")
    # Train autoencoder on inliers (normal transactions)
    X_normal = X[y == 0]
    autoencoder = MLPRegressor(
        hidden_layer_sizes=(14, 6, 14),
        activation='relu',
        solver='adam',
        max_iter=150,
        random_state=42
    )
    autoencoder.fit(X_normal, X_normal)
    # Predict reconstruction on all transactions
    X_reconstructed = autoencoder.predict(X)
    # Reconstruction Mean Squared Error (MSE) per transaction
    reconstruction_errors = np.mean(np.square(X.values - X_reconstructed), axis=1)
    # Set threshold at top (contamination) quantile
    ae_threshold = np.quantile(reconstruction_errors, 1.0 - contamination)
    ae_pred = (reconstruction_errors >= ae_threshold).astype(int)
    results.append(evaluate_predictions(y, ae_pred, "Autoencoder (Neural MSE)", reconstruction_errors))

    # 5. Model 4: One-Class SVM
    print("[4/4] Training One-Class SVM...")
    oc_svm = OneClassSVM(
        kernel='rbf',
        gamma='scale',
        nu=contamination
    )
    oc_svm.fit(X)
    oc_svm_raw = oc_svm.predict(X)
    oc_svm_pred = (oc_svm_raw == -1).astype(int)
    oc_svm_scores = -oc_svm.decision_function(X)
    results.append(evaluate_predictions(y, oc_svm_pred, "One-Class SVM", oc_svm_scores))

    # 6. Comparative Evaluation Table
    print("\n" + "="*85)
    print("BENCHMARK EVALUATION RESULTS (All 4 Project Brief Algorithms)")
    print("="*85)
    df_results = pd.DataFrame(results)
    display_cols = ['Model', 'Precision', 'Recall', 'F1-Score', 'FPR', 'ROC-AUC', 'PR-AUC', 'True Positives (TP)', 'False Positives (FP)']
    print(df_results[display_cols].to_string(index=False))
    print("="*85)

    # 7. Fairness Audit on Top Performing Anomaly Detector
    audit_fairness_by_card(df, lof_pred, "Local Outlier Factor")
    audit_fairness_by_card(df, ae_pred, "Autoencoder")

    # 8. Save model artifacts
    os.makedirs("models", exist_ok=True)
    joblib.dump(iforest, os.path.join("models", "isolation_forest.joblib"))
    joblib.dump(lof, os.path.join("models", "lof_model.joblib"))
    joblib.dump(autoencoder, os.path.join("models", "autoencoder.joblib"))
    joblib.dump(oc_svm, os.path.join("models", "one_class_svm.joblib"))
    joblib.dump(scaler, os.path.join("models", "scaler.joblib"))
    joblib.dump(X.columns.tolist(), os.path.join("models", "feature_columns.joblib"))
    joblib.dump(ae_threshold, os.path.join("models", "ae_threshold.joblib"))
    print(f"\nSaved all 4 trained models, scaler, and metadata to 'models/' directory.")

    # 9. Export metrics to CSV
    metrics_path = "benchmark_metrics.csv"
    df_results.to_csv(metrics_path, index=False)
    print(f"Saved benchmark metrics to: {metrics_path}")

if __name__ == "__main__":
    main()
