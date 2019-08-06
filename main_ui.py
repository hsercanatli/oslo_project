import time

from PyQt5.QtWidgets import QDialog, QGroupBox, QPushButton, QHBoxLayout, QVBoxLayout

from graph_widget import TimeSeriesWidget
from workers import SensorWorker, RecorderWorker


class MainWindow(QDialog):
    """UI is here"""

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # creating the layout
        self._create_buttons_group()
        self._create_graphs_group()

        # creating layout for main dialog
        layout = QVBoxLayout()
        layout.addWidget(self.buttonsGroupBox)
        layout.addWidget(self.graphsGroupBox)

        self.setLayout(layout)

        # setting mock sensors
        self.sensor_list = []
        self.sensor_1 = SensorWorker(self, min_freq=50, max_freq=1000, sample_rate=500, name="Sensor_1")
        self.sensor_2 = SensorWorker(self, min_freq=50, max_freq=1000, sample_rate=500, name="Sensor_2")
        self.sensor_3 = SensorWorker(self, min_freq=50, max_freq=1000, sample_rate=500, name="Sensor_3")
        self.sensor_4 = SensorWorker(self, min_freq=50, max_freq=1000, sample_rate=500, name="Sensor_4")

        self.recorder = RecorderWorker(self)

        self.sensor_list = [self.sensor_1, self.sensor_2, self.sensor_3, self.sensor_4]

        # signals
        self.recordButton.clicked.connect(self._record_button_clicked)
        self.stopButton.clicked.connect(self._stop_button_clicked)

    # -------------------- override methods -------------------#
    def closeEvent(self, QCloseEvent):
        pass
        """Stops the mock sensors before closing the app"""

    # --------------------- private methods ---------------------#
    # ui creation
    def _create_buttons_group(self):
        self.buttonsGroupBox = QGroupBox()

        self.recordButton = QPushButton("Record")
        self.stopButton = QPushButton("Stop")
        self.stopButton.setDisabled(True)

        layout = QHBoxLayout()
        layout.addWidget(self.recordButton)
        layout.addWidget(self.stopButton)
        layout.addStretch(1)

        self.buttonsGroupBox.setLayout(layout)

    def _create_graphs_group(self):
        self.graphsGroupBox = QGroupBox()

        self.sensor_1_graph = TimeSeriesWidget()

        layout = QHBoxLayout()
        layout.addWidget(self.sensor_1_graph)
        layout.addStretch(1)

        self.graphsGroupBox.setLayout(layout)

    # ---------------#

    # ui controllers
    def _update_button_status(self):
        if self.sensor_1.is_sensor_active():
            self.recordButton.setDisabled(True)
            self.stopButton.setDisabled(False)
        else:
            self.recordButton.setDisabled(False)
            self.stopButton.setDisabled(True)

    # ---------------#

    # slots
    def _record_button_clicked(self):
        self.recorder.start_recording.emit()
        self._run_sensors()
        self.time_now = time.time()
        self._update_button_status()

    def _stop_button_clicked(self):
        self.recorder.stop_recording.emit()
        self._stop_sensors()
        print(time.time() - self.time_now)
        self._update_button_status()

    # ---------------#

    # sensor related
    def _run_sensors(self):
        for sensor in self.sensor_list:
                sensor.start()

    def _stop_sensors(self):
        for sensor in self.sensor_list:
            if sensor.is_sensor_active():
                sensor.stop()
    # ---------------#
