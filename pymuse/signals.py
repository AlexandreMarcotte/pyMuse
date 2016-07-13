__author__ = 'benjamindeleener'
import numpy as np
from datetime import datetime

class MuseSignal(object):
    def __init__(self, length, acquisition_freq):
        self.length = length
        self.acquisition_freq = acquisition_freq
        self.time = list(np.linspace(-float(self.length) / self.acquisition_freq + 1.0 / self.acquisition_freq, 0.0, self.length))
        self.init_time = datetime.now()

    def add_time(self):
        diff = datetime.now() - self.init_time
        self.time.append(float(diff.total_seconds() * 1000))  # in milliseconds
        del self.time[0]

    def compute_real_acquisition_frequency(self, window=None):
        if not window or window > self.length:
            window = self.length

        diff_time = np.zeros(window)
        for k in range(0, window - 1):  # self.length, self.length - window, -1):
            diff_time[k] = self.time[self.length - k] - self.time[self.length - (k + 1)]
        acquisition_frequency = 1.0 / np.mean(diff_time)
        return acquisition_frequency


class MuseEEG(MuseSignal):
    def __init__(self, length=200, acquisition_freq=220.0):
        super(MuseEEG, self).__init__(length, acquisition_freq)
        self.l_ear, self.l_forehead, self.r_forehead, self.r_ear = [0.0] * self.length, [0.0] * self.length, \
                                                                   [0.0] * self.length, [0.0] * self.length

    def add_l_ear(self, s):
        self.l_ear.append(s)
        del self.l_ear[0]

    def add_l_forehead(self, s):
        self.l_forehead.append(s)
        del self.l_forehead[0]

    def add_r_forehead(self, s):
        self.r_forehead.append(s)
        del self.r_forehead[0]

    def add_r_ear(self, s):
        self.r_ear.append(s)
        del self.r_ear[0]


class MuseConcentration(MuseSignal):
    def __init__(self, length=200, acquisition_freq=10.0):
        super(MuseConcentration, self).__init__(length, acquisition_freq)
        self.concentration = [0.0] * self.length

    def add_concentration(self, s):
        self.concentration.append(s)
        del self.concentration[0]


class MuseMellow(MuseSignal):
    def __init__(self, length=200, acquisition_freq=10.0):
        super(MuseMellow, self).__init__(length, acquisition_freq)
        self.mellow = [0.0] * self.length

    def add_mellow(self, s):
        self.mellow.append(s)
        del self.mellow[0]
