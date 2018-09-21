
# pyMuse

This repository contains tools for getting Muse signals using Python.

## Installation & dependences
You will need some tools to get started with Muse headset and pyMuse:
* [MuseDirect](http://www.choosemuse.com/direct/)
* [Python 2.7](https://www.python.org/downloads/release/python-2714/)

Don't hesitate to go on [Muse Developer website](http://www.choosemuse.com/developer/) to get information.

### Installation of this package
Make sure you downloaded the right Python distribution and download the pyMuse package (e.g., using `git clone`).

Open a terminal, go into the package and type: 
`pip install -r requirements.txt`.

The installer should install all requirements, including:
* numpy
* scipy
* matplotlib
* [pyosc](https://github.com/ptone/pyosc/)

## Getting started
### Display your Muse data with eeg displayer
1. Connect your Muse headset with your computer by bluetooth
2. Start Muse Direct and set an OSC UDP output:

![Set OSC/UDP output on localhost:5001](https://lh3.googleusercontent.com/W52JORAt_rx-I_VBtzFf7ieRUFCQMIeXCrc2jSvjHaPJgtIg_cz5M0OIeth8pdh3oAcquDXr2Vs "OSC.UDP Output")

Be sure all output data and all output algorithm are selected.

3. Start EEG display script (in a new terminal):
  ```
  python eeg_display.py
  ```

### Save Muse data and stream offline

See the [developer webpage](http://www.choosemuse.com/developer-kit/) for details.

1. Connect your Muse headset with your computer by bluetooth
2. Start Muse Direct and set a Save to File output:

![You must create a save to file output](https://lh3.googleusercontent.com/Qy2mg7cmcef-sTSC9IqtNAdgBZsTUtfSpNErYwagc1kWdqHvd3IVe-paVRLkgADW7cGxs4TDSvU "SaveToFile")

3. Press the record button when you want to start to record your brain waves. Stop recording when you're done.

![Press Record](https://lh3.googleusercontent.com/Gd_jUquAZrnu_YVDi36yChywVhYmjC-4V0Xpy494xSXPQJFLooL-PEJhlMgIjRSjIgWEERSb1Eo "Press Record")

4. Run [MusePlayer](http://developer.choosemuse.com/tools/museplayer) to stream the data to a server.
  ```
  muse-player -f MyExperiment.muse -s osc.udp://localhost:5001
  ```
Note that you can add your recorded data to the following [repository](https://github.com/PolyCortex/MuseData) to share it with the other members.

5. Now you can display your recorded session using eeg displayer, or processing with your favorite software.
