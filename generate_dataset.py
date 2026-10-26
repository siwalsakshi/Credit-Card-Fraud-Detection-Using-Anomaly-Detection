"""
Credit Card Fraud Anomaly Detection Dataset Generator
Project: Credit Card Fraud Detection Using Anomaly Detection (Project No. 32)
Domain : Digital-Data-AI / AIML
HCLTech Career Shaper Programme

Generates 4,500 additional rows precisely continuing the user's 500-row dataset.csv
to reach 5,000 rows total, matching exact column names, categories, token format,
and calibrated to 3.5% fraud rate across the full 5,000 rows.
"""

import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

def generate_exact_extension():
    # 1. Load original 500 rows
    original_path = "dataset_500_original.csv" if os.path.exists("dataset_500_original.csv") else "dataset.csv"
    df_orig = pd.read_csv(original_path)
    print(f"Loaded original {len(df_orig)} rows from {original_path}.")
    print("Columns:", df_orig.columns.tolist())
    print("Original Fraud count:", df_orig['is_fraud'].value_counts().to_dict())

    orig_fraud_count = int(df_orig['is_fraud'].sum())
    total_target_rows = 5000
    rows_to_generate = total_target_rows - len(df_orig) # 4500
    target_total_fraud = int(round(total_target_rows * 0.035)) # 175 frauds (3.5%)
    frauds_to_generate = target_total_fraud - orig_fraud_count # 175 - 6 = 169

    print(f"Generating {rows_to_generate} additional rows with {frauds_to_generate} frauds.")

    # 2. Extract pools from original data
    existing_cards = df_orig['card_token'].unique().tolist()
    existing_merchants = df_orig['merchant_id'].unique().tolist()
    card_types = ['Debit', 'Credit', 'Prepaid']
    categories = ['Fuel', 'Travel', 'Electronics', 'Online', 'Healthcare', 'Grocery', 'Restaurant']
    
    category_weights = [0.17, 0.16, 0.15, 0.14, 0.14, 0.12, 0.12]
    fraud_category_weights = [0.05, 0.25, 0.25, 0.30, 0.05, 0.04, 0.06] # Online, Travel, Electronics higher fraud
    card_type_weights = [0.35, 0.35, 0.30]

    # Map cards to card_type consistently
    card_to_type = dict(zip(df_orig['card_token'], df_orig['card_type']))
    # Expand card pool to ~1,200 cards total
    all_cards = list(existing_cards)
    while len(all_cards) < 1200:
        new_token = f"CARD_XXXX{random.randint(1000, 9999)}"
        if new_token not in card_to_type:
            ctype = np.random.choice(card_types, p=card_type_weights)
            card_to_type[new_token] = ctype
            all_cards.append(new_token)

    # Expand merchant pool to 500 merchants (MER0001 to MER0500)
    all_merchants = [f"MER{i:04d}" for i in range(1, 501)]

    # 3. Setup sequential timestamps starting after row 500
    last_timestamp_str = df_orig['timestamp'].iloc[-1]
    last_time = pd.to_datetime(last_timestamp_str)
    print(f"Sequencing timestamps starting after: {last_time}")

    # Set fraud distribution array for the 4500 rows
    is_fraud_array = np.zeros(rows_to_generate, dtype=int)
    fraud_indices = np.random.choice(rows_to_generate, size=frauds_to_generate, replace=False)
    is_fraud_array[fraud_indices] = 1

    current_time = last_time
    new_rows = []

    # Category average amounts
    cat_base_amounts = {
        'Grocery': (55.0, 30.0),
        'Restaurant': (45.0, 25.0),
        'Fuel': (65.0, 20.0),
        'Healthcare': (140.0, 80.0),
        'Electronics': (280.0, 210.0),
        'Travel': (350.0, 240.0),
        'Online': (95.0, 75.0)
    }

    start_trans_id = int(df_orig['trans_id'].iloc[-1]) + 1 # 501

    for i in range(rows_to_generate):
        trans_id = start_trans_id + i
        is_fraud = int(is_fraud_array[i])

        # Sequential delta time (mean ~15 mins, diurnal rhythm)
        hour = current_time.hour
        if 1 <= hour <= 5:
            delta_sec = int(np.random.exponential(scale=1800) + 120)
        elif 10 <= hour <= 21:
            delta_sec = int(np.random.exponential(scale=650) + 40)
        else:
            delta_sec = int(np.random.exponential(scale=950) + 60)

        current_time += timedelta(seconds=delta_sec)
        time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

        if is_fraud:
            cat = np.random.choice(categories, p=fraud_category_weights)
            # SMOTE-style fraud amounts: micro-testing probing (<$5) or large unauthorized purchases ($300-$3500)
            if np.random.random() < 0.25:
                amount = round(float(np.random.uniform(0.50, 4.99)), 2)
            else:
                amount = round(float(np.random.exponential(scale=380) + 180), 2)
                amount = min(4500.0, max(12.50, amount))
        else:
            cat = np.random.choice(categories, p=category_weights)
            mean_amt, std_amt = cat_base_amounts[cat]
            shape = 2.0
            scale = mean_amt / shape
            amount = round(float(np.random.gamma(shape, scale) + 2.5), 2)
            amount = min(4200.0, max(2.0, amount))

        card_token = random.choice(all_cards)
        card_type = card_to_type[card_token]
        merchant_id = random.choice(all_merchants)

        new_rows.append({
            'trans_id': trans_id,
            'timestamp': time_str,
            'card_token': card_token,
            'amount': amount,
            'merchant_category': cat,
            'is_fraud': is_fraud,
            'merchant_id': merchant_id,
            'card_type': card_type
        })

    df_new = pd.DataFrame(new_rows)
    # Ensure exact same columns
    df_new = df_new[df_orig.columns.tolist()]

    # Save additional 4500 rows
    df_new.to_csv("dataset_additional_4500.csv", index=False)
    print(f"Saved dataset_additional_4500.csv ({len(df_new)} rows).")

    # Combine original 500 rows + new 4500 rows to create full 5000 rows
    df_combined = pd.concat([df_orig, df_new], ignore_index=True)
    df_combined.to_csv("dataset.csv", index=False)
    print(f"Saved complete combined dataset.csv ({len(df_combined)} rows).")

    print("\n--- FINAL COMBINED DATASET SUMMARY ---")
    print("Total rows:", len(df_combined))
    print("Fraud distribution:\n", df_combined['is_fraud'].value_counts())
    print(f"Fraud rate: {df_combined['is_fraud'].mean()*100:.2f}%")
    print("Date range:", df_combined['timestamp'].min(), "to", df_combined['timestamp'].max())
    print("Categories:\n", df_combined['merchant_category'].value_counts())
    print("Card types:\n", df_combined['card_type'].value_counts())
    print("First 3 rows:\n", df_combined.head(3))
    print("Last 3 rows:\n", df_combined.tail(3))

if __name__ == "__main__":
    generate_exact_extension()
