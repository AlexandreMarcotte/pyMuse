__author__ = 'benjamindeleener'
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
import numpy as np
from utils import AutoQueue


def timeTicks(x, pos):
    d = timedelta(milliseconds=x)
    return str(d)


class Viewer(object):
    def __init__(self, refresh_freq=10.0, signal_boundaries=None):
        super(Viewer, self).__init__()
        self.name = 'viewer'

        self.refresh_freq = refresh_freq
        self.init_time = datetime.now()
        self.last_refresh = datetime.now()

        if signal_boundaries is not None:
            self.low, self.high = signal_boundaries[0], signal_boundaries[1]
        else:
            self.low, self.high = 0, 1

    def show(self):
        plt.show(block=False)
        #plt.show()

    def start(self):
        self.show()
        #self.thread.start()


class ViewerSignal(Viewer):
    def __init__(self, signal, window_duration=5000.0, refresh_freq=10.0, signal_boundaries=None):
        super(ViewerSignal, self).__init__(refresh_freq, signal_boundaries)
        self.signal = signal
        self.window_duration = window_duration
        self.number_of_channels = self.signal.number_of_channels

        self.figure, self.axes = plt.subplots(self.number_of_channels, 1, sharex=True, figsize=(15, 10))
        self.axes_plot = []
        formatter = mticker.FuncFormatter(timeTicks)

        self.signal.lock.acquire()
        signal_time, signal_data = self.signal.get_window_ms(length_window=self.window_duration)
        self.signal.lock.release()

        for i, label in enumerate(self.signal.label_channels):
            self.axes[i].set_title(label)
            ax_plot, = self.axes[i].plot(signal_time, signal_data[i, :])
            self.axes_plot.append(ax_plot)
            self.axes[i].set_ylim([self.low, self.high])
            self.axes[i].xaxis.set_major_formatter(formatter)

        self.figure.canvas.draw()
        plt.ion()

    def refresh(self):
        while True:
            time_now = datetime.now()
            if (time_now - self.last_refresh).total_seconds() > 1.0 / self.refresh_freq:
                self.last_refresh = time_now
                pass
            else:
                return

            self.signal.lock.acquire()
            signal_time, signal_data = self.signal.get_window_ms(length_window=self.window_duration)
            self.signal.lock.release()
            for i in range(self.number_of_channels):
                self.axes_plot[i].set_ydata(signal_data[i, :])
                times = np.linspace(signal_time[0], signal_time[-1], len(signal_time))
                self.axes_plot[i].set_xdata(times)
            self.axes[0].set_xlim(signal_time[0], signal_time[-1])

            self.figure.canvas.draw()
            self.figure.canvas.flush_events()


class FFTViewer(Viewer):
    def __init__(self, signal=None, refresh_freq=10.0, signal_boundaries=None, label_channels=None):
        """
        Plots a Single-Sided Amplitude Spectrum of y(t)
        """
        if signal_boundaries is None:
            signal_boundaries = [0, 15]
        super(FFTViewer, self).__init__(refresh_freq, signal_boundaries)
        self.signal = signal

        self.label_channels = label_channels
        self.number_of_channels = len(self.label_channels)

        self.figure, self.axes = plt.subplots(self.number_of_channels, 1, figsize=(15, 10))
        self.axes_plot = []
        formatter = mticker.FuncFormatter(timeTicks)

        fake_freq, fake_data = range(100), np.zeros(100)

        for i, label in enumerate(self.label_channels):
            self.axes[i].set_title(label)
            ax_plot, = self.axes[i].plot(fake_freq, fake_data)
            self.axes_plot.append(ax_plot)
            self.axes[i].set_ylim([self.low, self.high])
            self.axes[i].set_xlim([0.0, 100.0])

        self.figure.canvas.draw()
        plt.ion()

    def refresh(self, data=None):
        time_now = datetime.now()
        if (time_now - self.last_refresh).total_seconds() > 1.0 / self.refresh_freq:
            self.last_refresh = time_now
            pass
        else:
            return

        if data is not None:
            signal_to_display = data
        elif isinstance(self.signal, AutoQueue):
            signal_to_display = self.signal.get()
        else:
            signal_to_display = self.signal

        signal_to_display.lock.acquire()
        signal_freq = signal_to_display.freq
        signal_data = abs(signal_to_display.data)**2
        signal_to_display.lock.release()
        x_freq = range(0, 100)

        for i in range(self.number_of_channels):
            y_signal = np.interp(x_freq, signal_freq, signal_data[i, :])
            self.axes_plot[i].set_data(x_freq, y_signal)
            #self.axes_plot[i].set_data(signal_freq, signal_data[i, :])
            #self.axes[i].set_xlim(signal_freq[0], signal_freq[-1])
            #self.axes[i].draw_artist(self.axes_plot[i])

        #self.figure.canvas.update()
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

        #print signal_to_display.get_alpha_power()
