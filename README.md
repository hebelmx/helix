# Inverter and PLC Controller

This project provides a comprehensive solution for controlling an inverter and a PLC (Programmable Logic Controller) using CAN bus and Ethernet communication. The application features a graphical user interface (GUI) built with Tkinter and integrates real-time graphing using Matplotlib.

## Table of Contents

- [Features](#features)
- [System Requirements](#system-requirements)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [GUI Components](#gui-components)
- [CAN Messages and PLC Communication](#can-messages-and-plc-communication)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **Inverter Control**: Set system state, control mode, torque setpoint, enable/disable drive, and direction of rotation.
- **Real-Time Monitoring**: Display status and fault messages from the inverter.
- **Graphing**: Real-time graphs for current, speed, and torque.
- **PLC Control**: Control relays and read inputs from the PLC.
- **User-Friendly GUI**: Simple and intuitive interface for user interaction.

## System Requirements

- **Operating System**: Windows, Linux, or macOS
- **Python Version**: Python 3.x
- **Hardware**: CAN interface (e.g., CAN USB adapter), Ethernet connection for PLC communication

### Required Python Libraries

- `python-can`
- `snap7`
- `matplotlib`
- `numpy`
- `tkinter`

## Architecture

The application consists of the following main components:

1. **InverterController**: Handles CAN communication with the inverter.
2. **PLCController**: Manages Ethernet communication with the PLC.
3. **App**: The main GUI application that integrates the InverterController and PLCController, providing user interaction and real-time graphing.

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/inverter-plc-controller.git
   cd inverter-plc-controller
2. **Install Python Libraries**:
   ```bash
   pip install python-can snap7 matplotlib numpy
   
3. **Configure PLC**: Update the IP address, rack, and slot in the PLCController class in inverter_control.py.
   
   ## Usage

1. **Run the Application**:
   ```bash
   python inverter_control.py
## GUI Controls:

## GUI Components

- **System State**: Input field and button to set the system state.
- **Control Mode**: Input field and button to set the control mode.
- **Torque Setpoint**: Input field and button to set the torque setpoint.
- **Enable Drive**: Input field and button to enable or disable the drive.
- **Direction of Rotation**: Input field and button to set the direction of rotation.
- **Status**: Label to display the current status.
- **PLC Control**: Buttons to activate PLC output and read PLC input.
- **Graphs**: Real-time graphs for current, speed, and torque using Matplotlib.

### Real-Time Graphs

The GUI displays real-time graphs for current, speed, and torque, updating automatically as data is received from the inverter.

## CAN Messages and PLC Communication

### CAN Messages

- **System State (0x101)**: Set the system state of the inverter.
- **Control Mode (0x102)**: Set the control mode of the inverter.
- **Torque Setpoint (0x103)**: Set the torque setpoint.
- **Enable Drive (0x104)**: Enable or disable the drive.
- **Direction of Rotation (0x105)**: Set the direction of rotation.
- **Status (0x201)**: Receive status messages from the inverter.
- **Fault (0x202)**: Receive fault messages from the inverter.
- **Current (0x203)**: Receive current data from the inverter.
- **Speed (0x204)**: Receive speed data from the inverter.
- **Torque (0x205)**: Receive torque data from the inverter.

### PLC Communication

- **PLC IP**: 192.168.0.1
- **Rack**: 0
- **Slot**: 1
- **Port**: 102

## Error Handling

- **CAN Communication Errors**: Logged using the `logging` module and displayed in the GUI status label.
- **PLC Communication Errors**: Logged using the `logging` module and displayed in the GUI status label.
- **User Input Errors**: Handled using try-except blocks and displayed in the GUI status label.

## Logging

The application uses the `logging` module to log information, errors, and debug messages. Logs are printed to the console for real-time monitoring.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Acknowledgements

- [python-can](https://python-can.readthedocs.io/en/stable/)
- [python-snap7](https://python-snap7.readthedocs.io/en/latest/)
- [Matplotlib](https://matplotlib.org/)
- [Tkinter](https://wiki.python.org/moin/TkInter)

---

This document should serve as a comprehensive guide for understanding, installing, and using the Inverter and PLC Controller application.
