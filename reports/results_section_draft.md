# Results and Robustness Validation
*RF Jamming Detection System — Section for Final Report*

## 1. Baseline Performance

The proposed system was evaluated using a synthetic dataset of 9,000 samples
distributed equally across three classes: Normal, Weak Jamming, and Strong
Jamming. Sixteen features were used for classification, comprising eight
original radio metrics and eight engineered features including moving averages,
z-score normalization, FFT energy ratio, and a composite Signal Quality Index.

Three machine learning algorithms — Random Forest, K-Nearest Neighbors, and
Support Vector Machine — were trained on an 80/20 stratified train-test split
with random_state=42 for reproducibility. All three models achieved perfect
classification on the held-out test set.

**Table 1: Baseline Model Performance Comparison**

| Model | Accuracy | Precision | Recall | F1-Score |
|---|---|---|---|---|
| Random Forest | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| K-Nearest Neighbors | 1.0000 | 1.0000 | 1.0000 | 1.0000 |
| Support Vector Machine | 1.0000 | 1.0000 | 1.0000 | 1.0000 |

Random Forest was selected as the deployment model due to feature importance
scoring, faster inference, and superior interpretability. Feature importance
analysis identified Packet_Loss (22.1%), PDR (20.6%), FFT_Variance (11.3%),
SNR (11.3%), and Noise_Power (10.1%) as the five most discriminative features.

## 2. Robustness Validation

To rule out data leakage or memorization, four-tier robustness validation
was performed.

### 2.1 Stratified K-Fold Cross-Validation
Five-fold stratified CV yielded a mean macro-F1 of 1.0000 with a standard
deviation of 0.0000, indicating performance is not split-dependent.

### 2.2 Noise Perturbation Test
Additive Gaussian noise scaled to feature standard deviation was applied at
sigma values of 0.01 to 0.20. The model maintained macro-F1 of 0.9911 even
at sigma = 0.20, demonstrating a broad decision boundary.

### 2.3 Label Shuffle Leakage Test
Training labels were randomly permuted and the model retrained. Macro-F1
collapsed to 0.3289, statistically indistinguishable from the chance baseline
of 0.333 for a balanced three-class problem. This proves the model genuinely
learns the feature-label mapping and rules out leakage.

### 2.4 Distribution Shift Test

**Table 2: Distribution Shift Robustness**

| Test Scenario | Macro-F1 | Real-World Equivalent |
|---|---|---|
| Baseline (no shift) | 1.0000 | Same-session evaluation |
| Mean Shift (+5%) | 0.9994 | Sensor calibration drift |
| Scale Shift (+10%) | 0.9967 | Amplifier gain variation |
| Heavy Noise (sigma=0.15) | 0.9917 | Different environment |
| Combined Shift | 0.9950 | Worst-case multi-factor drift |
| **Average across shifts** | **0.9966** | — |

Worst-case macro-F1 of 0.9917 demonstrates robustness to realistic deployment
variations.

## 3. Discussion

The combined evidence — CV stability (std = 0.0000), graceful noise degradation
(F1 = 0.9911 at 20% perturbation), collapse to chance under label shuffling
(F1 = 0.3289), and high performance under distribution shift (worst-case
F1 = 0.9917) — supports the conclusion that perfect baseline accuracy reflects
clean separability of the engineered feature space, not data leakage.

Real-world performance is expected in the 0.95–0.99 macro-F1 range, consistent
with the 97% accuracy reported in the RF Spectral paper and 99.3% reported in
the Novel RF vs Decision Tree study.

## Summary Statement

> The RF jamming detector achieved near-perfect macro-F1 under standard
> evaluation, maintained >0.99 macro-F1 under multiple synthetic distribution
> shifts, and dropped to chance level under label shuffling — indicating
> robust learning with no evidence of data leakage or overfitting.
