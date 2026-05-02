package rfdetect;

import javafx.animation.KeyFrame;
import javafx.animation.Timeline;
import javafx.application.Platform;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.chart.LineChart;
import javafx.scene.chart.XYChart;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.Region;
import javafx.util.Duration;

import java.net.URL;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.Random;
import java.util.ResourceBundle;

public class DashboardController implements Initializable {

    @FXML private LineChart<Number, Number> rssiChart;
    @FXML private LineChart<Number, Number> snrChart;
    @FXML private LineChart<Number, Number> pdrChart;
    @FXML private Region alertIndicator;
    @FXML private Label statusLabel;
    @FXML private Label confidenceLabel;
    @FXML private Label probNormalLabel;
    @FXML private Label probWeakLabel;
    @FXML private Label probStrongLabel;
    @FXML private Label apiStatusLabel;
    @FXML private Label timestampLabel;
    @FXML private Label footerLabel;
    @FXML private Label inferenceLabel;
    @FXML private Button startBtn;
    @FXML private Button stopBtn;

    private XYChart.Series<Number, Number> rssiSeries;
    private XYChart.Series<Number, Number> snrSeries;
    private XYChart.Series<Number, Number> pdrSeries;

    private Timeline simulator;
    private Timeline clock;
    private int timeStep = 0;
    private final int MAX_POINTS = 30;
    private final Random rng = new Random();

    @Override
    public void initialize(URL url, ResourceBundle rb) {
        rssiChart.setTitle("RSSI (Signal Strength)");
        snrChart.setTitle("SNR (Signal-to-Noise Ratio)");
        pdrChart.setTitle("PDR (Packet Delivery Ratio)");
        rssiChart.setAnimated(false);
        snrChart.setAnimated(false);
        pdrChart.setAnimated(false);
        rssiChart.setLegendVisible(false);
        snrChart.setLegendVisible(false);
        pdrChart.setLegendVisible(false);

        rssiSeries = new XYChart.Series<>();
        snrSeries  = new XYChart.Series<>();
        pdrSeries  = new XYChart.Series<>();
        rssiChart.getData().add(rssiSeries);
        snrChart.getData().add(snrSeries);
        pdrChart.getData().add(pdrSeries);

        startBtn.setOnAction(e -> startSimulation());
        stopBtn.setOnAction(e -> stopSimulation());

        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("HH:mm:ss");
        clock = new Timeline(new KeyFrame(Duration.seconds(1),
            e -> timestampLabel.setText(LocalTime.now().format(fmt))));
        clock.setCycleCount(Timeline.INDEFINITE);
        clock.play();

        new Thread(() -> {
            boolean alive = ApiClient.checkHealth();
            Platform.runLater(() -> {
                if (alive) {
                    apiStatusLabel.setText("API: Connected");
                    apiStatusLabel.setStyle("-fx-text-fill: #4caf50; -fx-font-size: 13px;");
                } else {
                    apiStatusLabel.setText("API: Offline");
                    apiStatusLabel.setStyle("-fx-text-fill: #f44336; -fx-font-size: 13px;");
                    footerLabel.setText("WARNING: Flask API not reachable. Start it with: python app.py");
                }
            });
        }).start();

        System.out.println("Dashboard initialized successfully");
    }

    private void startSimulation() {
        startBtn.setDisable(true);
        stopBtn.setDisable(false);
        footerLabel.setText("Live detection running... calling Flask API every 1s");
        simulator = new Timeline(new KeyFrame(Duration.seconds(1),
            e -> generateAndPredict()));
        simulator.setCycleCount(Timeline.INDEFINITE);
        simulator.play();
    }

    private void stopSimulation() {
        if (simulator != null) simulator.stop();
        startBtn.setDisable(false);
        stopBtn.setDisable(true);
        footerLabel.setText("Detection stopped. Click 'Start Live Detection' to resume.");
    }

    private void generateAndPredict() {
        timeStep++;
        int scenarioIdx = (timeStep / 8) % 3;
        double rssi, snr, pdr, packetLoss, noisePower, fftMean, fftVariance, peakFreq;

        if (scenarioIdx == 0) {
            rssi = -55 - rng.nextDouble() * 15;
            snr  =  25 + rng.nextDouble() * 10;
            pdr  = 0.92 + rng.nextDouble() * 0.08;
            packetLoss = 1.0 - pdr;
            noisePower = -98 + rng.nextDouble() * 5;
            fftMean = 0.10 + rng.nextDouble() * 0.18;
            fftVariance = 0.01 + rng.nextDouble() * 0.03;
            peakFreq = 2400 + rng.nextDouble() * 25;
        } else if (scenarioIdx == 1) {
            rssi = -70 - rng.nextDouble() * 13;
            snr  =  12 + rng.nextDouble() * 10;
            pdr  = 0.65 + rng.nextDouble() * 0.20;
            packetLoss = 1.0 - pdr;
            noisePower = -92 + rng.nextDouble() * 9;
            fftMean = 0.27 + rng.nextDouble() * 0.30;
            fftVariance = 0.04 + rng.nextDouble() * 0.10;
            peakFreq = 2418 + rng.nextDouble() * 37;
        } else {
            rssi = -85 - rng.nextDouble() * 13;
            snr  =   2 + rng.nextDouble() * 8;
            pdr  = 0.10 + rng.nextDouble() * 0.40;
            packetLoss = 1.0 - pdr;
            noisePower = -84 + rng.nextDouble() * 14;
            fftMean = 0.55 + rng.nextDouble() * 0.43;
            fftVariance = 0.13 + rng.nextDouble() * 0.25;
            peakFreq = 2445 + rng.nextDouble() * 53;
        }

        final double fRssi = rssi, fSnr = snr, fPdr = pdr;
        final double fPL = packetLoss, fNP = noisePower;
        final double fFM = fftMean, fFV = fftVariance, fPF = peakFreq;

        new Thread(() -> {
            ApiClient.PredictionResult result = ApiClient.predict(
                fRssi, fSnr, fPdr, fPL, fNP, fFM, fFV, fPF
            );

            Platform.runLater(() -> {
                rssiSeries.getData().add(new XYChart.Data<>(timeStep, fRssi));
                snrSeries.getData().add(new XYChart.Data<>(timeStep, fSnr));
                pdrSeries.getData().add(new XYChart.Data<>(timeStep, fPdr));

                if (rssiSeries.getData().size() > MAX_POINTS) {
                    rssiSeries.getData().remove(0);
                    snrSeries.getData().remove(0);
                    pdrSeries.getData().remove(0);
                }

                if (result.success) {
                    updateAlertPanel(result);
                    inferenceLabel.setText(String.format("Inference: %.1f ms",
                        result.inferenceMs));
                } else {
                    statusLabel.setText("API ERROR");
                    confidenceLabel.setText(result.error);
                    inferenceLabel.setText("Inference: -- ms");
                }
            });
        }).start();
    }

    private void updateAlertPanel(ApiClient.PredictionResult result) {
        statusLabel.setText(result.label.replace("_", " ").toUpperCase());
        confidenceLabel.setText(String.format("Confidence: %.1f%%",
            result.confidence * 100));

        probNormalLabel.setText(String.format("Normal: %.3f", result.probNormal));
        probWeakLabel.setText(String.format("Weak Jam: %.3f", result.probWeak));
        probStrongLabel.setText(String.format("Strong Jam: %.3f", result.probStrong));

        String color;
        switch (result.alertLevel) {
            case "GREEN":  color = "#4caf50"; break;
            case "YELLOW": color = "#ffa500"; break;
            case "RED":    color = "#f44336"; break;
            default:       color = "#9e9e9e"; break;
        }
        alertIndicator.setStyle(
            "-fx-background-color: " + color + "; -fx-background-radius: 5;"
        );
    }
}
