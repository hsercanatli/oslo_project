import pyaudio
import wave
import datetime

from PyQt5.QtCore import QObject


class Recorder(QObject):
    CHUNK = 1024

    def __init__(self, parent=None, bitrate=pyaudio.paInt16, sample_rate=48000, num_channels=2):
        super().__init__(parent)
        self.IS_ON_AIR = False

        self._bitrate = bitrate
        self._sample_rate = sample_rate
        self._num_channels = num_channels

        self._recording_data = []

        # set stream
        self._audio_object = pyaudio.PyAudio()

        # open wave file
        self._generate_wave_file()

    # public methods
    def start_recording(self):
        if not self.IS_ON_AIR:
            self._set_stream()
            self.IS_ON_AIR = True
            print("stream is set")

    def stop_recording(self):
        self.IS_ON_AIR = False

        self._stream.stop_stream()
        self._stream.close()
        self._audio_object.terminate()

        self._wave_file.writeframes(b''.join(self._recording_data))
        self._wave_file.close()

    # private methods
    def _set_stream(self):
        self._stream = self._audio_object.open(format=self._bitrate,
                                               rate=self._sample_rate,
                                               channels=self._num_channels,
                                               input=True,
                                               frames_per_buffer=self.CHUNK)

    def _generate_wave_file(self):
        file_name = str(datetime.datetime.now()) + ".wav"
        self._wave_file = wave.open(file_name, 'wb')
        self._wave_file.setframerate(self._sample_rate)
        self._wave_file.setnchannels(self._num_channels)
        self._wave_file.setsampwidth(self._audio_object.get_sample_size(self._bitrate))

    def write_frames(self):
        self._recording_data.append(self._stream.read(self.CHUNK))
