"""
Exploratory Data Analysis (EDA) Script for Credit Card Fraud Detection
Project: Credit Card Fraud Detection Using Anomaly Detection
Domain : Digital-Data-AI / AIML
Deliverable: EDA notebook or analysis script with 3+ visualisations
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

def perform_eda(csv_path="dataset.csv", output_dir="visualizations"):
    os.makedirs(output_dir, exist_ok=True)
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    df['datetime'] = pd.to_datetime(df['timestamp'])
    df['hour'] = df['datetime'].dt.hour
    df['log_amount'] = np.log1p(df['amount'])
    
    print("\n--- Summary Statistics ---")
    print(f"Total Transactions: {len(df):,}")
    print(f"Legitimate (0): {(df['is_fraud']==0).sum():,} ({(df['is_fraud']==0).mean()*100:.2f}%)")
    print(f"Fraudulent (1): {(df['is_fraud']==1).sum():,} ({(df['is_fraud']==1).mean()*100:.2f}%)")
    
    # -------------------------------------------------------------
    # Visualisation 1: Class Imbalance & Transaction Proportions
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    
    # Bar plot
    palette = ['#2b5c8f', '#d9534f']
    sns.countplot(data=df, x='is_fraud', ax=axes[0], palette=palette, hue='is_fraud', legend=False)
    axes[0].set_title("Transaction Count by Class Label", fontsize=14, fontweight='bold', pad=12)
    axes[0].set_xlabel("Is Fraud (0 = Legitimate, 1 = Fraud)", fontsize=11)
    axes[0].set_ylabel("Number of Transactions", fontsize=11)
    for p in axes[0].patches:
        height = p.get_height()
        axes[0].annotate(f'{int(height):,}\n({height/len(df)*100:.1f}%)',
                         (p.get_x() + p.get_width() / 2., height / 2),
                         ha='center', va='center', fontsize=11, color='white', fontweight='bold')

    # Donut chart
    fraud_counts = df['is_fraud'].value_counts()
    axes[1].pie(fraud_counts, labels=['Legitimate (96.5%)', 'Fraudulent Anomaly (3.5%)'],
                colors=['#2b5c8f', '#d9534f'], autopct='%1.1f%%', startangle=140,
                explode=(0, 0.1), wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2))
    axes[1].set_title("Imbalanced Class Proportion", fontsize=14, fontweight='bold', pad=12)
    
    plt.tight_layout()
    v1_path = os.path.join(output_dir, "01_class_imbalance.png")
    plt.savefig(v1_path, dpi=300)
    plt.close()
    print(f"Saved: {v1_path}")

    # -------------------------------------------------------------
    # Visualisation 2: Amount Distribution (Normal vs Fraud)
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Kernel Density Estimation on Log Scale
    sns.kdeplot(data=df[df['is_fraud']==0]['log_amount'], ax=axes[0], label='Legitimate', color='#2b5c8f', fill=True, alpha=0.35)
    sns.kdeplot(data=df[df['is_fraud']==1]['log_amount'], ax=axes[0], label='Fraud (Anomaly)', color='#d9534f', fill=True, alpha=0.45)
    axes[0].set_title("Log Amount Density Distribution", fontsize=13, fontweight='bold')
    axes[0].set_xlabel("log(1 + Transaction Amount in $)", fontsize=11)
    axes[0].set_ylabel("Density", fontsize=11)
    axes[0].legend(frameon=True)

    # Box plot comparing raw amounts up to 99th percentile
    p99 = df['amount'].quantile(0.99)
    df_filtered = df[df['amount'] <= p99]
    sns.boxplot(data=df_filtered, x='is_fraud', y='amount', ax=axes[1], palette=palette, hue='is_fraud', legend=False)
    axes[1].set_title("Amount Distribution (Capped at 99th Percentile)", fontsize=13, fontweight='bold')
    axes[1].set_xlabel("Is Fraud (0 = Legitimate, 1 = Fraud)", fontsize=11)
    axes[1].set_ylabel("Amount ($)", fontsize=11)

    plt.tight_layout()
    v2_path = os.path.join(output_dir, "02_amount_distribution.png")
    plt.savefig(v2_path, dpi=300)
    plt.close()
    print(f"Saved: {v2_path}")

    # -------------------------------------------------------------
    # Visualisation 3: Circadian Temporal Pattern (Diurnal Rhythm)
    # -------------------------------------------------------------
    fig, ax1 = plt.subplots(figsize=(12, 5))

    hourly_stats = df.groupby('hour').agg(
        total_txns=('is_fraud', 'count'),
        fraud_txns=('is_fraud', 'sum')
    ).reset_index()
    hourly_stats['fraud_rate'] = (hourly_stats['fraud_txns'] / hourly_stats['total_txns']) * 100

    color = '#2b5c8f'
    ax1.set_xlabel('Hour of Day (00:00 to 23:00)', fontsize=11)
    ax1.set_ylabel('Total Transaction Volume', color=color, fontsize=11)
    bars = ax1.bar(hourly_stats['hour'], hourly_stats['total_txns'], color=color, alpha=0.6, width=0.7, label='Transaction Volume')
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_xticks(range(0, 24))

    ax2 = ax1.twinx()
    color2 = '#d9534f'
    ax2.set_ylabel('Fraud Anomaly Rate (%)', color=color2, fontsize=11)
    line = ax2.plot(hourly_stats['hour'], hourly_stats['fraud_rate'], color=color2, marker='o', linewidth=2.5, label='Fraud Rate %')
    ax2.tick_params(axis='y', labelcolor=color2)
    ax2.grid(False)

    plt.title("Circadian Temporal Trends: Hourly Transaction Density vs. Fraud Rate", fontsize=13, fontweight='bold', pad=14)
    plt.tight_layout()
    v3_path = os.path.join(output_dir, "03_temporal_trends.png")
    plt.savefig(v3_path, dpi=300)
    plt.close()
    print(f"Saved: {v3_path}")

    # -------------------------------------------------------------
    # Visualisation 4: Fraud by Merchant Category & Card Type
    # -------------------------------------------------------------
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))

    # By Merchant Category
    cat_summary = df.groupby('merchant_category')['is_fraud'].agg(['count', 'mean']).reset_index()
    cat_summary['mean'] = cat_summary['mean'] * 100
    cat_summary = cat_summary.sort_values(by='mean', ascending=True)

    axes[0].barh(cat_summary['merchant_category'], cat_summary['mean'], color='#4a90e2', edgecolor='none')
    axes[0].set_title("Fraud Anomaly Rate by Merchant Sector (%)", fontsize=13, fontweight='bold')
    axes[0].set_xlabel("Fraud Rate (%)", fontsize=11)
    for i, v in enumerate(cat_summary['mean']):
        axes[0].text(v + 0.1, i, f"{v:.1f}%", va='center', fontsize=10, fontweight='bold')

    # By Card Network
    card_summary = df.groupby('card_type')['is_fraud'].agg(['count', 'mean']).reset_index()
    card_summary['mean'] = card_summary['mean'] * 100
    card_summary = card_summary.sort_values(by='mean', ascending=True)

    axes[1].barh(card_summary['card_type'], card_summary['mean'], color='#50e3c2', edgecolor='none')
    axes[1].set_title("Fraud Rate by Card Network (%)", fontsize=13, fontweight='bold')
    axes[1].set_xlabel("Fraud Rate (%)", fontsize=11)
    for i, v in enumerate(card_summary['mean']):
        axes[1].text(v + 0.05, i, f"{v:.2f}%", va='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    v4_path = os.path.join(output_dir, "04_category_card_breakdown.png")
    plt.savefig(v4_path, dpi=300)
    plt.close()
    print(f"Saved: {v4_path}")

    print(f"\nAll 4 visualisations successfully generated and saved to '{output_dir}/' directory.")

if __name__ == "__main__":
    perform_eda()
