"""
Day 9 (Bonus 2) - Distribution Shift Test
Simulates "different capture day" scenario by:
1. Training on standard distribution
2. Testing on shifted distributions (mean shift, scale shift, mixed)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
import json
import os

plots_dir = os.path.join("..", "plots")
os.makedirs(plots_dir, exist_ok=True)

df = pd.read_csv(os.path.join("..", "data", "processed_dataset.csv"))

FEATURE_COLS = [
    "RSSI", "SNR", "PDR", "Packet_Loss",
    "Noise_Power", "FFT_Mean", "FFT_Variance", "Peak_Frequency",
    "RSSI_MA5", "SNR_MA5", "PDR_MA5",
    "FFT_Energy_Ratio", "Signal_Quality_Index",
    "RSSI_ZScore", "SNR_ZScore", "FFT_Mean_ZScore"
]

X = df[FEATURE_COLS].values
y = df["Label"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("=" * 60)
print("Day 9 BONUS 2 - Distribution Shift Test")
print("=" * 60)
print("Simulating: train on Day 1 capture, test on Day 2 capture")
print()

# Train baseline model
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

results = {}

# ─── Baseline (no shift) ───
y_pred = model.predict(X_test)
baseline_f1 = f1_score(y_test, y_pred, average="macro")
print(f"[Baseline]            F1 = {baseline_f1:.4f}")
results["baseline"] = round(baseline_f1, 4)

# ─── Test 1: Mean Shift (sensor calibration drift) ───
feature_means = X_train.mean(axis=0)
shift = feature_means * 0.05  # 5% systematic offset
X_test_meanshift = X_test + shift
y_pred = model.predict(X_test_meanshift)
mean_shift_f1 = f1_score(y_test, y_pred, average="macro")
print(f"[Mean Shift +5%]      F1 = {mean_shift_f1:.4f}  (sensor calibration drift)")
results["mean_shift_5pct"] = round(mean_shift_f1, 4)

# ─── Test 2: Scale Shift (gain change) ───
X_test_scaleshift = X_test * 1.10  # 10% scale change
y_pred = model.predict(X_test_scaleshift)
scale_shift_f1 = f1_score(y_test, y_pred, average="macro")
print(f"[Scale Shift +10%]    F1 = {scale_shift_f1:.4f}  (gain/amplifier change)")
results["scale_shift_10pct"] = round(scale_shift_f1, 4)

# ─── Test 3: Heavy noise (different environment) ───
np.random.seed(99)
heavy_noise = np.random.normal(0, 0.15, X_test.shape) * X_train.std(axis=0)
X_test_heavy = X_test + heavy_noise
y_pred = model.predict(X_test_heavy)
heavy_noise_f1 = f1_score(y_test, y_pred, average="macro")
print(f"[Heavy Noise 15%]     F1 = {heavy_noise_f1:.4f}  (different environment)")
results["heavy_noise_15pct"] = round(heavy_noise_f1, 4)

# ─── Test 4: Combined shift (worst case) ───
X_test_combined = (X_test + shift) * 1.05 + heavy_noise * 0.5
y_pred = model.predict(X_test_combined)
combined_f1 = f1_score(y_test, y_pred, average="macro")
print(f"[Combined Shift]      F1 = {combined_f1:.4f}  (worst case - all shifts)")
results["combined_shift"] = round(combined_f1, 4)

# ─── Plot ───
labels = ["Baseline", "Mean+5%", "Scale+10%", "Noise+15%", "Combined"]
scores = [baseline_f1, mean_shift_f1, scale_shift_f1, heavy_noise_f1, combined_f1]

fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#4CAF50", "#2196F3", "#FF9800", "#9C27B0", "#F44336"]
bars = ax.bar(labels, scores, color=colors, width=0.6)
ax.set_ylim(0.5, 1.05)
ax.set_ylabel("F1 Score (macro)", fontsize=11)
ax.set_title("Distribution Shift Robustness Test\n(Random Forest)",
             fontweight="bold", fontsize=13)
ax.axhline(y=0.95, color="green", linestyle="--", alpha=0.5, label="95% threshold")
ax.grid(alpha=0.3, axis="y")
ax.legend()
for bar, score in zip(bars, scores):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
            f"{score:.3f}", ha="center", fontweight="bold")
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "distribution_shift.png"), dpi=150)
plt.close()

print()
print("=" * 60)
print("  DISTRIBUTION SHIFT SUMMARY")
print("=" * 60)
print(f"  Average F1 across all shifts: {np.mean(scores):.4f}")
print(f"  Worst case F1:                {min(scores):.4f}")

if min(scores) > 0.85:
    print()
    print("  VERDICT: Excellent generalization across distribution shifts")
    print("  Model handles sensor drift, gain change, and noise gracefully")
elif min(scores) > 0.70:
    print()
    print("  VERDICT: Acceptable generalization - some degradation expected")
else:
    print()
    print("  VERDICT: Model is sensitive to distribution shift")

with open(os.path.join("..", "models", "distribution_shift.json"), "w") as f:
    json.dump(results, f, indent=2)

print()
print("Saved -> plots/distribution_shift.png")
print("Saved -> models/distribution_shift.json")
print("Done!")
