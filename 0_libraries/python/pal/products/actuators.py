"""actuators: A module for simplifying interactions
with the Mechatronic Actuators Trainer platform.

This module provides a set of API classes and tools to facilitate
working with the Mechatronic Actuators Trainer.
It is designed to make it easy to read and write all available
inputs/outputs of the device. 4 instances of the class are needed for
the 4 available blocks in the product.
"""

import sys
import time

import numpy as np
from quanser.hardware import (HIL, HILError,
                              MAX_STRING_LENGTH, Clock,
                              DigitalState, IntegerProperty)
from quanser.hardware.enumerations import BufferOverflowMode

class ActuatorsTrainer():

    '''A class to configure Quanser's Mechatronic Actuators Trainer'''

    def __init__(
            self,
            block=0,
            id=0,
            readMode=0,
            frequency=200,
            servoMode=0,
            brushedDCLimit=0.7,
            bldcSensorless = 0,
            boardSpecificOptions=''):

        """
        Initializes and configures the Mechatronic Actuators Trainer.

        Parameters
        ----------
        block : int, optional
            Block identifier, matches the Block numbers printed on the product.
            Defaults to 0.
        id : int, optional
            Board identifier number. Defaults to 0.
            Used when more than 1 Actuators Trainer is connected.
        frequency : int, optional
            Sampling frequency. Used when readMode is set to 1.
            Defaults to 200.
        readMode : int, optional
            Indicates the read mode. Defaults to 0.
            (0 for immediate I/O, 1 for task-based I/O).
        servoMode : int, optional
            Indicates the range for the PWM signal that drives the Servo.
            This range gets mapped to a 0 to 1 PWM input in the device.
            Defaults to 0. (0 for 0.5 to 2.5ms, 1 for 1 to 2ms).
            Used only when boardSpecificOptions is empty, if not, set as part
            of that string.
        bldcSensorless : int, optional
            Indicates if the BLDC motor is used in sensorless mode.
            Defaults to 0. (0 for Hall sensor mode, 1 for sensorless mode).
            When 0, all 3 BLDC motor outputs (A, B and C) are directly derived
            by 3 PWM channels. When 1, the board is configured for sensorless
            operation. Only a single PWM output is used as a bidirectional
            input to drive the BLDC motor. Motor enable still needs to be used.
        boardSpecificOptions : str, optional
            Board-specific configuration options. Defaults to an empty string.
            If modified, `servoMode` will not be read, if it needs to be
            defined, use `servo_pwm_range` in this string, it
            will default to 0 if not defined here.

        Raises
        ------
        HILError
            If the board is not valid or there is a configuration error.
        """

        # high_priority()

        if not boardSpecificOptions:
            # if empty BSO, use defaults
            boardSpecificOptions = (
                "supply_voltage_low_limit=10.0;"
                "supply_voltage_high_limit=16.0;"
                "supply_current_high_limit=8.0;"
                "dc_motor_current_high_limit=1.1;"
                "servo_motor_current_high_limit=1.3;"
                "bldc_motor_current_high_limit=2.0;"
                "stepper_motor_current_high_limit=1.7;"
                f"servo_pwm_range={servoMode};enc_dir=0;"
                f"bldc_motor_mode={bldcSensorless};"
                "bldc_start_tc=0.03;"
                "bldc_start_target=1200"
                )

        self._boardSpecificOptions = boardSpecificOptions
        self._frequency = frequency
        self._readMode = readMode
        self._id = id
        self._block = block
        self._brushedDCLimit = np.clip(brushedDCLimit, 0, 1)

        boardIdentifier = f"{self._id}.{self._block}"

        # region: Channel and internal Buffer definitions

        # Define read/write channels and buffers
        self.WRITE_DIGITAL_CHANNELS = np.array([0, 1, 2, 3, 4, 5, 6],
                                               dtype=np.uint32)
        self.WRITE_PWM_CHANNELS = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                                           dtype=np.uint32)

        self.states = np.array([DigitalState.LOW]
                               * len(self.WRITE_DIGITAL_CHANNELS),
                               dtype=np.int32)

        self.dutyCycles = np.array([0.0]
                                   * len(self.WRITE_PWM_CHANNELS),
                                   dtype=np.float64)

        # Internal write buffers
        self._writeDigitalBuffer = np.zeros(
            len(self.WRITE_DIGITAL_CHANNELS),
            dtype=np.int8)
        self._writePWMBuffer = np.zeros(
            len(self.WRITE_PWM_CHANNELS),
            dtype=np.float64)

        self.READ_ANALOG_CHANNELS = np.array([0, 1, 2, 3, 4, 5, 6,
                                             7, 8, 9, 10, 11],
                                             dtype=np.uint32)
        self.READ_DIGITAL_CHANNELS = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                              10, 11, 12, 13, 14, 15, 16, 17],
                                              dtype=np.uint32)
        self.READ_ENCODER_CHANNELS = np.array([0],
                                              dtype=np.uint32)
        self.READ_OTHER_CHANNELS = np.array([10000, 14000, 14001],
                                            dtype=np.uint32)

        # Internal read buffers
        self._readAnalogBuffer = np.zeros(
            len(self.READ_ANALOG_CHANNELS),
            dtype=np.float64)
        self._readDigitalBuffer = np.zeros(
            len(self.READ_DIGITAL_CHANNELS),
            dtype=np.int8)
        self._readEncoderBuffer = np.zeros(
            len(self.READ_ENCODER_CHANNELS),
            dtype=np.int32)
        self._readOtherBuffer = np.zeros(
            len(self.READ_OTHER_CHANNELS),
            dtype=np.float64)
        # endregion

        # region: External read buffers

        # analog channel
        self.supplyCurrent = np.zeros(1, dtype=np.float64)
        self.supplyVoltage = np.zeros(1, dtype=np.float64)
        self.servoCurrent = np.zeros(1, dtype=np.float64)
        self.dcMotorCurrent = np.zeros(1, dtype=np.float64)
        self.bldcCurrent = np.zeros(3, dtype=np.float64)  # Channel A,B,C
        self.bldcVoltage = np.zeros(3, dtype=np.float64)  # Channel A,B,C
        self.stepperCurrent = np.zeros(2, dtype=np.float64)  # Channel A, B

        # encoder channel
        self.encoder = np.zeros(1, dtype=np.int32)

        # digital channel
        self.hallSensor = np.zeros(3, dtype=np.float64)
        self._deviceErrors = np.zeros(15, dtype=np.float64)
        self._deviceErrorsCount = np.zeros(15, dtype=np.float64)

        # other channel
        self.temperature = np.zeros(1, dtype=np.float64)
        self.tach = np.zeros(1, dtype=np.float64)
        self.sensorlessTach = np.zeros(1, dtype=np.float64)

        # endregion

        try:
            # Open the Card
            self.card = HIL("mech_actuators_trainer_usb", boardIdentifier)

            if self.card.is_valid():
                self.card.set_card_specific_options(
                    self._boardSpecificOptions,
                    MAX_STRING_LENGTH)

                self.card.set_encoder_counts(
                    self.READ_ENCODER_CHANNELS,
                    len(self.READ_ENCODER_CHANNELS),
                    np.zeros(len(self.READ_ENCODER_CHANNELS), dtype=np.int32))

                # check firmware
                properties = np.array([IntegerProperty.FIRMWARE_BUILD], dtype=np.int32)

                num_properties = len(properties)
                buffer = np.zeros(num_properties, dtype=np.int32)
                self.card.get_integer_property(properties, num_properties, buffer)
                # print(buffer)
                self._firmwareBuild = buffer

                self.card.watchdog_set_pwm_expiration_state(
                    self.WRITE_PWM_CHANNELS,
                    len(self.WRITE_PWM_CHANNELS),
                    self.dutyCycles)
                self.card.watchdog_set_digital_expiration_state(
                    self.WRITE_DIGITAL_CHANNELS,
                    len(self.WRITE_DIGITAL_CHANNELS),
                    self.states)

                self.card.watchdog_clear()
                self.card.watchdog_stop()

                # period = 1/self._frequency
                self.card.watchdog_start(0.2)

                if self._readMode == 1:
                    # Task based Read setup

                    self.samples = HIL.INFINITE
                    self.samplesToRead = 1
                    self._readTask = self.card.task_create_reader(
                        int(self._frequency),
                        self.READ_ANALOG_CHANNELS,
                        len(self.READ_ANALOG_CHANNELS),
                        self.READ_ENCODER_CHANNELS,
                        len(self.READ_ENCODER_CHANNELS),
                        self.READ_DIGITAL_CHANNELS,
                        len(self.READ_DIGITAL_CHANNELS),
                        self.READ_OTHER_CHANNELS,
                        len(self.READ_OTHER_CHANNELS)
                    )

                    # Set buffer overflow mode for hardware
                    self.card.task_set_buffer_overflow_mode(
                        self._readTask,
                        BufferOverflowMode.OVERWRITE_ON_OVERFLOW
                    )

                    self.card.task_start(
                        self._readTask,
                        Clock.HARDWARE_CLOCK_0,
                        self._frequency,
                        self.samples
                    )

                self.enable_motors()#False, False, False, False)

            self._startTime = time.time()
            self._checkError = False
            self._HilError = False

        except HILError as h:
            self._HilError = True  # Flag to know if error was HIL
            print('Make sure your device is powered and connected to your PC')
            print(h.get_error_message())
            sys.exit()

    def enable_motors(self, servo=True, dc=True, bldc=True, stepper=True):
        """
        Enables the motors in the Mechatronic Actuators Trainer.

        Parameters
        ----------
        servo : bool, optional
            Enable the servo motor. Defaults to True.
        dc : bool, optional
            Enable the DC motor. Defaults to True.
        bldc : bool, optional
            Enable the BLDC motor. Defaults to True.
        stepper : bool, optional
            Enable the stepper motor. Defaults to True.
        """

        servo = int(servo)
        dc = int(dc)
        bldc = int(bldc)
        stepper = int(stepper)

        self._writeDigitalBuffer[0] = servo
        self._writeDigitalBuffer[1] = dc
        self._writeDigitalBuffer[2] = bldc
        self._writeDigitalBuffer[3] = bldc
        self._writeDigitalBuffer[4] = bldc
        self._writeDigitalBuffer[5] = stepper
        self._writeDigitalBuffer[6] = stepper

        try:
            self.card.write_digital(
                self.WRITE_DIGITAL_CHANNELS,
                len(self.WRITE_DIGITAL_CHANNELS),
                np.array(self._writeDigitalBuffer, dtype=np.int8)
            )
        except HILError as h:
            self._HilError = True  # Flag to know if error was HIL
            raise

    def enable_bldc(self, coils):
        """
        Enables the BLDC (Brushless DC) motor.
        Useful when controlling the BLDC by individual steps.
        To drive the BLDC, two phases need to be enabled.
        The other one will be 'floating'.
        Use alongside `update_bldc` for correct usage.


        Parameters
        ----------
        coils : array_like, bool
            Array of enable values for the BLDC motor coils [A, B, C].

        Raises
        ------
        ValueError
            If the `coils` array does not have exactly 3 elements.
        """

        if len(coils) != 3:
            raise ValueError("coils must be a 3 element array for BLDC motors")

        self._writeDigitalBuffer[2] = int(coils[0])
        self._writeDigitalBuffer[3] = int(coils[1])
        self._writeDigitalBuffer[4] = int(coils[2])

        try:
            self.card.write_digital(
                self.WRITE_DIGITAL_CHANNELS,
                len(self.WRITE_DIGITAL_CHANNELS),
                np.array(self._writeDigitalBuffer, dtype=np.int8)
            )
        except HILError as h:
            self._HilError = True  # Flag to know if error was HIL
            raise
        except Exception as e:
            print(e)

    def write_motors(self):
        """
        Writes the current motor commands to the Mechatronic Actuators Trainer.
        Note: Use the individual update_name motor functions
        before using this function, this function sends the commands
        to the motors all at once.

        Raises
        ------
        HILError
            If there is an error during the write operation.
        """
        # use individual update functions first
        # IO
        self.card.watchdog_reload()
        try:

            # Writes: PWM Channel, Num PWM Channel, PWM Buffer
            self.card.write_pwm(self.WRITE_PWM_CHANNELS,
                                len(self.WRITE_PWM_CHANNELS),
                                self._writePWMBuffer)

        except HILError as h:
            self._HilError = True  # Flag to know if error was HIL
            raise

    def update_servo(self, cmd=0.5):
        """
        Updates the servo motor command.
        The 0 to 1 command maps to a 0.5 to 2.5 ms servo command or
        a 1 to 2 ms command depending on `servoMode` at initialization.

        After updating values, use `write_motors()` to send
        the command to the motors.

        Parameters
        ----------
        cmd : float, optional
            Command value for the servo motor. Must be between 0 and 1.
            Defaults to 0.5.
        """

        cmd = np.clip(cmd, 0, 1)
        self._writePWMBuffer[0] = cmd

    def update_dc(self,  cmd=0, limitCmd = True):
        """
        Updates the DC motor command.
        The command value  of -1 to 1 maps to a voltage range of ±12V or
        the voltage provided by the connected supply.
        After updating values, use `write_motors()` to send
        the command to the motors.

        Parameters
        ----------
        cmd : float, optional
            Command value for the DC motor. Must be between -1 and 1.
            Defaults to 0.
        limitCmd : bool, optional
            If True, limits the command value to the range [-0.7, 0.7].
            If False, allows the full range [-1, 1]. Defaults to True.
        """

        if limitCmd:
            cmd = np.clip(cmd, -self._brushedDCLimit, self._brushedDCLimit)
        else:
            cmd = np.clip(cmd, -1, 1)

        if cmd < 0:
            self._writePWMBuffer[1] = 0
            self._writePWMBuffer[2] = abs(cmd)
        else:
            self._writePWMBuffer[1] = cmd
            self._writePWMBuffer[2] = 0

    def update_dc_individual(self, left=0, right=0):
        """
        Updates the DC motor commands individually for left and right channels.
        -1 to 1 range maps to ±12V or the voltage provided by the connected supply.
        This function is not recommended, it only exists for teaching purposes,
        for normal usage, use `update_dc()` function directly.
        After updating values, use `write_motors()` to send
        the command to the motors.

        Parameters
        ----------
        left : float, optional
            Command value for the left channel (A) of the motor.
            Must be between -0.7 and 0.7. Defaults to 0.
        right : float, optional
            Command value for the right channel (B) of the motor.
            Must be between -0.7 and 0.7. Defaults to 0.
        """

        left = np.clip(left, 0, 1.0)
        right = np.clip(right, 0, 1.0)

        self._writePWMBuffer[1] = left
        self._writePWMBuffer[2] = right

    def update_bldc(self, coils):
        """
        Updates the BLDC motor commands.
        Use alongside `enable_bldc()` for correct usage.
        After updating values, use `write_motors()` to send
        the command to the motors.
        The command value  of -1 to 1 maps to a voltage range of ±12V or
        the voltage provided by the connected supply.

        Parameters
        ----------
        coils : array_like
            Array of command values for the BLDC motor coils [A, B, C].

        Raises
        ------
        ValueError
            If the `coils` array does not have exactly 3 elements.
        """

        if len(coils) != 3:
            raise ValueError("coils must be a 3 element array for BLDC motors")

        self._writePWMBuffer[3] = coils[0]
        self._writePWMBuffer[4] = coils[1]
        self._writePWMBuffer[5] = coils[2]

    def update_bldc_sensorless(self, pwm):
        """
        Updates the BLDC motor command when using sensorless mode.
        This will only work when init parameters are correctly set.
        In this mode, `enable_bldc` does not need to be used,
        enabling bldc once using `enable_motors` is enough.

        After updating values, use `write_motors()` to send
        the command to the motors.

        The command value  of -1 to 1 maps to a voltage range of ±12V or
        the voltage provided by the connected supply.

        Parameters
        ----------
        pwm : float
            Command value for the the motor.
            Must be between -1 and 1.

        Notes
        -----
        For speed information, use `sensorlessTach`, which
        imitates a hardware tach.
        """

        pwm = np.clip(pwm, -1, 1)
        self._writePWMBuffer[3] = pwm

    def update_stepper(self, coils):
        """
        Updates the stepper motor commands.
        After updating values, use `write_motors()` to send
        the command to the motors.

        The command value  of -1 to 1 maps to a voltage range of ±12V or
        the voltage provided by the connected supply.

        Parameters
        ----------
        coils : array_like
            Array of command values for the stepper motor coils
            [A_pos, A_neg, B_pos, B_neg].

        Raises
        ------
        ValueError
            If the `coils` array does not have exactly 4 elements.
        """

        if len(coils) != 4:
            raise ValueError(
                "coils must be a 4 element array for stepper motors")

        self._writePWMBuffer[6] = coils[0]
        self._writePWMBuffer[7] = coils[1]
        self._writePWMBuffer[8] = coils[2]
        self._writePWMBuffer[9] = coils[3]

    def read_outputs(self):
        """
        Reads all outputs for the Mechatronic Actuators Trainer.
        Also reloads the watchdog timer so it does trigger watchdog error.

        Raises
        ------
        HILError
            If there is an error during the read operation.

        Notes
        -----
        This function updates the following variables:
        - self.encoder (float): Measured encoder position (counts)

        - self.temperature (float): Temperature (C)
        - self.tach (float): Tachometer (counts/s)
        - self.sensorlessTach (float): Tachometer for sensorless BLDC drive (counts/s)

        - self.hallSensor (ndarray, float): Hall/encoder sensor pulses
            [A, B, C]
        - self._deviceErrors (ndarray, float): 15 possible device errors. Handled
            automatically.

        - self.supplyCurrent (float): Power Supply Current (A)
        - self.supplyVoltage (float): Power Supply Voltage (V)
        - self.servoCurrent (float): Servo Motor Current (A)
        - self.dcMotorCurrent (float): DC Motor Current (A)
        - self.bldcCurrent (ndarray, float): BLDC Motor Channel Current (A)
            [A, B, C]
        - self.bldcVoltage (ndarray, float): BLDC Motor Channel Voltage (V)
            [A, B, C]
        - self.stepperCurrent (ndarray, float): Stepper Motor
            Channel Current (A) [A, B]
        """
        self.card.watchdog_reload()
        try:
            if self._readMode == 1:
                self.card.task_read(
                    self._readTask,
                    self.samplesToRead,
                    self._readAnalogBuffer,
                    self._readEncoderBuffer,
                    self._readDigitalBuffer,
                    self._readOtherBuffer
                )

            else:
                self.card.read(
                    self.READ_ANALOG_CHANNELS,
                    len(self.READ_ANALOG_CHANNELS),
                    self.READ_ENCODER_CHANNELS,
                    len(self.READ_ENCODER_CHANNELS),
                    self.READ_DIGITAL_CHANNELS,
                    len(self.READ_DIGITAL_CHANNELS),
                    self.READ_OTHER_CHANNELS,
                    len(self.READ_OTHER_CHANNELS),
                    self._readAnalogBuffer,
                    self._readEncoderBuffer,
                    self._readDigitalBuffer,
                    self._readOtherBuffer
                )

        except HILError as h:
            self._HilError = True  # Flag to know if error was HIL
            raise

        finally:
            # encoder channel
            self.encoder = self._readEncoderBuffer[0]

            # other channel
            self.temperature = self._readOtherBuffer[0]
            self.tach = self._readOtherBuffer[1]
            self.sensorlessTach = self._readOtherBuffer[2]

            # digital channel
            # Sensor output A, B, C
            self.hallSensor = self._readDigitalBuffer[0:3]
            # 15 possible errors
            self._deviceErrors = self._readDigitalBuffer[3:]

            # analog channel
            self.supplyCurrent = self._readAnalogBuffer[0]
            self.supplyVoltage = self._readAnalogBuffer[1]
            self.servoCurrent = self._readAnalogBuffer[2]
            self.dcMotorCurrent = self._readAnalogBuffer[3]
            self.bldcCurrent = self._readAnalogBuffer[4:7]  # Channel A,B,C
            self.bldcVoltage = self._readAnalogBuffer[7:10]  # Channel A,B,C
            self.stepperCurrent = self._readAnalogBuffer[10:]  # Channel A, B

            self._error_handler()

    def _error_handler(self):
        """
        Handler for errors in the Mechatronic Actuators Trainer.

        This function iterates through the `_deviceErrors` array to
        identify any active errors. If an error is detected, it prints
        the corresponding error message and raises a `HILError` exception.

        Raises
        ------
        HILError
            Raised when an error is detected in the `_deviceErrors` array, with
            the corresponding error message.
        """
        if self._checkError:

            # samples needed for 20 milliseconds
            milis20 = np.ceil(self._frequency * 0.02)

            self._deviceErrorsCount = (
                self._deviceErrorsCount + self._deviceErrors) * self._deviceErrors

            # if np.any(self._deviceErrorsCount):
            #     print(f'Error add: {self._deviceErrorsCount} in Block {self._block}')

            # Mapping of error indices to error messages
            error_messages = {
                0: 'Power Supply Voltage Too Low',
                1: 'Power Supply Voltage Too High',
                2: 'Power Supply Current Too High',
                3: 'DC Motor Current Too High',
                4: 'DC Motor Driver Over-Current/Temperature',
                5: 'Servomotor Supply Current Too High',
                6: 'Servomotor Supply Voltage Out of Range (5V supply fault)',
                7: 'BLDC Channel A Current Too High',
                8: 'BLDC Channel B Current Too High',
                9: 'BLDC Channel C Current Too High',
                10: 'Stepper Channel A Winding Current Too High',
                11: 'Stepper Channel B Winding Current Too High',
                12: 'Stepper Channel A Driver Over-Current/Temperature',
                13: 'Stepper Channel B Driver Over-Current/Temperature',
                14: 'Device Over-Temperature'
            }
            # Iterate through the error indices and check for errors
            for index, message in error_messages.items():
                if self._deviceErrorsCount[index] >= milis20:
                    print(f'Error found by _error_handler(): {message} in Block {self._block}')
                    print('Stopping program to avoid damage to Actuators Trainer.')
                    self.card.watchdog_stop()
                    time.sleep(0.2)
                    raise UserWarning(message)
        else:
            if time.time() - self._startTime > 0.3:
                self._checkError = True

    def terminate(self):
        """
        Cleanly shuts down and terminates the connection with
        the Mechatronic Actuators Trainer.

        Terminates the device after disabling all motors and stops
        any active tasks.
        """

        try:
            if not self._HilError:
                # if its a HIL error, it will most likely
                # not be able to terminate properly
                self.enable_motors(False, False, False, False)

                if self._readMode == 1:
                    self.card.task_stop(self._readTask)
                    self.card.task_delete(self._readTask)

                self.card.watchdog_clear()
                self.card.watchdog_stop()
                self.card.close()
                print(f'Actuators Trainer Block {self._block} closed gracefully.')

        except HILError as h:
            print('Error during termination/closing.')
            print('Try restarting the device if needed.')
            print(h.get_error_message())

    def __enter__(self):
        """
        Used for the `with` statement.

        Returns
        -------
        ActuatorsTrainer
            The current instance of the class.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Used for the `with` statement.
        Ensures cleanup and terminates the connection
        with the Mechatronic Actuators Trainer.
        Catches KeyboardInterrupt and HILError exception
        types to not propagate the error.

        Parameters
        ----------
        exc_type : Exception type
            The exception type, if any.
        exc_value : Exception value
            The exception value, if any.
        traceback : Traceback
            The traceback object, if any.
        """

        # Suppress KeyboardInterrupt and HIL error.
        # Error description should be enough.
        if exc_type is KeyboardInterrupt:
            print("KeyboardInterrupt handled. Cleaning up.")
            self.terminate()
            return True  # Suppress the exception

        if exc_type is HILError:
            self._HilError = True
            print(
                f"HILError occurred during termination: "
                f"{exc_value.get_error_message()}"
            )
            print('Try restarting the device if needed.')
            self.terminate()
            return True  # Suppress the exception

        if exc_type is UserWarning:
            self.terminate()
            return True  # Suppress the exception

        # If another exception occurred, handle it
        if exc_type is not None:
            print(f"Exception occurred: {exc_type.__name__}: {exc_value}")

        # Always terminate the connection
        self.terminate()

        # Returning False allows other exceptions to propagate
        # for example, if error is ValueError,
        # traceback helps to pinpoint the error
        return False

# def high_priority():
#     """
#     Sets the priority of the process to high priority.

#     Notes
#     -----
#     On Windows, this sets the process priority to HIGH_PRIORITY_CLASS.
#     On other operating systems, it adjusts the process niceness.
#     """
#     platform = sys.platform
#     isWindows = True if platform == 'win32' else False

#     if isWindows:
#         import win32api
#         import win32process
#         import win32con

#         pid = win32api.GetCurrentProcessId()
#         handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS,
#                                       True,
#                                       pid)
#         win32process.SetPriorityClass(handle,
#                                       win32process.HIGH_PRIORITY_CLASS)
#     else:
#         # os.nice(-15)
#         pass
