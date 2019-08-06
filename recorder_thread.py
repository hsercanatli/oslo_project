from PyQt5.QtCore import QThread
import pyaudio

from recorder import Recorder


class RecorderThread(QThread):
    def __init__(self, parent=None, bitrate=pyaudio.paInt16, sample_rate=48000, num_channels=2):
        QThread.__init__(self, parent)

        self._recorder = Recorder(bitrate, sample_rate, num_channels)

    def start(self, priority=None):
        self._recorder.start_recording()

    def stop(self):
        self._recorder.stop_recording()
