"""
Feature definitions for RF Jamming Detection System
Day 3 - Feature Locking (FROZEN - do not modify after Day 3)
"""

# Final locked feature list
FEATURES = [
    'RSSI',           # Received Signal Strength Indicator (dBm)
    'SNR',            # Signal-to-Noise Ratio (dB)
    'PDR',            # Packet Delivery Ratio (0.0 - 1.0)
    'Packet_Loss',    # Packet Loss Rate (0.0 - 1.0)
    'Noise_Power',    # Background Noise Power (dBm)
    'FFT_Mean',       # Mean FFT Spectral Magnitude
    'FFT_Variance',   # Variance of FFT Spectral Magnitude
    'Peak_Frequency'  # Dominant Peak Frequency (MHz)
]

# Target labels
LABELS = {
    0: 'Normal',
    1: 'Weak_Jamming',
    2: 'Strong_Jamming'
}

# Value ranges per class (used for synthetic data generation - Day 5)
FEATURE_RANGES = {
    'Normal': {
        'RSSI': (-40, -70),
        'SNR': (20, 40),
        'PDR': (0.90, 1.0),
        'Packet_Loss': (0.0, 0.10),
        'Noise_Power': (-100, -95),
        'FFT_Mean': (0.1, 0.3),
        'FFT_Variance': (0.01, 0.05),
        'Peak_Frequency': (2400, 2420)
    },
    'Weak_Jamming': {
        'RSSI': (-70, -85),
        'SNR': (10, 20),
        'PDR': (0.60, 0.90),
        'Packet_Loss': (0.10, 0.40),
        'Noise_Power': (-95, -85),
        'FFT_Mean': (0.3, 0.6),
        'FFT_Variance': (0.05, 0.15),
        'Peak_Frequency': (2420, 2450)
    },
    'Strong_Jamming': {
        'RSSI': (-85, -100),
        'SNR': (0, 10),
        'PDR': (0.0, 0.60),
        'Packet_Loss': (0.40, 1.0),
        'Noise_Power': (-85, -70),
        'FFT_Mean': (0.6, 1.0),
        'FFT_Variance': (0.15, 0.40),
        'Peak_Frequency': (2450, 2500)
    }
}

def get_feature_count():
    return len(FEATURES)

def get_label_names():
    return list(LABELS.values())

if __name__ == '__main__':
    print("=== RF Jamming Detection - Locked Features ===")
    for i, f in enumerate(FEATURES, 1):
        print(f"F{i}: {f}")
    print(f"\nTotal features: {get_feature_count()}")
    print(f"Labels: {get_label_names()}")
    print("\nFeature ranges saved - ready for Day 5 dataset generation")
