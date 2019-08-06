import random

from PyQt5.QtCore import QObject

import datetime


class MockSensor(QObject):
    # signal

    def __init__(self, min_freq=20, max_freq=20000, sample_rate=500, name="", parent=None):
        QObject.__init__(self, parent)
        self.TIME_STAMP = 0  # in sec
        self.IS_FILE_OPEN = False

        self.min_freq = min_freq
        self.max_freq = max_freq
        self.sample_rate = sample_rate
        self.name = name

        self.interval = 1000 / self.sample_rate  # in msec
        self.generate_results_file()

    # public methods
    def generate_signal(self):
        self._generate_timestamp()
        self._write_results(self.TIME_STAMP, self._generate_freq())
        # !!! Need a signal here to trigger plotting

    def stop(self):
        # close the file
        self._results_file.close()
        self.IS_FILE_OPEN = False

        # reset the items
        self.TIME_STAMP = 0

    # private methods
    def generate_results_file(self):
        if not self.IS_FILE_OPEN:
            self._results_file = open(self.name + "_" + str(datetime.datetime.now()) + ".txt", "w")
            self.IS_FILE_OPEN = True

    def _generate_timestamp(self):
        """Updates timestamp"""
        self.TIME_STAMP += (self.interval / 1000)  # in secs

    def _generate_freq(self):
        """Generates random signal between the intervals"""
        return random.uniform(self.min_freq, self.max_freq)

    def _write_results(self, timestamp, freq):
        self._results_file.write(str(timestamp) + "\t" + str(freq) + "\n")
