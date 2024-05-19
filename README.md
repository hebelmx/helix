# helix


# Inverter and PLC Controller

This project provides a comprehensive solution for controlling an inverter and a PLC (Programmable Logic Controller) using CAN bus and Ethernet communication. The application features a graphical user interface (GUI) built with Tkinter and integrates real-time graphing using Matplotlib.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- Control inverter parameters such as system state, control mode, torque setpoint, and direction of rotation.
- Enable and disable the drive.
- Display real-time status and fault messages from the inverter.
- Graph real-time data for current, speed, and torque.
- Interface with a PLC to control relays and read inputs.
- User-friendly GUI built with Tkinter.

## Installation

### Prerequisites

- Python 3.x
- CAN interface (e.g., CAN USB adapter)
- Ethernet connection for PLC communication

### Required Python Libraries

Install the required Python libraries using pip:

```bash
pip install python-can snap7 matplotlib numpy tkinter


Usage
Setup CAN Interface: Ensure your CAN interface is connected and configured (e.g., can0 for SocketCAN on Linux).
Configure PLC: Update the PLC IP address, rack, and slot in the PLCController class.
Run the Application: Execute the Python script to launch the GUI.
bash
Copy code
python inverter_control.py
GUI Controls
System State: Set the system state of the inverter.
Control Mode: Set the control mode of the inverter.
Torque Setpoint: Set the torque setpoint for the inverter.
Enable Drive: Enable or disable the drive.
Direction of Rotation: Set the direction of rotation for the motor.
Activate PLC Output: Activate a specified PLC output.
Read PLC Input: Read a specified PLC input.
Real-Time Graphs
The GUI displays real-time graphs for current, speed, and torque, updating automatically as data is received from the inverter.

Project Structure
plaintext
Copy code
.
├── README.md
├── inverter_control.py
├── requirements.txt
└── assets
    └── example.png
README.md: This file.
inverter_control.py: The main Python script for the application.
requirements.txt: List of required Python libraries.
assets/: Directory for storing images and other assets.
Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Open a Pull Request.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
python-can
python-snap7
Matplotlib
Tkinter
markdown
Copy code

### How to Use the Markdown File

1. **Save the Content**: Save the provided content into a file named `README.md`.
2. **Add to Repository**: Place the `README.md` file in the root directory of your repository.
3. **Commit and Push**: Commit the `README.md` file to your GitHub repository.

```bash
git add README.md
git commit -m "Add README.md"
git push origin main
This README.md file will serve as the main page of your repository on GitHub, providing essential information about your project to users and contributors.