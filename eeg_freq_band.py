__author__ = 'benjamindeleener'

import sys
import time
from pymuse.ios import MuseIO, MuseIOError
from pymuse.viz import ViewerSignal
from pymuse.signals import MultiChannelSignal
from pymuse.pipeline import Analyzer

import numpy as np


def main():
    # initialization of variables
    signals, viewers = dict(), dict()

    # EEG signal
    signal_eeg = MultiChannelSignal(length=2000,
                                    estimated_acquisition_freq=220.0,
                                    label_channels=['Left ear', 'Left forehead', 'Right forehead', 'Right ear'])
    #viewer_eeg = ViewerSignal(window_duration=5000.0, signal=signal_eeg, refresh_freq=220.0, signal_boundaries=[600, 1200])

    signals['eeg'] = signal_eeg
    #viewers['eeg'] = viewer_eeg

    # Initializing the analyzer
    pipeline = Analyzer(signal=signals['eeg'], window_duration=200, analysis_frequency=10.0, list_process=['FFT'])
    queue_out = pipeline.get_final_queue()

    # Initializing the server
    try:
        server = MuseIO(port=5001, signal=signals)
    except MuseIOError, err:
        print str(err)
        sys.exit(1)

    # Displaying the viewers
    """for sign in viewers:
        viewers[sign].start()
    """

    pipeline.start()

    # Starting the server
    try:
        server.start()
        while 1:
            time.sleep(0.01)
    except KeyboardInterrupt:
        print "\nEnd of program: Caught KeyboardInterrupt"
        sys.exit(0)

if __name__ == "__main__":
    main()
