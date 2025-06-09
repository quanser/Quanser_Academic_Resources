"""gamepad: A module for simplifying interactions with gamepads (controllers).

This module provides classes and utilities to facilitate working with common
types of gamepads, such as the Logitech F710. It is designed to make it easy
to interface with these devices, read their states, and manage their
connections.
"""
from quanser.devices import GameController
import numpy as np
import platform


class LogitechF710:
    """Class for interacting with the Logitech Gamepad F710.

    This class opens a GameController device and establishes a connection
    to it. It provides methods for reading gamepad states and terminating
    the connection.

    Attributes:
        system (str): The current operating system name.
        mode (int): The gamepad mapping mode, depending on the OS.
        flag (bool): A flag used for trigger updates.
        leftJoystickX (float): Left joystick right/left value.
        leftJoystickY (float): Left joystick up/down value.
        rightJoystickX (float): Right joystick right/left value.
        rightJoystickY (float): Right joystick up/down value.
        trigger (float): Trigger value.
        buttonA (int): Button A state.
        buttonB (int): Button B state.
        buttonX (int): Button X state.
        buttonY (int): Button Y state.
        buttonLeft (int): Left button state.
        buttonRight (int): Right button state.
        up (int): Up arrow state.
        right (int): Right arrow state.
        left (int): Left arrow state.
        down (int): Down arrow state.
    """

    system = platform.system()

    if system == 'Windows':
        mode = 0
    elif system == 'Linux':
        mode = 1
    else:
        mode = -1

    flag = False

    # Continuous axis
    leftJoystickX = 0
    leftJoystickY = 0
    rightJoystickX = 0
    rightJoystickY = 0
    trigger = 0

    # Buttons
    buttonA = 0
    buttonB = 0
    buttonX = 0
    buttonY = 0
    buttonLeft = 0
    buttonRight = 0

    # Arrow keys
    up = 0
    right = 0
    left = 0
    down = 0

    def __init__(self, deviceID=1):
        """Initialize and open a connection to a LogitechF710 GameController.
        """
        self.gameController = GameController()
        self.gameController.open(deviceID)

    def read(self):
        """Update the gamepad states by polling the GameController.

        The updated states are:
        Continuous:
            leftJoystickX: Left Joystick (up/down) (-1 to 1)
            leftJoystickY: Left Joystick (right/left) (-1 to 1)
            rightJoystickX: Right Joystick (up/down) (-1 to 1)
            rightJoystickY: Right Joystick (right/left) (-1 to 1)
            trigger: Left and right triggers
                (0.5 -> 0 for right trigger, 0.5 -> 1 for left trigger)

        Buttons:
            buttonA, buttonB, buttonX, buttonY, buttonLeft, buttonRight
            up, right, down, left
        """
        data, new = self.gameController.poll()

        # Update the lateral and longitudinal axis
        self.leftJoystickX = -1 * data.x
        self.leftJoystickY = -1 * data.y
        self.rightJoystickX = -1 * data.rx
        self.rightJoystickY = -1 * data.ry

        # Trigger mapping for a Windows-based system
        if self.mode == 0:
            if data.z == 0 and not self.flag:
                self.trigger = 0
            else:
                self.trigger = 0.5 + 0.5 * data.z
                self.flag = True

        # Trigger mapping for a Linux-based system
        if self.mode == 1:
            if data.rz == 0 and not self.flag:
                self.trigger = 0
            else:
                self.trigger = 0.5 + 0.5 * data.rz
                self.flag = True

        # Update the buttons
        self.buttonA = int(data.buttons & (1 << 0))
        self.buttonB = int((data.buttons & (1 << 1)) / 2)
        self.buttonX = int((data.buttons & (1 << 2)) / 4)
        self.buttonY = int((data.buttons & (1 << 3)) / 8)
        self.buttonLeft = int((data.buttons & (1 << 4)) / 16)
        self.buttonRight = int((data.buttons & (1 << 5)) / 32)

        # Update the arrow keys
        val = 180 * data.point_of_views[0] / np.pi
        self.up = 0
        self.right = 0
        self.left = 0
        self.down = 0
        if val >= 310 or (val >= 0 and val < 50):
            self.up = 1
        if val >= 40 and val < 140:
            self.right = 1
        if val >= 130 and val < 230:
            self.down = 1
        if val >= 220 and val < 320:
            self.left = 1

        return new

    def terminate(self):
        """Terminate the GameController connection."""
        self.gameController.close()
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.terminate()