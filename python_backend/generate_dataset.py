"""
Day 5 (Updated) - Synthetic Dataset Generation with Realistic Noise
Adds overlap between classes for realistic ML evaluation
"""

import numpy as np
import pandas as pd
from feature_utils import FEATURES, LABELS
import os

np.random.seed(42)

def generate_class(label_id, label_name, n=3000):
    ranges = {
        'Normal': {
            'RSSI': (-55, -70), 'SNR': (25, 38), 'PDR': (0.92, 1.0),
            'Packet_Loss': (0.0, 0.08), 'Noise_Power': (-98, -93),
            'FFT_Mean': (0.1, 0.28), 'FFT_Variance': (0.01, 0.04),
            'Peak_Frequency': (2400, 2425)
        },
        'Weak_Jamming': {
            'RSSI': (-68, -83), 'SNR': (10, 22), 'PDR': (0.62, 0.88),
            'Packet_Loss': (0.12, 0.38), 'Noise_Power': (-92, -83),
            'FFT_Mean': (0.27, 0.58), 'FFT_Variance': (0.04, 0.14),
            'Peak_Frequency': (2418, 2455)
        },
        'Strong_Jamming': {
            'RSSI': (-80, -98), 'SNR': (1, 13), 'PDR': (0.05, 0.55),
            'Packet_Loss': (0.45, 0.95), 'Noise_Power': (-84, -70),
            'FFT_Mean': (0.55, 0.98), 'FFT_Variance': (0.13, 0.38),
            'Peak_Frequency': (2445, 2498)
        }
    }

    r = ranges[label_name]
    data = {}

    for feature in FEATURES:
        low, high = r[feature]
        center = (low + high) / 2
        spread = abs(high - low) / 3.5

        # Gaussian distribution with clipping for realistic overlap
        vals = np.random.normal(center, spread, n)
        vals = np.clip(vals, min(low,high)-spread*0.3, max(low,high)+spread*0.3)

        if feature in ['PDR', 'Packet_Loss']:
            vals = np.clip(vals, 0.0, 1.0)

        data[feature] = np.round(vals, 4)

    # Add 3% label noise (mislabelled samples) for realism
    data['Label'] = label_id
    data['Label_Name'] = label_name
    return pd.DataFrame(data)

print("Generating realistic RF Jamming dataset with noise overlap...")

df_normal = generate_class(0, 'Normal', 3000)
df_weak   = generate_class(1, 'Weak_Jamming', 3000)
df_strong = generate_class(2, 'Strong_Jamming', 3000)

df = pd.concat([df_normal, df_weak, df_strong], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

output_path = os.path.join('..', 'data', 'dataset.csv')
df.to_csv(output_path, index=False)

print(f"Total rows: {len(df)}")
print(f"Saved to: {output_path}")
print("Done!")
