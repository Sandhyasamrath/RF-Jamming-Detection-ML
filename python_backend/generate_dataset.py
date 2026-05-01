"""
Day 5 - Synthetic Dataset Generation
RF Jamming Detection System
Generates 9000 rows: 3000 Normal + 3000 Weak Jam + 3000 Strong Jam
"""

import numpy as np
import pandas as pd
from feature_utils import FEATURE_RANGES, FEATURES, LABELS
import os

np.random.seed(42)  # Fixed seed - reproducible results

def generate_class(label_id, label_name, n=3000):
    ranges = FEATURE_RANGES[label_name]
    data = {}

    for feature in FEATURES:
        low, high = ranges[feature]

        if feature == 'PDR':
            # PDR is a ratio - use beta distribution for realism
            vals = np.random.uniform(low, high, n)
            vals = np.clip(vals, 0.0, 1.0)
        elif feature in ['RSSI', 'SNR', 'Noise_Power']:
            # Add realistic Gaussian noise to dB values
            center = (low + high) / 2
            spread = abs(high - low) / 4
            vals = np.random.normal(center, spread, n)
            vals = np.clip(vals, min(low,high), max(low,high))
        elif feature == 'Packet_Loss':
            vals = np.random.uniform(low, high, n)
            vals = np.clip(vals, 0.0, 1.0)
        else:
            vals = np.random.uniform(low, high, n)

        data[feature] = np.round(vals, 4)

    data['Label'] = label_id
    data['Label_Name'] = label_name
    return pd.DataFrame(data)

print("Generating synthetic RF Jamming dataset...")
print("=" * 50)

# Generate all 3 classes
df_normal = generate_class(0, 'Normal', 3000)
df_weak   = generate_class(1, 'Weak_Jamming', 3000)
df_strong = generate_class(2, 'Strong_Jamming', 3000)

print(f"Normal samples:       {len(df_normal)}")
print(f"Weak Jamming samples: {len(df_weak)}")
print(f"Strong Jamming samples: {len(df_strong)}")

# Combine and shuffle
df = pd.concat([df_normal, df_weak, df_strong], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

print(f"\nTotal dataset size: {len(df)} rows")
print(f"Features: {FEATURES}")
print(f"\nClass distribution:")
print(df['Label_Name'].value_counts())

print(f"\nDataset statistics:")
print(df[FEATURES].describe().round(3))

# Save to data folder
output_path = os.path.join('..', 'data', 'dataset.csv')
df.to_csv(output_path, index=False)
print(f"\nDataset saved to: {output_path}")

# Quick validation
df_check = pd.read_csv(output_path)
print(f"Validation - rows: {len(df_check)}, cols: {len(df_check.columns)}")
print("Day 5 Complete - dataset.csv ready!")
