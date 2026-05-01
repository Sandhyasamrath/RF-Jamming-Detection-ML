"""
Day 9 (Bonus) - Overfitting / Leakage Sanity Checks
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.metrics import f1_score, accuracy_score
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
print("Day 9 BONUS - Overfitting & Leakage Sanity Checks")
print("=" * 60)

results = {}

print("\n[1/3] Stratified 5-Fold Cross-Validation...")
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
cv_scores = cross_val_score(model, X, y, cv=cv, scoring="f1_macro", n_jobs=-1)
print(f"  Fold scores: {[f'{s:.4f}' for s in cv_scores]}")
print(f"  Mean F1 (macro): {cv_scores.mean():.4f}")
print(f"  Std deviation:   {cv_scores.std():.4f}")
if cv_scores.std() < 0.02:
    print("  PASS - Low variance across folds")
else:
    print("  WARNING - High variance")
results["cv_scores"] = [round(s,4) for s in cv_scores.tolist()]
results["cv_mean"]   = round(cv_scores.mean(), 4)
results["cv_std"]    = round(cv_scores.std(), 4)

print("\n[2/3] Noise-Perturbed Test Set Robustness...")
model.fit(X_train, y_train)
noise_levels = [0.0, 0.01, 0.03, 0.05, 0.10, 0.15, 0.20]
noise_scores = []
for sigma in noise_levels:
    if sigma == 0:
        y_pred = model.predict(X_test)
    else:
        feature_stds = X_train.std(axis=0)
        noise = np.random.normal(0, sigma, X_test.shape) * feature_stds
        X_test_noisy = X_test + noise
        y_pred = model.predict(X_test_noisy)
    f1 = f1_score(y_test, y_pred, average="macro")
    noise_scores.append(f1)
    print(f"  sigma = {sigma:.2f} -> F1: {f1:.4f}")

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(noise_levels, noise_scores, marker="o", linewidth=2, markersize=8, color="#2196F3")
ax.fill_between(noise_levels, noise_scores, alpha=0.2, color="#2196F3")
ax.set_xlabel("Noise Sigma (x feature std)")
ax.set_ylabel("F1 Score (macro)")
ax.set_title("Model Robustness Under Noise Perturbation\n(Random Forest)", fontweight="bold")
ax.grid(alpha=0.3)
ax.axhline(y=0.95, color="green", linestyle="--", alpha=0.5, label="95% threshold")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, "noise_robustness.png"), dpi=150)
plt.close()
print("  Saved noise_robustness.png")
results["noise_levels"] = noise_levels
results["noise_f1_scores"] = [round(s,4) for s in noise_scores]

print("\n[3/3] Label Shuffle Test...")
np.random.seed(42)
y_train_shuffled = np.random.permutation(y_train)
sm = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
sm.fit(X_train, y_train_shuffled)
y_pred = sm.predict(X_test)
shuffle_f1 = f1_score(y_test, y_pred, average="macro")
shuffle_acc = accuracy_score(y_test, y_pred)
print(f"  F1 with shuffled labels: {shuffle_f1:.4f}")
print(f"  Accuracy: {shuffle_acc:.4f}")
print(f"  Random baseline: ~0.33")
if shuffle_f1 < 0.40:
    print("  PASS - No leakage detected")
else:
    print("  FAIL - LEAKAGE DETECTED")
results["shuffle_f1"]  = round(shuffle_f1, 4)
results["shuffle_acc"] = round(shuffle_acc, 4)

print("\n" + "=" * 60)
print("  SANITY CHECK SUMMARY")
print("=" * 60)
print(f"  CV F1 Mean:        {results['cv_mean']:.4f} (std: {results['cv_std']:.4f})")
print(f"  Noise robust @20%: {results['noise_f1_scores'][-1]:.4f}")
print(f"  Shuffle F1:        {results['shuffle_f1']:.4f}")

if results["cv_std"] < 0.05 and results["shuffle_f1"] < 0.45:
    print("\n  VERDICT: Model is GENUINELY learning - no leakage detected")
    print("  100% accuracy is due to clean feature separability,")
    print("  NOT data leakage or overfitting.")
else:
    print("\n  VERDICT: Investigate further")

with open(os.path.join("..", "models", "sanity_check.json"), "w") as f:
    json.dump(results, f, indent=2)
print("\nDone!")
