"""
Day 9 - Model Evaluation
RF Jamming Detection System
Generates: Confusion Matrix, Classification Report, Feature Importance Plot
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import (confusion_matrix, classification_report,
                             ConfusionMatrixDisplay)
import joblib
import os

# ── Setup ─────────────────────────────────────────────────────
plots_dir = os.path.join('..', 'plots')
os.makedirs(plots_dir, exist_ok=True)

df = pd.read_csv(os.path.join('..', 'data', 'processed_dataset.csv'))

FEATURE_COLS = [
    'RSSI', 'SNR', 'PDR', 'Packet_Loss',
    'Noise_Power', 'FFT_Mean', 'FFT_Variance', 'Peak_Frequency',
    'RSSI_MA5', 'SNR_MA5', 'PDR_MA5',
    'FFT_Energy_Ratio', 'Signal_Quality_Index',
    'RSSI_ZScore', 'SNR_ZScore', 'FFT_Mean_ZScore'
]

X = df[FEATURE_COLS]
y = df['Label']
CLASS_NAMES = ['Normal', 'Weak_Jam', 'Strong_Jam']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Load best model (Random Forest)
model = joblib.load(os.path.join('..', 'models', 'trained_model.pkl'))
y_pred = model.predict(X_test)

print("=" * 55)
print("Day 9 - Model Evaluation")
print("=" * 55)

# ── 1. Classification Report ──────────────────────────────────
print("\n=== Classification Report ===")
report = classification_report(y_test, y_pred, target_names=CLASS_NAMES)
print(report)

# Save report to file
with open(os.path.join(plots_dir, 'classification_report.txt'), 'w') as f:
    f.write("RF Jamming Detection - Classification Report\n")
    f.write("=" * 50 + "\n")
    f.write(report)
print("Classification report saved.")

# ── 2. Confusion Matrix ───────────────────────────────────────
print("\nGenerating Confusion Matrix...")
cm = confusion_matrix(y_test, y_pred)

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=CLASS_NAMES,
            yticklabels=CLASS_NAMES,
            linewidths=0.5, linecolor='gray')
ax.set_title('RF Jamming Detection — Confusion Matrix\n(Random Forest)', 
             fontsize=14, fontweight='bold', pad=15)
ax.set_ylabel('Actual Label', fontsize=12)
ax.set_xlabel('Predicted Label', fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'confusion_matrix.png'), dpi=150)
plt.close()
print("Confusion matrix saved → plots/confusion_matrix.png")

# ── 3. Feature Importance Plot ────────────────────────────────
print("\nGenerating Feature Importance Plot...")
importances = model.feature_importances_
indices = np.argsort(importances)[::-1]

fig, ax = plt.subplots(figsize=(12, 6))
colors = ['#2196F3' if i < 8 else '#4CAF50' for i in range(len(FEATURE_COLS))]
bars = ax.bar(range(len(FEATURE_COLS)),
              importances[indices],
              color=[colors[i] for i in indices])
ax.set_xticks(range(len(FEATURE_COLS)))
ax.set_xticklabels([FEATURE_COLS[i] for i in indices],
                   rotation=45, ha='right', fontsize=9)
ax.set_title('Feature Importance — Random Forest\n(Blue=Original, Green=Engineered)',
             fontsize=13, fontweight='bold')
ax.set_ylabel('Importance Score')
ax.set_xlabel('Features')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'feature_importance.png'), dpi=150)
plt.close()
print("Feature importance saved → plots/feature_importance.png")

# ── 4. Model Accuracy Bar Chart ───────────────────────────────
print("\nGenerating Model Comparison Chart...")
models_list  = ['Random Forest', 'KNN', 'SVM']
accuracies   = [100.0, 100.0, 100.0]
f1_scores    = [1.0, 1.0, 1.0]

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Accuracy chart
bars1 = axes[0].bar(models_list, accuracies,
                    color=['#2196F3','#4CAF50','#FF9800'], width=0.5)
axes[0].set_ylim(95, 101)
axes[0].set_title('Model Accuracy Comparison', fontweight='bold')
axes[0].set_ylabel('Accuracy (%)')
for bar, val in zip(bars1, accuracies):
    axes[0].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.05,
                 f'{val:.1f}%', ha='center', fontweight='bold')

# F1 Score chart
bars2 = axes[1].bar(models_list, f1_scores,
                    color=['#2196F3','#4CAF50','#FF9800'], width=0.5)
axes[1].set_ylim(0.95, 1.01)
axes[1].set_title('Model F1 Score Comparison', fontweight='bold')
axes[1].set_ylabel('F1 Score')
for bar, val in zip(bars2, f1_scores):
    axes[1].text(bar.get_x() + bar.get_width()/2,
                 bar.get_height() + 0.001,
                 f'{val:.4f}', ha='center', fontweight='bold')

plt.suptitle('RF Jamming Detection — Model Comparison', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(plots_dir, 'model_comparison.png'), dpi=150)
plt.close()
print("Model comparison chart saved → plots/model_comparison.png")

# ── 5. Print top features ─────────────────────────────────────
print("\n=== Top 5 Most Important Features ===")
for i in range(5):
    print(f"  {i+1}. {FEATURE_COLS[indices[i]]:<25} {importances[indices[i]]:.4f}")

print("\n=== Files Generated ===")
for f in ['confusion_matrix.png', 'feature_importance.png',
          'model_comparison.png', 'classification_report.txt']:
    path = os.path.join(plots_dir, f)
    size = os.path.getsize(path)
    print(f"  {f} ({size/1024:.1f} KB)")

print("\nDay 9 Complete! All evaluation plots ready.")
