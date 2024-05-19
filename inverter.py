import can
import time
import threading
import logging
import socket
import snap7
from snap7.util import *
from snap7.types import *
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Define CAN message IDs and data formats
SYSTEM_STATE_ID = 0x101
CONTROL_MODE_ID = 0x102
TORQUE_SETPOINT_ID = 0x103
ENABLE_DRIVE_ID = 0x104
DIR_ROTATION_SELECTION_ID = 0x105
STATUS_ID = 0x201
FAULT_ID = 0x202
CURRENT_ID = 0x203
SPEED_ID = 0x204
TORQUE_ID = 0x205

# PLC Communication settings
PLC_IP = '192.168.0.1'
PLC_RACK = 0
PLC_SLOT = 1
PLC_PORT = 102

# Setup logging
logging.basicConfig(level=logging.INFO)

class InverterController:
    def __init__(self, channel='can0', bustype='socketcan'):
        try:
            self.bus = can.interface.Bus(channel=channel, bustype=bustype)
        except can.CanError as e:
            logging.error(f"Error initializing CAN interface: {e}")
            exit(1)
        self.notifier = can.Notifier(self.bus, [self.receive_message])

    def send_message(self, message_id, data):
        message = can.Message(arbitration_id=message_id, data=data, is_extended_id=False)
        try:
            self.bus.send(message)
            logging.info(f'Sent CAN message: {message_id} data: {data}')
        except can.CanError as e:
            logging.error(f"Error sending message with ID {message_id}: {e}")

    def receive_message(self, msg):
        if msg.arbitration_id == STATUS_ID:
            self.handle_status_message(msg.data)
        elif msg.arbitration_id == FAULT_ID:
            self.handle_fault_message(msg.data)
        elif msg.arbitration_id == CURRENT_ID:
            app.update_graph("Current", msg.data)
        elif msg.arbitration_id == SPEED_ID:
            app.update_graph("Speed", msg.data)
        elif msg.arbitration_id == TORQUE_ID:
            app.update_graph("Torque", msg.data)
        else:
            logging.info(f"Received message with ID {msg.arbitration_id}: {msg.data}")

    def handle_status_message(self, data):
        state = data[0]
        logging.info(f"Status - System State: {state}")
        app.update_status(f"System State: {state}")

    def handle_fault_message(self, data):
        fault_code = data[0]
        logging.info(f"Fault - Code: {fault_code}")
        app.update_status(f"Fault - Code: {fault_code}")

    def set_system_state(self, state):
        data = [state] + [0] * 7
        self.send_message(SYSTEM_STATE_ID, data)

    def set_control_mode(self, mode):
        data = [mode] + [0] * 7
        self.send_message(CONTROL_MODE_ID, data)

    def set_torque_setpoint(self, torque):
        data = list(torque.to_bytes(2, byteorder='big')) + [0] * 6
        self.send_message(TORQUE_SETPOINT_ID, data)

    def enable_drive(self, enable):
        data = [enable] + [0] * 7
        self.send_message(ENABLE_DRIVE_ID, data)

    def set_direction_of_rotation(self, direction):
        data = [direction] + [0] * 7
        self.send_message(DIR_ROTATION_SELECTION_ID, data)

class PLCController:
    def __init__(self, ip, rack, slot):
        self.client = snap7.client.Client()
        self.client.connect(ip, rack, slot)
        if not self.client.get_connected():
            logging.error(f"Error connecting to PLC at {ip}")
            exit(1)
        logging.info("Connected to PLC")

    def write_output(self, byte_index, bit_index, value):
        try:
            data = self.client.read_area(areas['PA'], 0, byte_index, 1)
            set_bool(data, 0, bit_index, value)
            self.client.write_area(areas['PA'], 0, byte_index, data)
            logging.info(f"Output {byte_index}.{bit_index} set to {value}")
        except Exception as e:
            logging.error(f"Error writing to PLC: {e}")

    def read_input(self, byte_index, bit_index):
        try:
            data = self.client.read_area(areas['PE'], 0, byte_index, 1)
            value = get_bool(data, 0, bit_index)
            logging.info(f"Input {byte_index}.{bit_index} is {value}")
            return value
        except Exception as e:
            logging.error(f"Error reading from PLC: {e}")

    def disconnect(self):
        self.client.disconnect()
        logging.info("Disconnected from PLC")

class App:
    def __init__(self, root, inverter, plc):
        self.root = root
        self.root.title("Inverter and PLC Controller")
        self.inverter = inverter
        self.plc = plc

        self.status_var = tk.StringVar()
        self.status_var.set("Status: Ready")

        self.graph_data = {
            "Current": [],
            "Speed": [],
            "Torque": []
        }

        self.fig, self.axs = plt.subplots(3, 1, figsize=(6, 8))
        self.graph_lines = {
            "Current": self.axs[0].plot([], [])[0],
            "Speed": self.axs[1].plot([], [])[0],
            "Torque": self.axs[2].plot([], [])[0]
        }
        self.graph_labels = ["Current", "Speed", "Torque"]

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=8, column=0, columnspan=3)

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        # System State
        tk.Label(self.root, text="System State:").grid(row=0, column=0)
        self.system_state = tk.Entry(self.root)
        self.system_state.grid(row=0, column=1)
        tk.Button(self.root, text="Set System State", command=self.set_system_state).grid(row=0, column=2)

        # Control Mode
        tk.Label(self.root, text="Control Mode:").grid(row=1, column=0)
        self.control_mode = tk.Entry(self.root)
        self.control_mode.grid(row=1, column=1)
        tk.Button(self.root, text="Set Control Mode", command=self.set_control_mode).grid(row=1, column=2)

        # Torque Setpoint
        tk.Label(self.root, text="Torque Setpoint:").grid(row=2, column=0)
        self.torque_setpoint = tk.Entry(self.root)
        self.torque_setpoint.grid(row=2, column=1)
        tk.Button(self.root, text="Set Torque Setpoint", command=self.set_torque_setpoint).grid(row=2, column=2)

        # Enable Drive
        tk.Label(self.root, text="Enable Drive:").grid(row=3, column=0)
        self.enable_drive = tk.Entry(self.root)
        self.enable_drive.grid(row=3, column=1)
        tk.Button(self.root, text="Enable Drive", command=self.enable_drive_func).grid(row=3, column=2)

        # Direction of Rotation
        tk.Label(self.root, text="Direction of Rotation:").grid(row=4, column=0)
        self.direction_of_rotation = tk.Entry(self.root)
        self.direction_of_rotation.grid(row=4, column=1)
        tk.Button(self.root, text="Set Direction", command=self.set_direction_of_rotation).grid(row=4, column=2)

        # Status
        self.status_label = tk.Label(self.root, textvariable=self.status_var)
        self.status_label.grid(row=5, column=0, columnspan=3)

        # PLC Control
        tk.Button(self.root, text="Activate PLC Output", command=self.activate_plc_output).grid(row=6, column=0, columnspan=3)
        tk.Button(self.root, text="Read PLC Input", command=self.read_plc_input).grid(row=7, column=0, columnspan=3)

    def set_system_state(self):
        try:
            state = int(self.system_state.get())
            self.inverter.set_system_state(state)
            self.update_status(f"System State set to {state}")
        except ValueError:
            self.update_status("Invalid System State value")

    def set_control_mode(self):
        try:
            mode = int(self.control_mode.get())
            self.inverter.set_control_mode(mode)
            self.update_status(f"Control Mode set to {mode}")
        except ValueError:
            self.update_status("Invalid Control Mode value")

    def set_torque_setpoint(self):
        try:
            torque = int(self.torque_setpoint.get())
            self.inverter.set_torque_setpoint(torque)
            self.update_status(f"Torque Setpoint set to {torque}")
        except ValueError:
            self.update_status("Invalid Torque Setpoint value")

    def enable_drive_func(self):
        try:
            enable = int(self.enable_drive.get())
            self.inverter.enable_drive(enable)
            self.update_status(f"Drive {'enabled' if enable else 'disabled'}")
        except ValueError:
            self.update_status("Invalid Enable Drive value")

    def set_direction_of_rotation(self):
        try:
            direction = int(self.direction_of_rotation.get())
            self.inverter.set_direction_of_rotation(direction)
            self.update_status(f"Direction of Rotation set to {direction}")
        except ValueError:
            self.update_status("Invalid Direction of Rotation value")

    def activate_plc_output(self):
        try:
            self.plc.write_output(0, 0, 1)
            self.update_status("PLC Output 0.0 activated")
        except Exception as e:
            self.update_status(f"Error activating PLC Output: {e}")

    def read_plc_input(self):
        try:
            value = self.plc.read_input(0, 0)
            self.update_status(f"PLC Input 0.0 is {value}")
        except Exception as e:
            self.update_status(f"Error reading PLC Input: {e}")

    def update_status(self, message):
        self.status_var.set(f"Status: {message}")

    def update_graph(self, label, data):
        try:
            value = int.from_bytes(data[:2], byteorder='big')
            self.graph_data[label].append(value)
            self.graph_lines[label].set_xdata(np.arange(len(self.graph_data[label])))
            self.graph_lines[label].set_ydata(self.graph_data[label])
            self.axs[self.graph_labels.index(label)].relim()
            self.axs[self.graph_labels.index(label)].autoscale_view()
            self.canvas.draw()
        except Exception as e:
            logging.error(f"Error updating graph for {label}: {e}")

if __name__ == "__main__":
    controller = InverterController()
    plc = PLCController(PLC_IP, PLC_RACK, PLC_SLOT)

    root = tk.Tk()
    app = App(root, controller, plc)

    # Start the CAN message receiver in a separate thread to avoid blocking the GUI
    def can_receiver():
        while True:
            msg = controller.bus.recv()
            controller.receive_message(msg)
    
    threading.Thread(target=can_receiver, daemon=True).start()

    root.mainloop()
    
    plc.disconnect()
