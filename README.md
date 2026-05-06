Neuraflow Hardware Simulator
================================================

A basic Python-based simulator for OpenBCI hardware. This repository provides a lightweight simulator that emits OpenBCI-style data packets over a virtual serial device (PTY), so you can develop and test GUIs and data pipelines without physical boards.

Features

- Simulate OpenBCI-style data streams over pseudo-terminals (PTYs)
- Generate synthetic signals or replay recorded data
- Simple command-line entrypoint (`cyton.py`) to start a simulator on a device
- Useful for automated testing, development, and integration with OpenBCI_GUI

Quick start

1. Create a virtual serial pair (example using `socat`):

 socat -d -d pty,raw,echo=0 pty,raw,echo=0

 socat prints two device paths (e.g. `/dev/pts/3` and `/dev/pts/4`).

1. Start the simulator on one end of the pair (replace with the device path shown by `socat`):

 python3 cyton.py /dev/pts/3

1. Point your OpenBCI-compatible GUI or tool to the other device path (e.g. `/dev/pts/4`) and connect.

Requirements

- Python 3.8 or newer
- `pyserial` (and `numpy` if using generated signals)

Install dependencies:

 pip install pyserial numpy

Usage notes

- `cyton.py` is the simulator entrypoint in this repository. It accepts a serial device path and will emit a continuous OpenBCI-like stream. Run `python3 cyton.py --help` for available options if supported.
- This project is intended for development and testing only — it does not replace real OpenBCI hardware or official tools.

License

- MIT — see [LICENSE](LICENSE)
