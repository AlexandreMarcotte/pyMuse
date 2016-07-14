__author__ = 'benjamindeleener'

import sys
import time
from pymuse.ios import MuseIO, MuseIOError
from pymuse.viz import ViewerMuseEEG, MuseViewerConcentrationMellow
from pymuse.signals import MuseEEG, MuseConcentration, MuseMellow


def main():
    # initialization of variables
    signals, viewers = dict(), dict()

    # EEG signal
    signal_eeg = MuseEEG(length=2000, acquisition_freq=220.0)
    viewer_eeg = ViewerMuseEEG(signal_eeg, 220.0, signal_boundaries=[600, 1200])

    signals['eeg'] = signal_eeg
    viewers['eeg'] = viewer_eeg

    """
    # Concentration and Mellow
    signal_concentration = MuseConcentration(length=400, acquisition_freq=10.0)
    signal_mellow = MuseMellow(length=400, acquisition_freq=10.0)
    viewer_concentration_mellow = MuseViewerConcentrationMellow(signal_concentration, signal_mellow, signal_boundaries=[-0.05, 1.05])

    signals['concentration'] = signal_concentration
    signals['mellow'] = signal_mellow
    viewers['concentration-mellow'] = viewer_concentration_mellow
    """

    # Initializing the server
    try:
        server = MuseIO(port=5001, signal=signals, viewer=viewers)
    except MuseIOError, err:
        print str(err)
        sys.exit(1)

    # Displaying the viewers
    for sign in viewers:
        viewers[sign].show()

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
