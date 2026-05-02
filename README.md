# 🛡️ ML-Based RF Jamming Detection System

A real-time machine learning system that detects RF jamming attacks using PHY-layer and spectral features. Built with Python (Scikit-learn + Flask) for the ML backend and Java (JavaFX) for the live dashboard.

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)]()
[![Java](https://img.shields.io/badge/Java-21-orange.svg)]()
[![JavaFX](https://img.shields.io/badge/JavaFX-21-green.svg)]()

---

## 🎯 Project Overview

This system detects RF jamming attacks in real-time by analyzing 8 radio metrics — RSSI, SNR, PDR, Packet Loss, Noise Power, FFT Mean, FFT Variance, and Peak Frequency — and classifies them into three categories: **Normal**, **Weak Jamming**, or **Strong Jamming**.

### Key Achievements
- **100% accuracy** on synthetic dataset (validated against overfitting)
- **Sub-60ms inference latency** for real-time detection
- **17 requests/sec throughput** with 100% success rate under stress test
- **0.99+ F1 score** maintained even under 20% noise perturbation
- **Cross-validated and leakage-tested** at four levels

---

## 📊 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| **Random Forest** ⭐ | **1.0000** | **1.0000** | **1.0000** | **1.0000** |
| K-Nearest Neighbors | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Support Vector Machine | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

### Robustness Validation
- **5-Fold Cross-Validation:** F1 = 1.000 ± 0.000 (stable)
- **Noise Perturbation (σ=0.20):** F1 = 0.9911 (robust)
- **Label Shuffle Test:** F1 = 0.3289 (≈ chance, no leakage)
- **Distribution Shift Test:** F1 = 0.9966 average across all shifts

### Top Feature Importance
1. Packet Loss (22.1%)
2. PDR (20.6%)
3. FFT Variance (11.3%)
4. SNR (11.3%)
5. Noise Power (10.1%)

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| ML Models | Random Forest, KNN, SVM (Scikit-learn) |
| Backend API | Python 3.10, Flask, Flask-CORS |
| Frontend GUI | Java 21, JavaFX 21, Maven |
| HTTP Client | Jackson (JSON parsing) |
| Visualization | Matplotlib, Seaborn |
| Data Processing | Pandas, NumPy, SciPy |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+, Java 21 (OpenJDK), Maven 3.6+

### 1. Setup Python Backend
```bash
cd python_backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Train the Model (pre-trained models also included)
```bash
python generate_dataset.py
python feature_engineering.py
python train_models.py
python compare_models.py
python evaluate_model.py
```

### 3. Run Flask API
```bash
python app.py
```

### 4. Launch JavaFX Dashboard (separate terminal)
```bash
cd java_gui
mvn javafx:run
```

Click **Start Live Detection** — the dashboard cycles through Normal → Weak → Strong jamming with live ML predictions.

---

## 📚 Reference Papers

1. **SAJD** — O-RAN Adaptive Jamming Detection (>95% acc)
2. **JamShield** — Hybrid feature classification on OTA datasets
3. **RF Spectral Dataset** — ML on FFT/RSSI (~97% acc)
4. **RF on PHY metrics** — Random Forest on RSSI/SNR/CBR
5. **Novel RF vs DT** — RF achieves 99.3% accuracy

---

## 👤 Author

**Sandhya Samrath** — Final Year Project | 2026  
[GitHub](https://github.com/Sandhyasamrath)

