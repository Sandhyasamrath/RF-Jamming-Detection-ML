from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "RF Jamming Detector API running"})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    return jsonify({"message": "Endpoint ready", "received": data})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
