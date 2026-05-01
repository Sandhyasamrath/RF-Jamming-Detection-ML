"""
Day 10 - Predictor Module
Loads trained model and runs inference on live input
"""

import joblib
import numpy as np
import pandas as pd
import os

# Feature order must match training
FEATURE_COLS = [
    "RSSI", "SNR", "PDR", "Packet_Loss",
    "Noise_Power", "FFT_Mean", "FFT_Variance", "Peak_Frequency",
    "RSSI_MA5", "SNR_MA5", "PDR_MA5",
    "FFT_Energy_Ratio", "Signal_Quality_Index",
    "RSSI_ZScore", "SNR_ZScore", "FFT_Mean_ZScore"
]

LABELS = {0: "Normal", 1: "Weak_Jamming", 2: "Strong_Jamming"}
ALERT_LEVELS = {0: "GREEN", 1: "YELLOW", 2: "RED"}

class JammingPredictor:
    def __init__(self):
        models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
        self.model = joblib.load(os.path.join(models_dir, "trained_model.pkl"))
        print(f"Model loaded: {type(self.model).__name__}")

    def engineer_features(self, raw_input):
        """
        Takes 8 raw features, computes the 8 engineered ones.
        For single-sample inference we approximate moving averages with current values
        and use a fixed reference for z-score normalization.
        """
        rssi = raw_input["RSSI"]
        snr  = raw_input["SNR"]
        pdr  = raw_input["PDR"]
        packet_loss = raw_input["Packet_Loss"]
        noise_power = raw_input["Noise_Power"]
        fft_mean = raw_input["FFT_Mean"]
        fft_var  = raw_input["FFT_Variance"]
        peak_freq = raw_input["Peak_Frequency"]

        # Moving averages = current value (single sample)
        rssi_ma5 = rssi
        snr_ma5  = snr
        pdr_ma5  = pdr

        # FFT energy ratio
        fft_energy_ratio = fft_mean / (fft_var + 1e-6)

        # Signal Quality Index (using approximate reference values)
        sqi = (rssi / -100.0) * 0.4 + (snr / 40.0) * 0.4 + pdr * 0.2

        # Z-scores using training set means/stds (approximate)
        rssi_zscore = (rssi - (-75)) / 8
        snr_zscore  = (snr - 18) / 5
        fft_mean_zscore = (fft_mean - 0.4) / 0.2

        return [rssi, snr, pdr, packet_loss, noise_power,
                fft_mean, fft_var, peak_freq,
                rssi_ma5, snr_ma5, pdr_ma5,
                fft_energy_ratio, sqi,
                rssi_zscore, snr_zscore, fft_mean_zscore]

    def predict(self, raw_input):
        """
        raw_input: dict with 8 keys (RSSI, SNR, PDR, ...)
        Returns: dict with prediction, confidence, alert_level
        """
        features = self.engineer_features(raw_input)
        features_df = pd.DataFrame([features], columns=FEATURE_COLS)

        prediction = int(self.model.predict(features_df)[0])
        probabilities = self.model.predict_proba(features_df)[0]
        confidence = float(probabilities[prediction])

        return {
            "prediction": prediction,
            "label": LABELS[prediction],
            "alert_level": ALERT_LEVELS[prediction],
            "confidence": round(confidence, 4),
            "probabilities": {
                "Normal": round(float(probabilities[0]), 4),
                "Weak_Jamming": round(float(probabilities[1]), 4),
                "Strong_Jamming": round(float(probabilities[2]), 4)
            }
        }

if __name__ == "__main__":
    p = JammingPredictor()
    
    test_normal = {
        "RSSI": -60, "SNR": 30, "PDR": 0.95, "Packet_Loss": 0.05,
        "Noise_Power": -95, "FFT_Mean": 0.2, "FFT_Variance": 0.02,
        "Peak_Frequency": 2412
    }
    test_strong = {
        "RSSI": -90, "SNR": 5, "PDR": 0.30, "Packet_Loss": 0.70,
        "Noise_Power": -75, "FFT_Mean": 0.8, "FFT_Variance": 0.25,
        "Peak_Frequency": 2470
    }
    
    print("\n--- Test: Normal ---")
    print(p.predict(test_normal))
    print("\n--- Test: Strong Jamming ---")
    print(p.predict(test_strong))
