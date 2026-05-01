import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import joblib
import json
import os

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

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))

def evaluate(name, model):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted')
    rec  = recall_score(y_test, y_pred, average='weighted')
    f1   = f1_score(y_test, y_pred, average='weighted')
    print(f"\n=== {name} ===")
    print(f"Accuracy : {acc*100:.2f}%")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1 Score : {f1:.4f}")
    print(classification_report(y_test, y_pred, target_names=['Normal','Weak_Jam','Strong_Jam']))
    return model, {'accuracy': round(acc,4), 'precision': round(prec,4), 'recall': round(rec,4), 'f1_score': round(f1,4)}

rf_model, rf_metrics  = evaluate("Random Forest", RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1))
knn_model, knn_metrics = evaluate("KNN (K=5)", KNeighborsClassifier(n_neighbors=5))

os.makedirs(os.path.join('..', 'models'), exist_ok=True)
joblib.dump(rf_model,  os.path.join('..', 'models', 'rf_model.pkl'))
joblib.dump(knn_model, os.path.join('..', 'models', 'knn_model.pkl'))

split_info = {'feature_cols': FEATURE_COLS, 'test_size': 0.2, 'random_state': 42}
with open(os.path.join('..', 'models', 'split_info.json'), 'w') as f:
    json.dump(split_info, f, indent=2)

metrics = {'Random_Forest': rf_metrics, 'KNN': knn_metrics}
with open(os.path.join('..', 'models', 'model_metrics.json'), 'w') as f:
    json.dump(metrics, f, indent=2)

print("\n=== COMPARISON ===")
print(f"{'Metric':<12} {'Random Forest':>15} {'KNN':>10}")
for m in ['accuracy','precision','recall','f1_score']:
    print(f"{m:<12} {rf_metrics[m]:>15.4f} {knn_metrics[m]:>10.4f}")
print("\nDay 7 Complete! Models saved.")
