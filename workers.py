from PyQt5.QtCore import QThread, QObject, QTimer, pyqtSignal
import pyaudio

from mock_sensor import MockSensor
from recorder import Recorder


class SensorWorker(QObject):
    def __init__(self, parent=None, min_freq=20, max_freq=20000, sample_rate=500, name=""):
        super().__init__(parent)

        # worker
        self.sensor = MockSensor(min_freq, max_freq, sample_rate, name)

        # timer
        self.timer = QTimer()
        self.timer.setInterval(self.sensor.interval)

        # worker thread
        self.worker_thread = QThread()
        self.sensor.moveToThread(self.worker_thread)
        self.worker_thread.start()

        # signals
        self.timer.timeout.connect(self.sensor.generate_signal)

    def is_sensor_active(self):
        return self.timer.isActive()

    def start(self):
        self.sensor.generate_results_file()
        self.timer.start()

    def stop(self):
        self.timer.stop()
        self.sensor.stop()


class RecorderWorker(QObject):
    start_recording = pyqtSignal()
    stop_recording = pyqtSignal()

    def __init__(self, parent=None, bitrate=pyaudio.paInt16, sample_rate=48000, num_channels=2):
        super().__init__(parent)

        # recorder
        self.recorder = Recorder(parent=None, bitrate=bitrate, sample_rate=sample_rate, num_channels=num_channels)

        # worker thread
        self.worker_thread = QThread()
        self.recorder.moveToThread(self.worker_thread)
        self.worker_thread.start()

        self.timer = QTimer()
        self.timer.setInterval((1000/sample_rate) * self.recorder.CHUNK)

        # signals
        self.timer.timeout.connect(self.recorder.write_frames)

        self.start_recording.connect(self.recorder.start_recording)
        self.start_recording.connect(self.timer.start)

        self.stop_recording.connect(self.recorder.stop_recording)
        self.stop_recording.connect(self.timer.stop)
