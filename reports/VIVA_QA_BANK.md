# Viva Question Bank — RF Jamming Detection Project

## TIER 1 — Most Likely Questions

### Q1: What is RF jamming and why does it matter?
RF jamming is a denial-of-service attack on wireless networks where an attacker transmits high-power interference signals to disrupt legitimate communications. With 5G/6G and IoT proliferation, real-time detection is critical for maintaining network reliability and security.

### Q2: Why did you choose 8 features specifically?
The features cover three layers of RF analysis. RSSI and SNR are PHY-layer indicators used in SAJD and Novel RF vs DT papers. PDR and Packet Loss capture network-layer degradation from JamShield. FFT Mean, Variance, and Peak Frequency come from the RF Spectral paper achieving ~97% accuracy. Noise Power provides early-warning detection. Together they cover PHY, network, and spectral dimensions of jamming.

### Q3: Why Random Forest over SVM and KNN?
All three models achieved 100% on the synthetic dataset, so I selected Random Forest based on three deployment criteria: it provides feature importance scores out of the box, runs faster than SVM at inference time (no scaling needed), and is more interpretable for real-world RF engineering teams.

### Q4: 100% accuracy seems suspicious. Did you check for overfitting?
Yes, I ran four levels of validation. Stratified 5-fold CV gives F1 of 1.000 with std 0.000 — confirming stability across splits. Noise perturbation at sigma=0.20 still gives F1 of 0.9911. Most importantly, the label shuffle test collapses F1 to 0.3289, exactly the chance baseline for 3 classes — proving no data leakage. Distribution shift testing maintains F1 above 0.99 even with combined sensor drift, gain change, and noise. The 100% reflects clean feature separability by design, not memorization.

### Q5: What is the architecture of your system?
It's a client-server architecture. The JavaFX dashboard generates RF feature vectors and sends them as JSON via HTTP POST to a Flask API on port 5000. Flask passes the input to a Predictor class which loads the trained Random Forest from a pickle file, runs inference in 30-60ms, and returns the prediction with confidence and class probabilities. The dashboard updates LineCharts and the color-coded alert panel based on the response.

### Q6: How does your dashboard work in real-time?
A JavaFX Timeline triggers every 1 second to send a prediction request. The HTTP call runs on a background thread to avoid freezing the UI. When the response arrives, Platform.runLater updates the charts and alert panel on the JavaFX Application Thread. Sliding-window logic keeps the last 30 data points visible. Total round-trip latency is under 100ms.

---

## TIER 2 — Technical Deep-Dive Questions

### Q7: Why didn't you use deep learning?
For 8 features with clearly separable ranges, deep learning is overkill. Random Forest gives equivalent accuracy with faster training, interpretable feature importance, and no GPU requirement. Deep learning would only be justified if I had raw IQ samples or large unstructured datasets.

### Q8: How would performance change with real-world data?
Real-world performance would likely be in the 0.95-0.99 F1 range, consistent with the 97% in the RF Spectral paper and 99.3% in the Novel RF vs DT paper. Real RF environments have multipath fading, channel hopping, and hardware noise that synthetic data cannot fully model. My distribution shift test simulates these conditions and the model maintains 0.9917 F1 in the worst case.

### Q9: What is the role of Z-score normalization?
Different features have wildly different scales — RSSI is in -100 to -50 dBm, PDR is 0 to 1, FFT Mean is roughly 0 to 1. Without normalization, models like KNN and SVM would be biased toward high-magnitude features. Z-score ensures all features contribute equally to the decision boundary.

### Q10: Explain FFT Energy Ratio.
FFT_Energy_Ratio = FFT_Mean / (FFT_Variance + epsilon). It captures the peak-to-spread relationship of the spectrum. A narrowband jammer concentrates energy at one frequency (high mean, low variance, high ratio). A broadband jammer spreads energy (lower ratio). This single feature distinguishes jamming styles.

### Q11: How does the API handle multiple concurrent requests?
Flask uses Werkzeug's threaded WSGI server, which handles concurrent requests in worker threads. My stress test of 100 sequential requests showed 17 req/sec throughput with 59ms average latency and 0% failures.

### Q12: What is the Signal Quality Index?
It's a composite score I engineered — 0.4 weighted RSSI normalized to its minimum + 0.4 weighted SNR normalized to its max + 0.2 PDR. It's a single 0-1 health score useful for the dashboard color logic and provides a high-level channel health interpretation for non-technical viewers.

---

## TIER 3 — Defense Questions

### Q13: What are the limitations?
Three main ones. First, the dataset is synthetic — real validation would need RF hardware captures. Second, the system uses 1-second window features; truly burst jammers below this granularity might be missed. Third, the dashboard simulates input rather than connecting to a real RF dongle — production deployment would need GNU Radio or USRP integration.

### Q14: How would you scale this to a fleet of 1000 sensors?
I would replace the Flask development server with Gunicorn + Nginx, add Redis as a request queue, and run multiple Flask workers behind a load balancer. Each sensor would publish to a message bus like Kafka, and a worker pool would consume and classify. Predictions would feed into a central dashboard via WebSockets instead of polling.

### Q15: Why three classes instead of binary?
Binary jamming detection is a solved problem. Three-class classification provides actionable severity information — the network can respond differently to weak interference (e.g. switch frequency) vs strong attack (e.g. trigger alert + switch protocol). My color-coded alert panel demonstrates this operational value.

### Q16: How is your project different from JamShield?
JamShield uses OTA hardware captures and binary classification. My project uses a synthetic dataset with 3-class severity labelling, adds network-layer features (PDR, Packet Loss), and provides a live JavaFX dashboard for visual monitoring — all of which JamShield does not.

---

## TIER 4 — Curveball Questions

### Q17: Walk me through what happens from button click to alert color change.
1. User clicks "Start Live Detection" in JavaFX
2. Timeline fires every 1 second
3. generateAndPredict() creates an 8-feature vector
4. New Thread spawns to call ApiClient.predict()
5. ApiClient builds JSON and POSTs to http://127.0.0.1:5000/predict
6. Flask predict() route receives the request
7. JammingPredictor.engineer_features() adds 8 engineered features
8. RF model .predict() returns class label, .predict_proba() returns probabilities
9. Flask returns JSON with prediction, confidence, alert_level, inference_ms
10. ApiClient parses the response into PredictionResult object
11. Platform.runLater() schedules UI update on JavaFX thread
12. updateAlertPanel() switches the color CSS based on alert_level
13. Charts get new data points appended, oldest popped if more than 30

### Q18: What did you learn from this project?
Three things stand out. First, the importance of robustness validation — without the label shuffle test, I would have presented 100% accuracy without confidence. Second, that GUI integration is often harder than ML itself — getting JavaFX threads, Flask CORS, and HTTP timeouts right took real engineering. Third, that good feature engineering can make even simple models like Random Forest beat fancier approaches.

