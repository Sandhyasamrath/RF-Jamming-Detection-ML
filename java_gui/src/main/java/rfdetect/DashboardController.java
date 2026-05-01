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

        apiStatusLabel.setText("API: Simulation Mode");
        System.out.println("Dashboard initialized successfully");
    }

    private void startSimulation() {
        startBtn.setDisable(true);
        stopBtn.setDisable(false);
        footerLabel.setText("Live detection running... feeding simulated RF data every 1s");
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
        double rssi, snr, pdr, confidence;
        int prediction;
        String label;

        if (scenarioIdx == 0) {
            rssi = -55 - rng.nextDouble() * 15;
            snr  =  25 + rng.nextDouble() * 10;
            pdr  = 0.92 + rng.nextDouble() * 0.08;
            confidence = 0.95 + rng.nextDouble() * 0.05;
            prediction = 0;
            label = "NORMAL";
        } else if (scenarioIdx == 1) {
            rssi = -70 - rng.nextDouble() * 13;
            snr  =  12 + rng.nextDouble() * 10;
            pdr  = 0.65 + rng.nextDouble() * 0.20;
            confidence = 0.85 + rng.nextDouble() * 0.10;
            prediction = 1;
            label = "WEAK JAMMING";
        } else {
            rssi = -85 - rng.nextDouble() * 13;
            snr  =   2 + rng.nextDouble() * 8;
            pdr  = 0.10 + rng.nextDouble() * 0.40;
            confidence = 0.92 + rng.nextDouble() * 0.08;
            prediction = 2;
            label = "STRONG JAMMING";
        }

        final double fRssi = rssi, fSnr = snr, fPdr = pdr, fConf = confidence;
        final int fPred = prediction;
        final String fLabel = label;

        Platform.runLater(() -> {
            rssiSeries.getData().add(new XYChart.Data<>(timeStep, fRssi));
            snrSeries.getData().add(new XYChart.Data<>(timeStep, fSnr));
            pdrSeries.getData().add(new XYChart.Data<>(timeStep, fPdr));

            if (rssiSeries.getData().size() > MAX_POINTS) {
                rssiSeries.getData().remove(0);
                snrSeries.getData().remove(0);
                pdrSeries.getData().remove(0);
            }

            updateAlertPanel(fPred, fLabel, fConf);
            inferenceLabel.setText(String.format("Inference: %.1f ms",
                25 + rng.nextDouble() * 20));
        });
    }

    private void updateAlertPanel(int prediction, String label, double confidence) {
        statusLabel.setText(label);
        confidenceLabel.setText(String.format("Confidence: %.1f%%", confidence * 100));

        double[] probs = new double[3];
        probs[prediction] = confidence;
        double remaining = 1.0 - confidence;
        for (int i = 0; i < 3; i++) {
            if (i != prediction) probs[i] = remaining / 2;
        }

        probNormalLabel.setText(String.format("Normal: %.3f", probs[0]));
        probWeakLabel.setText(String.format("Weak Jam: %.3f", probs[1]));
        probStrongLabel.setText(String.format("Strong Jam: %.3f", probs[2]));

        String color;
        switch (prediction) {
            case 0: color = "#4caf50"; break;  // GREEN
            case 1: color = "#ffa500"; break;  // ORANGE
            default: color = "#f44336"; break; // RED
        }
        alertIndicator.setStyle(
            "-fx-background-color: " + color + "; -fx-background-radius: 5;"
        );
    }
}
