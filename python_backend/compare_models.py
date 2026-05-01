"""
Day 8 - SVM Training + Full 3-Model Comparison
RF Jamming Detection System
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (accuracy_score, precision_score,
                             recall_score, f1_score, classification_report)
import joblib
import json
import os

# ── Load data ─────────────────────────────────────────────────
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

# Same split as Day 7 - fair comparison
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# SVM needs scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

print("=" * 55)
print("Day 8 - SVM + Full Model Comparison")
print("=" * 55)

# ── Load Day 7 models ─────────────────────────────────────────
rf_model  = joblib.load(os.path.join('..', 'models', 'rf_model.pkl'))
knn_model = joblib.load(os.path.join('..', 'models', 'knn_model.pkl'))

# ── Train SVM ─────────────────────────────────────────────────
print("\nTraining SVM (RBF kernel)... this may take 1-2 minutes")
svm_model = SVC(kernel='rbf', C=10, gamma='scale', random_state=42)
svm_model.fit(X_train_scaled, y_train)
print("SVM training complete!")

# ── Evaluate all 3 models ─────────────────────────────────────
def get_metrics(model, X, y_true, scaled=False):
    if scaled:
        y_pred = model.predict(X_test_scaled)
    else:
        y_pred = model.predict(X_test)
    return {
        'accuracy':  round(accuracy_score(y_true, y_pred), 4),
        'precision': round(precision_score(y_true, y_pred, average='weighted'), 4),
        'recall':    round(recall_score(y_true, y_pred, average='weighted'), 4),
        'f1_score':  round(f1_score(y_true, y_pred, average='weighted'), 4),
        'y_pred':    y_pred
    }

rf_m   = get_metrics(rf_model,  X_test, y_test, scaled=False)
knn_m  = get_metrics(knn_model, X_test, y_test, scaled=False)
svm_m  = get_metrics(svm_model, X_test, y_test, scaled=True)

# ── Print classification reports ──────────────────────────────
for name, m in [("Random Forest", rf_m), ("KNN", knn_m), ("SVM", svm_m)]:
    print(f"\n=== {name} ===")
    print(f"Accuracy : {m['accuracy']*100:.2f}%")
    print(f"Precision: {m['precision']:.4f}")
    print(f"Recall   : {m['recall']:.4f}")
    print(f"F1 Score : {m['f1_score']:.4f}")

# ── Final Comparison Table ────────────────────────────────────
print("\n" + "=" * 60)
print("  FINAL MODEL COMPARISON TABLE")
print("=" * 60)
print(f"  {'Metric':<12} {'Random Forest':>15} {'KNN':>10} {'SVM':>10}")
print(f"  {'─'*50}")
for metric in ['accuracy', 'precision', 'recall', 'f1_score']:
    print(f"  {metric:<12} {rf_m[metric]:>15.4f} {knn_m[metric]:>10.4f} {svm_m[metric]:>10.4f}")

# ── Select best model ─────────────────────────────────────────
scores = {
    'Random_Forest': rf_m['f1_score'],
    'KNN':           knn_m['f1_score'],
    'SVM':           svm_m['f1_score']
}
best_name = max(scores, key=scores.get)
print(f"\n  Best Model: {best_name} (F1 = {scores[best_name]:.4f})")

# ── Save SVM + scaler ─────────────────────────────────────────
joblib.dump(svm_model, os.path.join('..', 'models', 'svm_model.pkl'))
joblib.dump(scaler,    os.path.join('..', 'models', 'scaler.pkl'))

# ── Save best model as trained_model.pkl ─────────────────────
best_models = {
    'Random_Forest': rf_model,
    'KNN': knn_model,
    'SVM': svm_model
}
joblib.dump(best_models[best_name],
            os.path.join('..', 'models', 'trained_model.pkl'))

# ── Update metrics JSON ───────────────────────────────────────
all_metrics = {
    'Random_Forest': {k: rf_m[k]  for k in ['accuracy','precision','recall','f1_score']},
    'KNN':           {k: knn_m[k] for k in ['accuracy','precision','recall','f1_score']},
    'SVM':           {k: svm_m[k] for k in ['accuracy','precision','recall','f1_score']},
    'best_model':    best_name
}
with open(os.path.join('..', 'models', 'model_metrics.json'), 'w') as f:
    json.dump(all_metrics, f, indent=2)

print(f"\n  Saved: svm_model.pkl, scaler.pkl")
print(f"  Saved: trained_model.pkl ({best_name})")
print(f"  Saved: model_metrics.json (updated)")
print("\nDay 8 Complete!")
