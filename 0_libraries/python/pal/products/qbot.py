import numpy as np
from quanser.hardware import HIL, HILError, MAX_STRING_LENGTH, Clock
from quanser.hardware.enumerations import BufferOverflowMode

class QBot3():
    #region: Channels, Constants and Buffers

    # Constants
    GEAR_RATIO = 6545.0/132.0
    ENCODER_COUNTS = 52.0
    WHEEL_BASE = 0.230
    WHEEL_WIDTH = 0.021
    WHEEL_RADIUS = 0.035

    # Channels
    WRITE_DIGITAL_CHANNELS = np.array([28, 29, 30, 31], dtype=np.int32)
    WRITE_OTHER_CHANNELS = np.array([2000, 2001, 14000, 16000], dtype=np.int32)

    READ_ANALOG_CHANNELS = np.array([0], dtype=np.int32)
    READ_ENCODER_CHANNELS = np.array([0, 1], dtype=np.int32)
    READ_DIGITAL_CHANNELS = np.array([28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38])
    READ_OTHER_CHANNELS = np.array([1002, 3002], dtype=np.int32)

    # Buffers
    writeDigitalBuffer = np.zeros(4, dtype=np.int8)
    writeOtherBuffer = np.zeros(4, dtype=np.float64)

    readAnalogBuffer = np.zeros(1, dtype=np.float64)
    readEncoderBuffer = np.zeros(2, dtype=np.int32)
    readDigitalBuffer = np.zeros(11, dtype=np.int8)
    readOtherBuffer = np.zeros(5, dtype=np.float64)

    # Initialize return arrays
    batVoltage = np.zeros(1, dtype=np.float64)
    rightEncoder = np.zeros(1, dtype=np.int32)
    leftEncoder = np.zeros(1, dtype=np.int32)
    bumpers = np.zeros(3, dtype=np.float64)
    wheelDrop = np.zeros(2, dtype=np.float64)
    cliff = np.zeros(3, dtype=np.float64)
    buttons = np.zeros(3, dtype=np.float64)
    heading = np.zeros(1, dtype=np.float64)
    gyroscope = np.zeros(3, dtype=np.float64)
    #endregion

    def __init__(self, hardware=1, readMode=0, frequency=240):
        ''' This function configures the QBot 3 and returns a handle to the card. Use the handle for other methods such as terminate. This class uses Task Based IO at 240 Hz by default.'''

        self.card = HIL()
        self.hardware = hardware
        self.readMode = readMode
        try:
            # Open the Card
            if self.hardware:
                boardIdentifier = "0"
                self.card.open("qbot3", boardIdentifier)
            else:
                boardIdentifier = "0@tcpip://localhost:18910?nagle='off'"
                self.card.open("qbot2e", boardIdentifier)

            if self.card.is_valid():
                # Set PWM options
                self.card.set_card_specific_options("pwm0_en=1;pwm0_pin=12;pwm1_en=1;pwm1_pin=13;", MAX_STRING_LENGTH)

                # Set Encoder Quadrature
                self.card.set_encoder_counts(self.READ_ENCODER_CHANNELS, len(self.READ_ENCODER_CHANNELS), np.zeros(1, dtype=np.int32))
                self.frequency = frequency
                if self.readMode:
                    self.readTask = self.card.task_create_reader(int(self.frequency*2),
                            self.READ_ANALOG_CHANNELS,  len(self.READ_ANALOG_CHANNELS),
                            self.READ_ENCODER_CHANNELS, len(self.READ_ENCODER_CHANNELS),
                            self.READ_DIGITAL_CHANNELS, len(self.READ_DIGITAL_CHANNELS),
                            self.READ_OTHER_CHANNELS,   len(self.READ_OTHER_CHANNELS))

                    # Set buffer overflow mode depending on whether its for hardware or virtual QBot
                    if self.hardware:
                        self.card.task_set_buffer_overflow_mode(self.readTask, BufferOverflowMode.OVERWRITE_ON_OVERFLOW)
                    else:
                        self.card.task_set_buffer_overflow_mode(self.readTask, BufferOverflowMode.WAIT_ON_OVERFLOW)

                    self.card.task_start(self.readTask, Clock.HARDWARE_CLOCK_0, self.frequency, HIL.INFINITE)

                print('QBot 3 configured successfully.')

        except HILError as h:
            print(h.get_error_message())

    def terminate(self):
        ''' This function terminates the QBot 3 card after setting final values for drive & LEDs. Also terminates the task reader.'''

        # Set 0 outputs
        self.writeOtherBuffer = np.zeros(4, dtype=np.float64)
        self.writeDigitalBuffer = np.zeros(4, dtype=np.int8)

        try:
            self.card.write(None, 0, None, 0, self.WRITE_DIGITAL_CHANNELS, len(self.WRITE_DIGITAL_CHANNELS), self.WRITE_OTHER_CHANNELS, len(self.WRITE_OTHER_CHANNELS), None, None, self.writeDigitalBuffer, self.writeOtherBuffer)
            if self.readMode:
                self.card.task_stop(self.readTask)
            self.card.close()

        except HILError as h:
            print(h.get_error_message())

    def set_led_states_to_values(self, led1State, led2State):
        if led1State == 0:
            self.writeDigitalBuffer[0] = 1
            self.writeDigitalBuffer[1] = 0
        elif led1State == 1:
            self.writeDigitalBuffer[0] = 0
            self.writeDigitalBuffer[1] = 1
        elif led1State == 2:
            self.writeDigitalBuffer[0] = 1
            self.writeDigitalBuffer[1] = 1
        if led2State == 0:
            self.writeDigitalBuffer[2] = 1
            self.writeDigitalBuffer[3] = 0
        elif led2State == 1:
            self.writeDigitalBuffer[2] = 0
            self.writeDigitalBuffer[3] = 1
        elif led2State == 2:
            self.writeDigitalBuffer[2] = 1
            self.writeDigitalBuffer[3] = 1

    def read_write_std(self, rightWheelVel, leftWheelVel, led1State, led2State):
        '''Use this to write motor and LED commands, and read the battery voltage, motor current and encoder counts \n

        INPUTS:
        rightWheelVel - right wheel velocity in m/s.
        leftWheelVel - left wheel velocity in m/s.
        led_1_state - 0 (red), 1 (green) or 2(yellow)
        led_2_state - 0 (red), 1 (green) or 2(yellow)

        OUTPUTS:

        batVoltage - battery voltage measurement
        rightEncoder - right wheel encoder counts
        leftEncoder - left wheel encoder counts
        bumpers - 3x1 numpy array with right, center and left bumpers
        heading - heading value computed from gyroscope
        gyroscope - 3x1 numpy array gyroscope data'''

        self.writeOtherBuffer[0] = np.clip(rightWheelVel, -0.7, 0.7)
        self.writeOtherBuffer[1] = np.clip(leftWheelVel, -0.7, 0.7)
        # self.writeOtherBuffer[4] = np.clip(sound, 0.0, 6.0)
        self.set_led_states_to_values(led1State, led2State)

        # IO
        try:
            if True:
                self.card.write(None, 0, None, 0, self.WRITE_DIGITAL_CHANNELS, len(self.WRITE_DIGITAL_CHANNELS), self.WRITE_OTHER_CHANNELS, len(self.WRITE_OTHER_CHANNELS),
                                None, None, self.writeDigitalBuffer, self.writeOtherBuffer)
                if self.readMode:
                    self.card.task_read(self.readTask, 1, self.readAnalogBuffer, self.readEncoderBuffer, self.readDigitalBuffer, self.readOtherBuffer)
                else:
                    self.card.read( self.READ_ANALOG_CHANNELS, len(self.READ_ANALOG_CHANNELS),
                                    self.READ_ENCODER_CHANNELS, len(self.READ_ENCODER_CHANNELS),
                                    self.READ_DIGITAL_CHANNELS, len(self.READ_DIGITAL_CHANNELS),
                                    self.READ_OTHER_CHANNELS, len(self.READ_OTHER_CHANNELS),
                                    self.readAnalogBuffer,
                                    self.readEncoderBuffer,
                                    self.readDigitalBuffer,
                                    self.readOtherBuffer)
        except HILError as h:
            print(h.get_error_message())

        finally:
            # Set internal states
            self.batVoltage = self.readAnalogBuffer
            self.rightEncoder = self.readEncoderBuffer[0]
            self.leftEncoder = self.readEncoderBuffer[1]
            self.bumpers = self.readDigitalBuffer[0:3]
            self.wheelDrop = self.readDigitalBuffer[3:6]
            self.cliff = self.readDigitalBuffer[6:9]
            self.buttons = self.readDigitalBuffer[9:11]
            self.heading = self.readOtherBuffer[0]
            self.gyroscope = self.readOtherBuffer[1:-1]

    def estimate_wheel_travel(self, encoder):
        '''This function contains the out-of-the-box mapping from encoders (counts) to wheel travel distance.

        Inputs:
        ENCODER_COUNTS - encoder position in counts

        Outputs:
        distance - wheel travel distance in meters'''

        distance = ( 2*np.pi / self.ENCODER_COUNTS ) * ( 1 / self.GEAR_RATIO ) * self.WHEEL_RADIUS * encoder

        return distance