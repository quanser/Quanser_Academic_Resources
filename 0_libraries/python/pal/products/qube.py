"""qube: A module for simplifying interactions with the Qube Servo platform.

This module provides a set of API classes and tools to facilitate working with
the Qube Servo platform. It is designed to make it easy to read and write
all available inputs/outputs of the Qube Servo.
"""

from quanser.hardware import HIL, HILError, Clock, MAX_STRING_LENGTH
from quanser.hardware.enumerations import BufferOverflowMode
import numpy as np


class __QubeServo():
    """A class to configure Qubes, parent class to QubeServo2 and 3 class.

    """

    def __init__(
            self,
            version,
            id=0,
            hardware=1,
            frequency=500,
            pendulum = 0,
            readMode=1,
            boardSpecificOptions='pwm_en=0'
        ):

        """Initializes and configures the Qube Servo.

        Args:
            version(int): Qube-Servo version. Use 2 or 3 for
                Qube-Servo 2 and Qube-Servo 3 respectively.
            id (str, optional): Board identifier id number. Defaults to '0'.
            hardware (int, optional): Indicates whether to use hardware or virtual
                Qube. (0 for virtual, 1 for hardware). Defaults to 1.
            frequency (int, optional): Sampling frequency
                (used when readMode is set to 1). Defaults to 500.
            pendulum (int, optional): ONLY IF USING VIRTUAL QUBE SERVO.
                (0 if using Qube DC motor, 1 if using Qube Pendulum). Defaults to 0.
            readMode (int, optional): Indicates the read mode.
                (0 for immediate I/O, 1 for task-based I/O). Defaults to 1.
        """

        # Define read/write channels and buffers

        if version == 2:
            card_type = "qube_servo2_usb"
        elif version == 3:
            card_type = "qube_servo3_usb"
        else:
            raise ValueError(
                'Invalid Qube Version, please set to either 2 or 3.'
            )

        self.WRITE_DIGITAL_CHANNELS = np.array([0], dtype=np.uint32)
        self.WRITE_ANALOG_CHANNELS = np.array([0], dtype=np.uint32)
        self.WRITE_OTHER_CHANNELS = np.array(
            [11000, 11001, 11002], dtype=np.uint32)

        self.READ_DIGITAL_CHANNELS = np.array([0, 1, 2], dtype=np.uint32)
        self.READ_ANALOG_CHANNELS = np.array([0], dtype=np.uint32)
        self.READ_ENCODER_CHANNELS = np.array([0,1], dtype=np.uint32)
        # READ_OTHER_CHANNELS varies - it is at each individual Qube class

        # Internal read buffers
        self._readDigitalBuffer = np.zeros(
            len(self.READ_DIGITAL_CHANNELS),
            dtype=np.int8)
        self._readAnalogBuffer = np.zeros(
            len(self.READ_ANALOG_CHANNELS),
            dtype=np.float64)
        self._readEncoderBuffer = np.zeros(
            len(self.READ_ENCODER_CHANNELS),
            dtype=np.int32)
        self._readOtherBuffer = np.zeros(
            len(self.READ_OTHER_CHANNELS),
            dtype=np.float64)

        # External read buffers
        self.motorCurrent = np.zeros(1, dtype=np.float64)

        self.motorCountsPerSecond = np.zeros(1, dtype=np.float64)
        self.motorSpeed = np.zeros(1, dtype=np.float64)

        self.motorEncoderCounts = np.zeros(1, dtype=np.float64)
        self.pendulumEncoderCounts = np.zeros(1, dtype=np.float64)

        self.motorPosition = np.zeros(1, dtype=np.float64)
        self.pendulumPosition = np.zeros(1, dtype=np.float64)

        self.amplifierFault = np.zeros(1, dtype=np.float64)
        self.motorStallDetected = np.zeros(1, dtype=np.float64)
        self.motorStallError = np.zeros(1, dtype=np.float64)


        self._hardware = hardware
        self._readMode = readMode
        self._version = version
        self._id = str(id)
        self._pendulum = pendulum
        self._boardSpecificOptions = boardSpecificOptions

        if self._hardware:
            boardIdentifier = self._id
        elif self._version == 2 and not self._pendulum:
            boardIdentifier = self._id + "@tcpip://localhost:18920?nagle='off'"
        elif self._version == 2 and self._pendulum:
            boardIdentifier = self._id + "@tcpip://localhost:18921?nagle='off'"
        elif self._version == 3 and not self._pendulum:
            boardIdentifier = self._id + "@tcpip://localhost:18922?nagle='off'"
        elif self._version == 3 and self._pendulum:
            boardIdentifier = self._id + "@tcpip://localhost:18923?nagle='off'"
        

        try:
            # Open the Card
            self.card = HIL(card_type, boardIdentifier)

            if self.card.is_valid():
                if version == 3:
                    self.card.set_card_specific_options(
                        self._boardSpecificOptions,
                        MAX_STRING_LENGTH)

                self.card.set_encoder_counts(
                    self.READ_ENCODER_CHANNELS,
                    len(self.READ_ENCODER_CHANNELS),
                    np.zeros(len(self.READ_ENCODER_CHANNELS), dtype=np.int32)
                )

                # Set LEDs to green
                self.write_led([0,1,0])

                # Set motor voltage to 0
                self.write_voltage(0)

                # Enable amplifier
                self.card.write_digital(
                    self.WRITE_DIGITAL_CHANNELS,
                    len(self.WRITE_DIGITAL_CHANNELS),
                    np.array([1], dtype=np.int8)
                )

                if self._readMode == 1:
                    # Task based Read setup
                    self.frequency = frequency
                    self.samples = HIL.INFINITE
                    self.samplesToRead = 1
                    self._readTask = self.card.task_create_reader(
                        int(self.frequency),
                        self.READ_ANALOG_CHANNELS,
                        len(self.READ_ANALOG_CHANNELS),
                        self.READ_ENCODER_CHANNELS,
                        len(self.READ_ENCODER_CHANNELS),
                        self.READ_DIGITAL_CHANNELS,
                        len(self.READ_DIGITAL_CHANNELS),
                        self.READ_OTHER_CHANNELS,
                        len(self.READ_OTHER_CHANNELS)
                    )

                    # Set buffer overflow mode depending on whether
                    # its for hardware or virtual Qube
                    if self._hardware:
                        self.card.task_set_buffer_overflow_mode(
                            self._readTask,
                            BufferOverflowMode.OVERWRITE_ON_OVERFLOW
                        )
                    else:
                        self.card.task_set_buffer_overflow_mode(
                            self._readTask,
                            BufferOverflowMode.SYNCHRONIZED
                        )

                    self.card.task_start(
                        self._readTask,
                        Clock.HARDWARE_CLOCK_0,
                        self.frequency,
                        self.samples
                    )

        except HILError as h:
            print(h.get_error_message())

    def write_voltage(self, voltage):
        """Writes voltage commands to the QUBE.

        Args:
            voltage (float): Voltage command in Volts
                (saturated to be between +15 & -15 Volts).
        """
        try:

            self.card.write_analog(
                self.WRITE_ANALOG_CHANNELS,
                len(self.WRITE_ANALOG_CHANNELS),
                np.array([1 * np.clip(voltage, -15, 15)],dtype=np.float64)
            )

        except HILError as h:
            print(h.get_error_message())

    def write_led(self, baseLED=np.array([1, 0, 0], dtype=np.float64)):
        """Writes LED values to the QUBE.

        Args:
            baseLED (np.ndarray, optional): 3x1 numpy array of RGB colors.
                0 to 1 intensity for each color.
                Defaults to red (np.array([1, 0, 0], dtype=np.float64)).
        """
        try:
            self.card.write_other(
                self.WRITE_OTHER_CHANNELS,
                len(self.WRITE_OTHER_CHANNELS),
                np.array(baseLED, dtype=np.float64)
            )

        except HILError as h:
            print(h.get_error_message())

    def read_outputs(self):
        """Reads all outputs for the Qube.

        Reads the outputs and stores them in their respective member variables.
        These are the read variables:
        - motorCurrent (Amps)
        - motorCountsPerSecond
        - motorSpeed (rad/s)
        - pendulumCountsPerSecond (Only for Qube-Servo 3)
        - pendulumSpeed (rad/s) (Only for Qube-Servo 3)
        - motorEncoderCounts
        - motorPosition (rad)
        - pendulumEncoderCounts
        - pendulumPosition (rad)
        - amplifierFault: If the amplifer is enabled and this fault occurs,
            the amplifier may be experiencing excessive temperatures and shut
            down to protect itself.
        - motorStallDetected: Occurs when the motor is stalled or excessively
            slowed and the applied voltage (including deadband compensation)
            is greater than 5V.
        - motorStallError: When a stall warning has been asserted continuously
            for approximately 3s.

        """
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
            print(h.get_error_message())
        finally:
            self.motorCurrent = self._readAnalogBuffer

            self.motorCountsPerSecond = self._readOtherBuffer[0]
            self.motorSpeed = self.motorCountsPerSecond * 2*np.pi/2048

            self.motorEncoderCounts =  self._readEncoderBuffer[0]
            self.motorPosition = self.motorEncoderCounts * 2*np.pi/2048

            self.pendulumEncoderCounts = self._readEncoderBuffer[1]
            self.pendulumPosition = self.pendulumEncoderCounts * 2*np.pi/2048

            self.amplifierFault = self._readDigitalBuffer[0]
            self.motorStallDetected =self._readDigitalBuffer[1]
            self.motorStallError = self._readDigitalBuffer[2]

    def terminate(self):
        """Cleanly shutdown and terminate connection with the QUBE

        Terminates the QUBE card after setting final values for voltage and
        LEDs. Also terminates the task reader.
        """
        try:
            self.write_voltage(0)
            self.write_led(np.array([1, 0, 0], dtype=np.float64))

            self.card.write_digital(
                self.WRITE_DIGITAL_CHANNELS,
                len(self.WRITE_DIGITAL_CHANNELS),
                np.array([0], dtype=np.int32)
            )
            if self._readMode == 1:
                self.card.task_stop(self._readTask)
                self.card.task_delete(self._readTask)

            self.card.close()
        except HILError as h:
            print(h.get_error_message())

    def __enter__(self):
        """Used for with statement."""
        return self

    def __exit__(self, type, value, traceback):
        """Used for with statement. Terminates the connection with the QUBE."""
        self.terminate()

class QubeServo2(__QubeServo):
    """Class to set up Qube Servo 2.
    Sets available reading and writing channels
    """

    def __init__(self, id=0, hardware=1, frequency=500,pendulum=0, readMode=1):

        self.READ_OTHER_CHANNELS = np.array([14000], dtype=np.uint32)

        super().__init__(2, id, hardware, frequency, pendulum, readMode)

class QubeServo3(__QubeServo):
    """Class to set up Qube Servo 3.
    Sets available reading and writing channels.
    Has access to a pendulum tachometer not available in the QubeServo 2 class.
    """

    def __init__(
            self,
            id=0,
            hardware=1,
            frequency=500,
            pendulum=0,
            readMode=1,
            boardSpecificOptions='deadband_compensation=0.3;pwm_en=0;enc0_velocity=3.0;enc1_velocity=3.0;min_diode_compensation=0.3;max_diode_compensation=1.5'
        ):

        
        if hardware == 0 and pendulum == 0:
            self.READ_OTHER_CHANNELS = np.array([14000], dtype=np.uint32)
        else:
            self.READ_OTHER_CHANNELS = np.array([14000, 14001], dtype=np.uint32)

        self.pendulumCountsPerSecond = np.zeros(1, dtype=np.float64)
        self.pendulumSpeed = np.zeros(1, dtype=np.float64)

        super().__init__(
            3,
            id,
            hardware,
            frequency,
            pendulum,
            readMode,
            boardSpecificOptions
        )

    def read_outputs(self):
        super().read_outputs()
        if self._hardware == 0 and self._pendulum == 0:
           self.pendulumCountsPerSecond = 0
           self.pendulumSpeed = 0
        else:
            self.pendulumCountsPerSecond = self._readOtherBuffer[1]
            self.pendulumSpeed = self.pendulumCountsPerSecond * 2*np.pi/2048
