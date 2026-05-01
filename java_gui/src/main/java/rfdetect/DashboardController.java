package rfdetect;

import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.chart.LineChart;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.Region;
import java.net.URL;
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

    @Override
    public void initialize(URL url, ResourceBundle rb) {
        rssiChart.setTitle("RSSI (Signal Strength)");
        snrChart.setTitle("SNR (Signal-to-Noise Ratio)");
        pdrChart.setTitle("PDR (Packet Delivery Ratio)");
        rssiChart.setAnimated(false);
        snrChart.setAnimated(false);
        pdrChart.setAnimated(false);
        apiStatusLabel.setText("API: Disconnected");
        System.out.println("Dashboard initialized successfully");
    }
}
