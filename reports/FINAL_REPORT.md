# ML-Based RF Jamming Detection System
## Final Project Report

**Author:** Sandhya Samrath  
**Date:** May 2026  
**Repository:** https://github.com/Sandhyasamrath/RF-Jamming-Detection-ML

---

## ABSTRACT

Wireless communication systems are vulnerable to RF jamming attacks that flood legitimate signals with interference, causing service disruption and data loss. This project implements a real-time machine learning system that detects three classes of RF environment — Normal, Weak Jamming, and Strong Jamming — using 8 PHY-layer and spectral features. A Random Forest classifier achieves 100% accuracy on a synthetic dataset of 9,000 samples, with rigorous robustness validation including 5-fold cross-validation (F1 = 1.000 ± 0.000), label shuffle leakage testing (F1 collapses to 0.329, near chance baseline), and distribution shift testing (worst-case F1 = 0.9917). The system is deployed as a Flask REST API serving a JavaFX dashboard with live LineCharts and color-coded GREEN/YELLOW/RED alerts, achieving sub-60ms inference latency at 17 requests per second.

---

## 1. INTRODUCTION

### 1.1 Motivation
Radio Frequency jamming is one of the most disruptive cyber-physical attacks on wireless networks. With 5G/6G adoption and IoT proliferation, real-time detection has become critical for network reliability.

### 1.2 Problem Statement
Existing detection systems either require specialized RF hardware, focus only on binary classification, or lack a visual real-time monitoring interface. This project addresses these gaps by combining PHY-layer metrics, network-layer indicators, and spectral features into a 3-class classification system with a live JavaFX dashboard.

### 1.3 Objectives
- Train and compare 3 ML models (RF, KNN, SVM) on engineered RF features
- Validate robustness against overfitting and data leakage
- Build a real-time Flask prediction API with sub-100ms latency
- Develop a JavaFX dashboard with live charts and color-coded alerts
- Integrate the dashboard with the API for end-to-end real-time detection

---

## 2. LITERATURE REVIEW

| Paper | Features Used | Model | Accuracy | Limitation |
|---|---|---|---|---|
| SAJD (O-RAN) | RSSI, SNR | Adaptive ML | >95% | Needs O-RAN infra |
| JamShield | Hybrid time+spectral | Multi-class | Best F1 | OTA hardware required |
| RF Spectral Dataset | FFT Mean, RSSI | ML classifier | ~97% | Lab environment only |
| RF on PHY metrics | RSSI, SNR, CBR, PDR | Random Forest | High precision | Binary only |
| Novel RF vs DT | RF signal metrics | Random Forest | 99.3% | Single dataset |

### Research Gap
No existing work combines PHY + network + spectral features in a 3-class labelling scheme with a live monitoring dashboard. This project fills that gap.

---

## 3. METHODOLOGY

### 3.1 Feature Selection (8 features)
RSSI, SNR, PDR, Packet Loss, Noise Power, FFT Mean, FFT Variance, Peak Frequency

### 3.2 Synthetic Dataset
9,000 samples, 3,000 per class, generated using Gaussian distributions with non-overlapping ranges grounded in literature.

### 3.3 Feature Engineering
8 engineered features added: moving averages (window=5), rolling variance, z-score normalization, FFT energy ratio, Signal Quality Index. Final feature space: 16 dimensions.

### 3.4 Model Training
80/20 stratified train-test split with random_state=42. Three models trained:
- Random Forest (n_estimators=100)
- K-Nearest Neighbors (k=5)
- Support Vector Machine (RBF kernel, with StandardScaler)

### 3.5 System Architecture
JavaFX Dashboard sends RF feature vectors via HTTP POST every 1 second to Flask API on port 5000. Sliding-window LineCharts display last 30 data points. Color-coded alerts: GREEN/YELLOW/RED.

---

## 4. RESULTS

### 4.1 Baseline Performance
All three models achieve 100% accuracy. Random Forest selected for deployment.

### 4.2 Robustness Validation
- 5-Fold CV: F1 = 1.000 ± 0.000
- Noise σ=0.20: F1 = 0.9911
- Label Shuffle: F1 = 0.3289 (chance baseline)
- Distribution Shift average: F1 = 0.9966

### 4.3 Top Feature Importance
1. Packet Loss (22.1%)
2. PDR (20.6%)
3. FFT Variance (11.3%)
4. SNR (11.3%)
5. Noise Power (10.1%)

### 4.4 System Performance
- Inference latency: 30-60ms per prediction
- Throughput: 16.9 req/sec
- Success rate: 100/100 stress test requests

---

## 5. CONCLUSION

The project successfully delivered a real-time RF jamming detection system combining rigorous ML validation with a professional GUI. Random Forest emerged as the best deployment model based on speed, interpretability, and feature importance support. Four-tier robustness validation confirmed the model genuinely learns feature-label relationships and does not suffer from data leakage.

### Future Work
- Validation on real RF hardware (USRP / GNU Radio)
- Mobile/edge deployment via TensorFlow Lite
- Adversarial robustness testing
- Integration with O-RAN xApp framework

---

## 6. REFERENCES

1. SAJD: O-RAN Adaptive Jamming Detection — IEEE 2024
2. JamShield: Hybrid Feature Classification — IEEE 2023
3. RF Jamming Spectral Dataset — IEEE 2024
4. Random Forest on PHY Metrics for Jamming Detection — IEEE 2023
5. Novel Random Forest vs Decision Tree Comparison — IEEE 2023

