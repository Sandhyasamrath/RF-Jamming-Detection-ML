package rfdetect;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.Scanner;

public class ApiClient {

    private static final String API_BASE = "http://127.0.0.1:5000";
    private static final ObjectMapper mapper = new ObjectMapper();

    public static class PredictionResult {
        public int prediction;
        public String label;
        public String alertLevel;
        public double confidence;
        public double probNormal;
        public double probWeak;
        public double probStrong;
        public double inferenceMs;
        public boolean success;
        public String error;
    }

    public static boolean checkHealth() {
        try {
            URL url = new URL(API_BASE + "/health");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("GET");
            conn.setConnectTimeout(2000);
            conn.setReadTimeout(2000);
            return conn.getResponseCode() == 200;
        } catch (Exception e) {
            return false;
        }
    }

    public static PredictionResult predict(double rssi, double snr, double pdr,
                                           double packetLoss, double noisePower,
                                           double fftMean, double fftVariance,
                                           double peakFrequency) {
        PredictionResult result = new PredictionResult();
        try {
            ObjectNode payload = mapper.createObjectNode();
            payload.put("RSSI", rssi);
            payload.put("SNR", snr);
            payload.put("PDR", pdr);
            payload.put("Packet_Loss", packetLoss);
            payload.put("Noise_Power", noisePower);
            payload.put("FFT_Mean", fftMean);
            payload.put("FFT_Variance", fftVariance);
            payload.put("Peak_Frequency", peakFrequency);

            URL url = new URL(API_BASE + "/predict");
            HttpURLConnection conn = (HttpURLConnection) url.openConnection();
            conn.setRequestMethod("POST");
            conn.setRequestProperty("Content-Type", "application/json");
            conn.setDoOutput(true);
            conn.setConnectTimeout(3000);
            conn.setReadTimeout(3000);

            try (OutputStream os = conn.getOutputStream()) {
                os.write(payload.toString().getBytes(StandardCharsets.UTF_8));
            }

            int code = conn.getResponseCode();
            StringBuilder response = new StringBuilder();
            try (Scanner sc = new Scanner(
                    code >= 400 ? conn.getErrorStream() : conn.getInputStream(),
                    StandardCharsets.UTF_8)) {
                while (sc.hasNextLine()) response.append(sc.nextLine());
            }

            if (code != 200) {
                result.success = false;
                result.error = "HTTP " + code + ": " + response;
                return result;
            }

            JsonNode json = mapper.readTree(response.toString());
            result.prediction   = json.get("prediction").asInt();
            result.label        = json.get("label").asText();
            result.alertLevel   = json.get("alert_level").asText();
            result.confidence   = json.get("confidence").asDouble();
            result.inferenceMs  = json.get("inference_ms").asDouble();
            JsonNode probs = json.get("probabilities");
            result.probNormal = probs.get("Normal").asDouble();
            result.probWeak   = probs.get("Weak_Jamming").asDouble();
            result.probStrong = probs.get("Strong_Jamming").asDouble();
            result.success    = true;
        } catch (Exception e) {
            result.success = false;
            result.error = e.getMessage();
        }
        return result;
    }
}
