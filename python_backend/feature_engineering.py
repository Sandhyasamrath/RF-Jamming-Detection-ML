"""
Day 6 - Feature Engineering
RF Jamming Detection System
Input:  data/dataset.csv       (9000 rows, 8 features)
Output: data/processed_dataset.csv (9000 rows, 14 features)
"""

import numpy as np
import pandas as pd
from scipy import stats
import os

# Load raw dataset
input_path = os.path.join('..', 'data', 'dataset.csv')
df = pd.read_csv(input_path)

print("=" * 55)
print("Day 6 - Feature Engineering")
print("=" * 55)
print(f"Input shape: {df.shape}")

features = ['RSSI', 'SNR', 'PDR', 'Packet_Loss',
            'Noise_Power', 'FFT_Mean', 'FFT_Variance', 'Peak_Frequency']

# ── 1. Moving Average (window=5) ─────────────────────────────
print("\n[1/5] Adding moving averages...")
for f in ['RSSI', 'SNR', 'PDR']:
    df[f'{f}_MA5'] = df[f].rolling(window=5, min_periods=1).mean().round(4)

# ── 2. Rolling Variance (window=5) ───────────────────────────
print("[2/5] Adding rolling variance...")
for f in ['RSSI', 'FFT_Mean']:
    df[f'{f}_RollingVar'] = df[f].rolling(window=5, min_periods=1).var().fillna(0).round(4)

# ── 3. Z-Score Normalization ──────────────────────────────────
print("[3/5] Adding z-score normalization...")
for f in features:
    df[f'{f}_ZScore'] = stats.zscore(df[f]).round(4)

# ── 4. FFT Behavior Pattern ───────────────────────────────────
print("[4/5] Adding FFT behavior pattern...")
# FFT energy ratio: how dominant is the peak vs mean
df['FFT_Energy_Ratio'] = (df['FFT_Mean'] / (df['FFT_Variance'] + 1e-6)).round(4)

# ── 5. Signal Quality Index ───────────────────────────────────
print("[5/5] Adding Signal Quality Index...")
# Composite feature: combines RSSI + SNR + PDR into single score
df['Signal_Quality_Index'] = (
    (df['RSSI'] / df['RSSI'].min()) * 0.4 +
    (df['SNR']  / df['SNR'].max())  * 0.4 +
    (df['PDR'])                      * 0.2
).round(4)

# ── Save processed dataset ────────────────────────────────────
output_path = os.path.join('..', 'data', 'processed_dataset.csv')
df.to_csv(output_path, index=False)

print("\n" + "=" * 55)
print(f"Output shape: {df.shape}")
print(f"\nAll columns ({len(df.columns)}):")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2}. {col}")

print(f"\nClass distribution:")
print(df['Label_Name'].value_counts())

print(f"\nSample stats (first 5 engineered features):")
eng_cols = ['RSSI_MA5', 'SNR_MA5', 'FFT_Energy_Ratio',
            'Signal_Quality_Index', 'RSSI_ZScore']
print(df[eng_cols].describe().round(3))

# Validate no nulls
null_count = df.isnull().sum().sum()
print(f"\nNull values: {null_count} (should be 0)")
print(f"\nDataset saved to: {output_path}")
print("Day 6 Complete - processed_dataset.csv ready!")
