"""
Day 10 - Flask Prediction API
Real-time RF Jamming Detection endpoint
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from predictor import JammingPredictor
import time
import os

app = Flask(__name__)
CORS(app)

# Load model once at startup
predictor = JammingPredictor()

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "online",
        "service": "RF Jamming Detector API",
        "model_loaded": True,
        "version": "1.0"
    })

@app.route("/predict", methods=["POST"])
def predict():
    """
    Expects JSON body:
    {
        "RSSI": -60, "SNR": 30, "PDR": 0.95, "Packet_Loss": 0.05,
        "Noise_Power": -95, "FFT_Mean": 0.2, "FFT_Variance": 0.02,
        "Peak_Frequency": 2412
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON body provided"}), 400
        
        required = ["RSSI", "SNR", "PDR", "Packet_Loss",
                    "Noise_Power", "FFT_Mean", "FFT_Variance", "Peak_Frequency"]
        missing = [k for k in required if k not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400
        
        start = time.time()
        result = predictor.predict(data)
        result["inference_ms"] = round((time.time() - start) * 1000, 2)
        result["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/predict/batch", methods=["POST"])
def predict_batch():
    """Batch predictions for multiple samples"""
    try:
        data = request.get_json()
        samples = data.get("samples", [])
        if not samples:
            return jsonify({"error": "No samples provided"}), 400
        
        results = []
        for sample in samples:
            results.append(predictor.predict(sample))
        
        return jsonify({"count": len(results), "results": results}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("=" * 50)
    print("RF Jamming Detection API")
    print("Endpoints:")
    print("  GET  /health")
    print("  POST /predict")
    print("  POST /predict/batch")
    print("=" * 50)
    app.run(debug=False, host="0.0.0.0", port=5000)
