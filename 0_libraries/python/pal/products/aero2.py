from quanser.hardware import HIL, HILError, Clock
from quanser.hardware.enumerations import BufferOverflowMode
import numpy as np

class Aero2():
    """
    Aero2 class for initialization, I/O, and termination.

    This class provides an interface to configure and control the Aero2 platform.
    """

    # write channels
    WRITE_ANALOG_CHANNELS = np.array([0, 1], dtype=np.uint32)
    WRITE_DIGITAL_CHANNELS = np.array([0, 1], dtype=np.uint32)
    WRITE_OTHER_CHANNELS = np.array([11000, 11001, 11002], dtype=np.uint32)

    # read channels
    READ_ANALOG_CHANNELS = np.array([0, 1], dtype=np.uint32)
    READ_ENCODER_CHANNELS = np.array([0, 1, 2, 3], dtype=np.uint32)
    READ_OTHER_CHANNELS = np.array([3000, 3001, 3002, 4000, 4001, 4002, 14000, 14001, 14002, 14003], dtype=np.uint32)

    # write buffers
    writeAnalogBuffer = np.array([10, 10], dtype=np.float64)
    writeDigitalBuffer = np.array([1, 1], dtype=np.int8)
    writeOtherBuffer = np.array([1, 0, 0], dtype=np.float64)

    # read buffers (internal)
    readAnalogBuffer = np.zeros(2, dtype=np.float64)
    readEncoderBuffer = np.zeros(4, dtype=np.int32)
    readOtherBufer = np.zeros(10, dtype=np.float64)

    # read buffers (external)
    motorCurrent = np.zeros(2, dtype=np.float64)
    motorPosition = np.array(2, dtype=np.float64)
    pitchAngle, yawAngle = np.zeros(2, dtype=np.float64)
    gyroscope = np.zeros(3, dtype=np.float64)
    accelerometer = np.zeros(3, dtype=np.float64)
    motorSpeed = np.zeros(2, dtype=np.float64)
    pitchRate, yawRate = np.zeros(2, dtype=np.float64)

    def __init__(self, id=0, hardware=0, readMode=1, frequency=500):
        """
        Initializes and configures the Aero2 platform.

        Parameters
        ----------
        id : int, optional
            The board identifier id number. Defaults to 0.
        hardware : int, optional
            0 for virtual Aero2 (requires Quanser Interactive Labs), 1 for hardware Aero2. Defaults to 0.
        readMode : int, optional
            0 for immediate I/O, 1 for task-based I/O. Defaults to 1.
        frequency : int, optional
            Sampling frequency (used when `readMode` is set to 1). Defaults to 500.

        Raises
        ------
        HILError
            If there is an error during initialization.

        Notes
        -----
        - Aero can be used as 1 DOF, where yaw is fixed, pitch is freely moving.
        - In 2-DOF mode, both pitch and yaw are free to move.
        """

        self.card = HIL()
        self._id = str(id)
        self.hardware = hardware
        self.readMode = readMode
        self.frequency = frequency
        self.samples = HIL.INFINITE
        self.samples_to_read = 1

        # select hardware or virtual Aero2
        if self.hardware:
            boardIdentifier = self._id
        else:
            boardIdentifier = self._id+"@tcpip://localhost:18950"
        try:
            # open the Aero2
            self.card.open("quanser_aero2_usb", boardIdentifier)
            if self.card.is_valid():
                # initialize encoder counts
                counts = np.array([0, 0, 0, 0], dtype=np.float64)
                self.card.set_encoder_counts(self.READ_ENCODER_CHANNELS, len(self.READ_ENCODER_CHANNELS), counts)

                # enable writing to motors
                self.card.write_digital(self.WRITE_DIGITAL_CHANNELS,
                                        len(self.WRITE_DIGITAL_CHANNELS),
                                        self.writeDigitalBuffer)
                # task-based I/O setup
                if self.readMode:
                    self.readTask = self.card.task_create_reader(int(self.frequency),
                                                            self.READ_ANALOG_CHANNELS, len(self.READ_ANALOG_CHANNELS),
                                                            self.READ_ENCODER_CHANNELS, len(self.READ_ENCODER_CHANNELS),
                                                            None, 0,
                                                            self.READ_OTHER_CHANNELS, len(self.READ_OTHER_CHANNELS))

                    # set buffer overflow mode for either hardware or virtual Aero2
                    if self.hardware:
                        self.card.task_set_buffer_overflow_mode(self.readTask, BufferOverflowMode.OVERWRITE_ON_OVERFLOW)
                    else:
                        self.card.task_set_buffer_overflow_mode(self.readTask, BufferOverflowMode.WAIT_ON_OVERFLOW)
                    # start read task
                    self.card.task_start(self.readTask, Clock.HARDWARE_CLOCK_0, self.frequency, self.samples)

        except HILError as h:
            print(h.get_error_message())

    def read_analog_encoder_other_channels(self):
        """This function reads sensor information from the 'analog', 'encoder' and 'other' channels of the Aero2.\n

        Returns
        -------
        motorCurrent : array
            An array containing motor_0 and motor_1 currents read from analog channels 0 and 1. The array contains
            two elements, the first element is the current of motor_0 and the second element is the current of motor_1.
        motorPosition : array
            An array containing motor_0 and motor_1 positions read from encoder channels 0 and 1. The array contains
            two elements, the first element is the position of motor_0 and the second element is the position of motor_1.
        pitchAngle : float
            The pitch angle read from encoder channel 2
        yawAngle : float
            The yaw angle read from encoder channel 3
        gyroscope : array
            An array containing the velocity in x, y, z axes read from other channels 3000, 3001, 3002. The array
            contains three elements, the first element is the velocity along x-axis, the second element is the velocity
            along y-axis and the third element is the velocity along the z-axis.
        accelerometer : array
            An array containing acceleration in x, y, z axes read from other channels 4000, 4001, 4002. The array
            contains three elements, the first element is the acceleratoin along x-axis, the second element is the
            acceleration along y-axis and the third element is the acceleration along the z-axis.
        motorSpeed : array
            An array containing motor_0 and motor_0 speeds read from other channels 14000, 14001. The array contains two
            elements, the first element is the speed of motor_0 and the second element is the speed of motor_1.
        pitchRate : float
            The pitch velocity read from other channel 14002
        yawRate : float
            The yaw velocity read from other channel 14003

        """
        try:
            if self.readMode: # use task based I/O
                self.card.task_read(self.readTask, self.samples_to_read,
                                    self.readAnalogBuffer, self.readEncoderBuffer,
                                    None, self.readOtherBufer)
            else: # use immediate I/O
                self.card.read(self.READ_ANALOG_CHANNELS, len(self.READ_ANALOG_CHANNELS),
                                    self.READ_ENCODER_CHANNELS, len(self.READ_ENCODER_CHANNELS),
                                    None, 0,
                                    self.READ_OTHER_CHANNELS, len(self.READ_OTHER_CHANNELS),
                                    self.readAnalogBuffer,
                                    self.readEncoderBuffer,
                                    None,
                                    self.readOtherBufer)

        except HILError as h:
            print(h.get_error_message())

        finally:
            self.motorCurrent = self.readAnalogBuffer
            self.motorPosition = 2*np.pi*self.readEncoderBuffer[0:2]/2048
            self.pitchAngle = 2*np.pi*self.readEncoderBuffer[2]/2880
            self.yawAngle = 2*np.pi*self.readEncoderBuffer[3]/4096
            self.gyroscope = self.readOtherBufer[0:3]
            self.accelerometer = self.readOtherBufer[3:6]
            self.motorSpeed = 2*np.pi*self.readOtherBufer[6:8]/2048
            self.pitchRate = 2*np.pi*self.readOtherBufer[8]/2880
            self.yawRate = 2*np.pi*self.readOtherBufer[9]/4096

    def write_led(self, color=np.array([1, 0, 0], dtype=np.float64)):
        """Use this to write LED values to the Aero2. \n

        Parameter
        ---------
        color : array
            3x1 numpy array of RGB colors (0 to 1 intensity for each).
            Eg. np.array([0, 1, 0], dtype=np.float64) for Green).

        """
        try:
            self.writeOtherBuffer = color
            self.card.write_other(self.WRITE_OTHER_CHANNELS, len(self.WRITE_OTHER_CHANNELS), self.writeOtherBuffer)

        except HILError as h:
            print(h.get_error_message())

    def write_voltage(self, voltage0=0, voltage1=0):
        """
        Writes voltage commands to the motors on the Aero2.

        Parameters
        ----------
        voltage0 : float
            Voltage command sent to rotor 0. Must be between -15 and 15.
        voltage1 : float
            Voltage command sent to rotor 1. Must be between -15 and 15.
        """
        try:
            self.writeAnalogBuffer = np.array([np.clip(voltage0, -15, 15), np.clip(voltage1, -15, 15)], dtype=np.float64)

            self.card.write_analog(self.WRITE_ANALOG_CHANNELS, len(self.WRITE_ANALOG_CHANNELS), self.writeAnalogBuffer)

        except HILError as h:
            print(h.get_error_message())

    def terminate(self):
        """
        Terminates the Aero2 card.

        Notes
        -----
        - Stops the task reader if `readMode` is 1.
        - Sets final voltage values and LED color.
        """

        try:
            self.write_voltage(0, 0)
            self.write_led(np.array([1, 0, 0], dtype=np.float64))
            self.writeDigitalBuffer = np.zeros([2], dtype=np.int8)
            self.card.write_digital(self.WRITE_DIGITAL_CHANNELS,
                                    len(self.WRITE_DIGITAL_CHANNELS),
                                    self.writeDigitalBuffer)

            if self.readMode:
                self.card.task_stop(self.readTask)
                self.card.task_delete(self.readTask)
            self.card.close()

        except HILError as h:
            print(h.get_error_message())

    def __enter__(self):
        """
        Used for the `with` statement.

        Returns
        -------
        Aero2
            The current instance of the class.
        """
        return self

    def __exit__(self, type, value, traceback):
        """
        Used for the `with` statement. Terminates the connection with the Aero2.

        Parameters
        ----------
        type : Exception type
            The exception type, if any.
        value : Exception value
            The exception value, if any.
        traceback : Traceback
            The traceback object, if any.
        """
        self.terminate()