import urllib.request
import json
import time

N = 100
latencies = []
predictions = {"Normal": 0, "Weak_Jamming": 0, "Strong_Jamming": 0}

print(f"Sending {N} requests to Flask API...")
start = time.time()

for i in range(N):
    scenario = i % 3
    if scenario == 0:
        data = {"RSSI": -60, "SNR": 30, "PDR": 0.95, "Packet_Loss": 0.05,
                "Noise_Power": -95, "FFT_Mean": 0.2, "FFT_Variance": 0.02,
                "Peak_Frequency": 2412}
    elif scenario == 1:
        data = {"RSSI": -75, "SNR": 17, "PDR": 0.75, "Packet_Loss": 0.25,
                "Noise_Power": -88, "FFT_Mean": 0.4, "FFT_Variance": 0.08,
                "Peak_Frequency": 2435}
    else:
        data = {"RSSI": -90, "SNR": 5, "PDR": 0.30, "Packet_Loss": 0.70,
                "Noise_Power": -75, "FFT_Mean": 0.8, "FFT_Variance": 0.25,
                "Peak_Frequency": 2470}

    req = urllib.request.Request(
        "http://127.0.0.1:5000/predict",
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"}
    )
    t0 = time.time()
    response = json.loads(urllib.request.urlopen(req).read())
    latencies.append((time.time() - t0) * 1000)
    predictions[response["label"]] += 1

elapsed = time.time() - start
print(f"\n=== STRESS TEST RESULTS ===")
print(f"Total requests:     {N}")
print(f"Total time:         {elapsed:.2f}s")
print(f"Throughput:         {N/elapsed:.1f} req/sec")
print(f"Avg latency:        {sum(latencies)/len(latencies):.2f} ms")
print(f"Min latency:        {min(latencies):.2f} ms")
print(f"Max latency:        {max(latencies):.2f} ms")
print(f"\nPrediction distribution:")
for label, count in predictions.items():
    print(f"  {label:<20} {count}")
print(f"\nAll {N} requests succeeded - API is stable!")
