Neuraflow Hardware Simulator (OpenBCI_GUI fork)
================================================

This is a small custom fork of OpenBCI_GUI that adds support for connecting to virtual serial ports (pseudo-terminals). It makes development and testing easier by allowing the GUI to talk to simulated boards or data streams without physical hardware.

Features

- Connect to virtual/loopback serial ports (PTYs)
- Easier automated testing and development workflows
- Minimal, compatible changes to the original OpenBCI_GUI

Quick Start

- Create a virtual serial pair (example using `socat`):

 socat -d -d pty,raw,echo=0 pty,raw,echo=0

- Configure the GUI to open the provided PTY device path.

Notes

- This project is intended for development and simulation only — not a replacement for the official OpenBCI tools. See the original OpenBCI_GUI for upstream features and licensing.

License

- [MIT](/LICENSE)
