"""sensors: A module for simplifying interactions with
the Mechatronic Sensors Trainer platform.

This module provides a set of API classes and tools to facilitate working
with the Mechatronic Sensors Trainer. It is designed to make it easy
to read and write all available inputs/outputs of the device.
"""

import os
import sys

import numpy as np
from quanser.hardware import (HIL, HILError, MAX_STRING_LENGTH,
                              Clock, StringProperty, IntegerProperty,
                              EncoderQuadratureMode)
from quanser.hardware.enumerations import BufferOverflowMode
from pal.utilities.vision import Camera2D
from quanser.devices import (QuanserMechatronicSensorsTrainerDisplay,
                             LCDTouch, DeviceError)
from quanser.multimedia import ImageFormat, ImageDataType


class SensorsTrainer():
    '''A class to configure Quanser's Mechatronic Sensors Trainer'''

    def __init__(
            self,
            id=0,
            readMode=0,
            frequency=200,
            radarService = 0,
            radarStart = 0.2,
            radarLength = 1.0,
            ultraService = 0,
            ultraStart = 0.0,
            ultraLength = 2.4,
            knobEncQuad = 4,
            extEncQuad = 4,
            btn0Pol = 1,
            btn1Pol = 1,
            boardSpecificOptions=''):
        """
        Initializes and configures the Sensors Trainer.

        Parameters
        ----------
        id : int, optional
            Board identifier number. Defaults to 0.
            Used when more than 1 Sensors Trainer is connected.
        readMode : int, optional
            Indicates the read mode. Defaults to 0.
            (0 for immediate I/O, 1 for task-based I/O).
        frequency : int, optional
            Sampling frequency. Used when readMode is set to 1.
            Defaults to 200.
        radarService : int, optional
            Indicates the radar service to use. Defaults to 0 (off).
            (1.Distance. 2.Presence, 3.Power Bins, 4.Envelope, 5.IQ, 6.Sparse)
        radarStart: float, optional
            Start distance in meters for radar reading. Defaults to 0.1.
            Radar range is 0 to 7 meters.
        radarLength: float, optional
            Distance in meters for radar reading starting at `radarStart`.
            Defaults to 6.9. Radar range is 0 to 7 meters. e.g., to read
            from 0 to 1 m or 2 to 3 m, this value should be 1.
        ultraService : int, optional
            Indicates the ultrasonic service to use. Defaults to 0 (off).
            (1. Distance only, 2.Distance + IQ)
        ultraStart: float, optional
            Start distance in meters for ultrasonic reading. Defaults to 0.
            Ultrasonic range is 0 to 2.4 meters.
        ultraLength: float, optional
            Distance in meters for ultrasonic reading starting at `ultraStart`.
            Defaults to 2.4. Radar range is 0 to 2.4 meters. e.g., to read
            from 0 to 1 m or 2 to 3 m, this value should be 1.
        knobEncQuad: int, optional
            Decoding mode for the knob encoder. Defaults to 4. (Quadrature)
            (1. 1x decoding, 2. 2x decoding, 4. 4x decoding).
        extEncQuad: int, optional
            Decoding mode for the external encoder. Defaults to 4. (Quadrature)
            (1. 1x decoding, 2. 2x decoding, 4. 4x decoding).
        boardSpecificOptions : str, optional
            Board-specific configuration options. Defaults to an empty string.
            If modified, `radarService`, `radarStart`, `radarLength`,
            `ultraService`, `ultraStart` and `ultraLength` will not be read and
            will have to be defined in the string as
            `radar_serv`, `radar_start`, `radar_len`, `ultra_len`,
            `ultra_serv` and `ultra_start`.

        Raises
        ------
        HILError
            If the board is not valid or there is a configuration error.
        """

        knobEncQuad = knobEncQuad if knobEncQuad in (1,2,4)  else 4
        extEncQuad = extEncQuad if extEncQuad in (1,2,4)  else 4

        if not boardSpecificOptions:
            if radarService < 0 or radarService > 6:
                print(f"Invalid radarService value: {radarService}. Must be between 1 and 6.")

            if radarStart > 6.5 or radarStart < 0:
                radarStart = 0
                print('Make sure radarStart is between 0 and 6.5 m. Value set to 0')

            if radarLength + radarStart > 7.0:
                radarLength = 7 - radarStart
                print(f'radarLength was out of bounds. Value set to {radarLength}'
                      f' to keep range between {radarStart} and 7.')

            if ultraService < 0 or ultraService > 2:
                print(f"Invalid radarService value: {ultraService}. Must be between 0 and 2.")

            if ultraStart > 5 or ultraStart < 0:
                ultraStart = 0
                print('Make sure ultraStart is between 0 and 5 m. Value set to 0')

            if ultraLength + ultraStart > 5:
                ultraLength = 5 - ultraStart
                print(f'ultraLength was out of bounds. Value set to {ultraLength}'
                      f' to keep range between {ultraStart} and 5.')

            # if empty BSO, use defaults
            boardSpecificOptions = (
                "adc1_os=256;adc2_os=256;adc3_os=64;"
                f"btn0_pol={btn0Pol};btn1_pol={btn1Pol};"
                "dio0_mode=0;dio1_mode=0;dio2_mode=0;dio3_mode=0;"
                "enc_dir=0;enc_mode=0;enc_freq=240e6;knob_dir=0;"
                "gyro_avg=1;gyro_filter=196.6;gyro_fs=2000;gyro_rate=1125;"
                "accel_avg=1;accel_filter=246;accel_fs=16;accel_rate=1125;"
                "temp_filter=7932;color_int=50;color_ag=4;color_dg=4;"
                "tof_res=8x8;tof_order=0;tof_freq=15;tof_int=2;tof_sharp=14;"
                "radar_bins=0;radar_down=1;radar_gain=0.30;radar_hwaas=30;"
                f"radar_len={radarLength};radar_mur=6;radar_noise=0;radar_prof=3;"
                "radar_run=0.7;radar_samp=A;"
                f"radar_serv={radarService};radar_start={radarStart};"
                "radar_sweeps=16;radar_swprate=0.0;"
                f"ultra_int=100;ultra_len={ultraLength};"
                f"ultra_serv={ultraService};ultra_start={ultraStart};"
                "hum_over=2;press_over=4;temp_over=8;"
                "weather_standby=0.5;weather_filt=2;"
                "load_gain=128;load_rate=320;"
            )


        self._boardSpecificOptions = boardSpecificOptions
        self._frequency = frequency
        self._readMode = readMode
        self._id = str(id)
        boardIdentifier = self._id

        # region: Channel and internal Buffer definitions

        # Define read/write channels and buffers
        self.WRITE_OTHER_CHANNELS = np.array([11000, 11001, 11002,
                                              11003, 11004, 11005,
                                              11006],
                                             dtype=np.uint32)
                                            # , 11007, 11008,
                                            #   11009, 11010, 11011,
                                            #   11012

        # Internal write buffers
        self._writeOtherBuffer = np.zeros(
            len(self.WRITE_OTHER_CHANNELS),
            dtype=np.float64)

        self.READ_ANALOG_CHANNELS = np.array([0, 1, 2, 3, 4, 5, 6, 7],
                                             dtype=np.uint32)
        self.READ_ENCODER_CHANNELS = np.array([0, 1], dtype=np.uint32)
        self.READ_DIGITAL_CHANNELS = np.array([0, 1, 2, 3, 4, 5, 6,
                                               7, 8, 9, 10, 11, 12, 13, 14,30],
                                              dtype=np.uint32)

        rangeTOF = np.arange(0, 128, dtype=np.uint32) # 0 - 127
        environmentSensors = np.array([9000, 10000, 11000], dtype=np.uint32)
        colorReflectance =  np.arange(11001, 11070, dtype=np.uint32) # 11001 - 11069
        TOFTargets = np.arange(13000, 13064, dtype=np.uint32) # 13000 - 13063
        imuThermal =  np.array([3000, 3001, 3002, 4000,
                                 4001, 4002, 8000, 8001, 8002,
                                 10001, 10002, 10003], dtype=np.uint32)
        cpuTemp = np.array([10004], dtype=np.uint32)


        radarStartChnl = np.array([128], dtype=np.uint32)
        radarLengthChnl = np.array([129], dtype=np.uint32)
        radarPointsChnl = np.array([13064], dtype=np.uint32)
        radarServiceChnl = np.array([16000], dtype=np.uint32)

        ultraStartChnl = np.array([130], dtype=np.uint32)
        ultraLengthChnl = np.array([131], dtype=np.uint32)
        ultraDistChnl = np.array([132], dtype=np.uint32)
        ultraPointsChnl = np.array([13065], dtype=np.uint32)

        self._radarEn = 1
        # Define radar channels based on radarService using if-elif-else
        if radarService == 1:  # Distance
            radarDistance = np.arange(10000000, 10000010, dtype=np.uint32)
            radarAmplitude = np.arange(21000000, 21000010, dtype=np.uint32)
        elif radarService == 2:  # Presence
            radarDistance = np.array([10000000], dtype=np.uint32)
            radarAmplitude = np.array([21000000], dtype=np.uint32)
        elif radarService == 3:  # Power Bins
            radarDistance = np.arange(10000000, 10000437, dtype=np.uint32)
            radarAmplitude = np.arange(21000000, 21000437, dtype=np.uint32)
        elif radarService == 4:  # Envelope
            radarDistance = np.arange(10000000, 10014455, dtype=np.uint32)
            radarAmplitude = np.arange(21000000, 21014455, dtype=np.uint32)
        elif radarService == 5:  # IQ
            radarDistance = np.arange(10000000, 10014385, dtype=np.uint32)
            radarAmplitude = np.arange(21000000, 21028770, dtype=np.uint32)
        elif radarService == 6:  # Sparse
            radarDistance = np.array([10000000], dtype=np.uint32)
            radarAmplitude = np.arange(21000000, 21001808, dtype=np.uint32)
        elif radarService == 0:
            radarDistance = np.array([10000000], dtype=np.uint32)
            radarAmplitude = np.array([21000000], dtype=np.uint32)
            self._radarEn = 0
        else:
            raise ValueError(f"Invalid radarService value: {radarService}. Must be between 1 and 6.")

        self._ultraEn = 1
        # Define radar channels based on radarService using if-elif-else
        if ultraService == 2:  # IQ
            ultraIQDistance = np.arange(10050000, 10050450, dtype=np.uint32)
            ultraAmplitude = np.arange(21050000, 21050900, dtype=np.uint32)
        elif ultraService == 0 or ultraService == 1: # service 1 is single distance only
            ultraIQDistance = np.array([10050000], dtype=np.uint32)
            ultraAmplitude = np.array([21050000], dtype=np.uint32)
            self._ultraEn = 0
        else:
            raise ValueError(f"Invalid ultraService value: {ultraService}. Must be between 1 and 6.")

        self.READ_OTHER_CHANNELS = np.concatenate((rangeTOF, environmentSensors,
                                        colorReflectance, TOFTargets,
                                        imuThermal, cpuTemp, radarStartChnl,
                                        radarLengthChnl, radarPointsChnl,
                                        radarServiceChnl, radarDistance,
                                        radarAmplitude, ultraStartChnl,
                                        ultraLengthChnl, ultraPointsChnl,
                                        ultraDistChnl, ultraIQDistance,
                                        ultraAmplitude))

        # Internal read buffers
        self._readAnalogBuffer = np.zeros(
            len(self.READ_ANALOG_CHANNELS),
            dtype=np.float64)
        self._readEncoderBuffer = np.zeros(
            len(self.READ_ENCODER_CHANNELS),
            dtype=np.int32)
        self._readDigitalBuffer = np.zeros(
            len(self.READ_DIGITAL_CHANNELS),
            dtype=np.int8)
        self._readOtherBuffer = np.zeros(
            len(self.READ_OTHER_CHANNELS),
            dtype=np.float64)

        # endregion

        # External read buffers

        # analog channel
        self.joystick = np.zeros(2, dtype=np.float64)
        self.lightResistor = np.zeros(1, dtype=np.float64)
        self.forceResistor = np.zeros(1, dtype=np.float64)
        self.passiveIR = np.zeros(1, dtype=np.float64)
        self.IRDistance = np.zeros(1, dtype=np.float64)
        self.loadCell = np.zeros(1, dtype=np.float64)
        self.userCurrent = np.zeros(1, dtype=np.float64)

        # encoder channel
        self.encoder = np.zeros(2, dtype=np.int32)

        # digital channel
        self.digitalInputs = np.zeros(4, dtype=np.float64)
        self.buttons = np.zeros(2, dtype=np.float64)
        self.joystickButton = np.zeros(1, dtype=np.float64)
        self.encoderPulses = np.zeros(2, dtype=np.float64)
        self.powerAlert = np.zeros(1, dtype=np.float64)
        self.thermocoupleFault = np.zeros(4, dtype=np.float64)
        self.sdCardPresent = np.zeros(1, dtype=np.float64)
        self.radarConfigError = np.zeros(1, dtype=np.float64)

        # other channel: TOF color sensor and environment
        self.TOFDistance = np.zeros(64, dtype=np.float64)
        self.TOFSigma = np.zeros(64, dtype=np.float64)
        self.TOFReflectance = np.zeros(64, dtype=np.float64)
        self.TOFNumberOfTargets = np.zeros(64, dtype=np.float64)
        self.pressure = np.zeros(1, dtype=np.float64)
        self.tempWeather = np.zeros(1, dtype=np.float64)
        self.tempCPU = np.zeros(1, dtype=np.float64)
        self.humidity = np.zeros(1, dtype=np.float64)
        self.colorClear = np.zeros(1, dtype=np.float64)
        self.colorRGB = np.zeros(3, dtype=np.float64)
        self.colorIR = np.zeros(1, dtype=np.float64)
        self.gyro = np.zeros(3, dtype=np.float64)
        self.accelerometer = np.zeros(3, dtype=np.float64)
        self.magnetometer = np.zeros(3, dtype=np.float64)
        self.tempThermoChip = np.zeros(1, dtype=np.float64)
        self.tempThermo = np.zeros(1, dtype=np.float64)
        self.tempIMU = np.zeros(1, dtype=np.float64)

        self.radarStart = np.zeros(1, dtype=np.float64)
        self.radarLength = np.zeros(1, dtype=np.float64)
        self.radarPoints = np.zeros(1, dtype=np.float64)
        self.radarService = np.zeros(1, dtype=np.float64)

        self._radDistLen = len(radarDistance)
        self.radarDistances = np.zeros(self._radDistLen, dtype=np.float64)
        self._radAmpLen = len(radarAmplitude)
        self.radarAmplitudes = np.zeros(self._radAmpLen, dtype=np.float64)

        self.ultraStart = np.zeros(1, dtype=np.float64)
        self.ultraLength = np.zeros(1, dtype=np.float64)
        self.ultraPoints = np.zeros(1, dtype=np.float64)
        self.ultraDistance = np.zeros(1, dtype=np.float64)

        self._ultDistLen = len(ultraIQDistance)
        self.ultraIQDistances = np.zeros(self._ultDistLen, dtype=np.float64)
        self._ultraAmpLen = len(ultraAmplitude)
        self.ultraIQAmplitudes = np.zeros(self._ultraAmpLen, dtype=np.float64)

        try:
            # Open the Card
            self.card = HIL("mech_sensors_trainer_usb", boardIdentifier)

            if self.card.is_valid():
                self.card.set_card_specific_options(
                    self._boardSpecificOptions,
                    MAX_STRING_LENGTH)

                self.serialNumber = self.card.get_string_property(
                    StringProperty.SERIAL_NUMBER,64)

                # check firmware
                properties = np.array([IntegerProperty.FIRMWARE_BUILD], dtype=np.int32)

                num_properties = len(properties)
                buffer = np.zeros(num_properties, dtype=np.int32)
                self.card.get_integer_property(properties, num_properties, buffer)
                # print(buffer)
                self._firmwareBuild = buffer

                self.card.set_encoder_counts(
                    self.READ_ENCODER_CHANNELS,
                    len(self.READ_ENCODER_CHANNELS),
                    np.zeros(len(self.READ_ENCODER_CHANNELS), dtype=np.int32)
                )

                modes = np.array([EncoderQuadratureMode.X4,
                                  EncoderQuadratureMode.X4],
                                  dtype=np.int32)

                if knobEncQuad == 1:
                    modes[0] = EncoderQuadratureMode.X1
                elif knobEncQuad == 2:
                    modes[0] = EncoderQuadratureMode.X2

                if extEncQuad == 1:
                    modes[1] = EncoderQuadratureMode.X1
                elif extEncQuad == 2:
                    modes[1] = EncoderQuadratureMode.X2

                self.card.set_encoder_quadrature_mode(
                    self.READ_ENCODER_CHANNELS,
                    len(self.READ_ENCODER_CHANNELS),
                    modes)

                # initial setup
                # Turn off all LEDs
                self.write_leds(0, 0)

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

                self.read_outputs() # read data once to clear old data

            self._HilError = False

        except HILError as h:
            self._HilError = True  # Flag to know if error was HIL

            if h.error_code == -108:
                print('Make sure your device is connected to your PC and has finished loading.')

            elif h.error_code == -1068:
                print('Update your device firmware by following the instructions at *link*')
                print(h.get_error_message())

            else:
                print(h.get_error_message())
            sys.exit()

    def write_leds(self, rgb = [1, 1, 1], ir = 0):
        """
        Writes the RGB and IR values to the LEDs of the Sensors Trainer.

        Parameters
        ----------
        rgb : list or float/int, optional
            RGB values for the 2 RGB LEDs next to the color sensor.
            - If a list: must contain exactly 3 values (R, G, B).
            - If a single number: it will use the same values as the R, G and B
            channel, useful for a dimmer white color.
            Defaults to [1, 1, 1] (white).
            Each value should be between 0 and 1.
        ir : list or float/int, optional
            IR value for the IR LED next to the color sensor.
            - If a list: must contain exactly 1 value ([value])
            - If a single number: it will be converted to [value].
            Defaults to 0 (off).
            Each value should be between 0 and 1.
        """
        # Make sure both are always a list
        if isinstance(rgb, (int, float)):
            rgb = [rgb, rgb, rgb]

        if isinstance(ir, (int, float)):
            ir = [ir]

        if len(rgb) != 3 or len(ir) != 1:
            raise ValueError("RGB must have 3 values and IR must have 1 value.")

        # Clamp with numpy
        rgb = np.clip(rgb, 0, 1).tolist()
        ir = np.clip(ir[0], 0, 1)

        try:
            self._writeOtherBuffer[0:3] = rgb
            self._writeOtherBuffer[3:6] = rgb
            self._writeOtherBuffer[6] = ir

            self.card.write_other(
                self.WRITE_OTHER_CHANNELS,
                len(self.WRITE_OTHER_CHANNELS),
                self._writeOtherBuffer
            )
        except HILError as h:
            self._HilError = True  # Flag to know if error was HIL
            raise

    def read_outputs(self):
        """Reads all sensor data from the Mechatronics Sensor Trainer.

        This method reads all available sensor data and updates the
        corresponding instance variables with the latest measurements.

        Returns
        -------
        None

        Raises
        ------
        HILError
            If there is an error during the read operation.

        Attributes Updated
        ----------------
        self.joystick : ndarray of float, shape (2,)
            Measured joystick position [x, y] in percent.
        self.lightResistor : float
            Light resistor measurement in volts.
        self.forceResistor : float
            Force resistor measurement in volts.
        self.passiveIR : float
            Passive IR sensor measurement in volts.
        self.IRDistance : float
            IR distance sensor measurement in volts.
        self.loadCell : float
            Load cell measurement in volts.
        self.encoder0 : int
            Knob encoder position in counts.
        self.encoder1 : int
            External encoder position in counts.

        self.buttons : ndarray of float, shape (2,)
            Button states [button0, button1], 1 when pressed.
            If button polarity is initialized as 0, it produces 0 when pressed.
        self.joystickButton : float
            Joystick button state, 1 when pressed.
        self.encoderPulses : ndarray of float, shape (2,)
            Integrated knob encoder pulses (0/1) [pulseA, pulseB].
        self.thermocoupleFault : ndarray of bool, shape (4,)
            Thermocouple fault states [fault, short to vcc, short to gnd, not connected].

        self.TOFDistance : ndarray of float, shape (64,)
            Time-of-flight distances from 8x8 TOF grid in meters.
        self.TOFSigma : ndarray of float, shape (64,)
            Time-of-flight distance confidence values from 8x8 TOF grid in meters.
        self.pressure : float
            Weather sensor pressure in Pascals.
        self.tempWeather : float
            Weather sensor temperature in Celsius.
        self.humidity : float
            Weather sensor humidity in percent.
        self.colorClear : float
            Color sensor clear channel in percent.
        self.colorRGB : ndarray of float, shape (3,)
            Color sensor RGB values [red, green, blue] in percent.
        self.colorIR : float
            Color sensor IR channel in percent.
        self.TOFReflectance : ndarray of float, shape (64,)
            Time-of-flight reflectance values from 8x8 grid in percent.
        self.TOFNumberOfTargets : ndarray of float, shape (64,)
            Number of targets detected by TOF sensor per grid cell.
        self.gyro : ndarray of float, shape (3,)
            IMU Gyroscope measurements [x, y, z] in rad/s.
        self.accelerometer : ndarray of float, shape (3,)
            IMU Accelerometer measurements [x, y, z] in m/s^2.
        self.magnetometer : ndarray of float, shape (3,)
            IMU Magnetometer measurements [x, y, z] in Tesla.
        self.tempThermo : float
            Thermocouple probe temperature in Celsius.
        self.tempThermoChip : float
            Thermocouple chip temperature in Celsius.
        self.tempIMU : float
            IMU temperature in Celsius.

        self.radarStart : float
            Radar start distance in meters.
        self.radarLength : float
            Radar distance range to read starting from `radarStart` in meters .
        self.radarPoints : float
            Number of valid radar measurement points. Use to discard extra points.
        self.radarService : float
            Active Radar Service mode.
        self.radarDistances : ndarray of float
            Radar distance measurements in meters (length varies by service).
        self.radarAmplitudes : ndarray of float
            Radar amplitude measurements (length varies by service).
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
            self._HilError = True  # Flag to know if error was HIL
            raise

        finally:
            self.joystick = self._readAnalogBuffer[0:2]
            self.lightResistor = self._readAnalogBuffer[2]
            self.forceResistor = self._readAnalogBuffer[3]
            self.passiveIR = self._readAnalogBuffer[4]
            self.IRDistance = self._readAnalogBuffer[5]
            self.loadCell = self._readAnalogBuffer[6]
            self.userCurrent = self._readAnalogBuffer[7]

            self.encoder0 = self._readEncoderBuffer[0]
            self.encoder1 = self._readEncoderBuffer[1]

            self.digitalInputs = self._readDigitalBuffer[0:4]
            self.buttons = self._readDigitalBuffer[4:6]
            self.joystickButton = self._readDigitalBuffer[6]
            self.encoderPulses = self._readDigitalBuffer[[7, 8]]
            self.powerAlert = self._readDigitalBuffer[9]
            self.thermocoupleFault = self._readDigitalBuffer[10:14]
            self.sdCardPresent = self._readDigitalBuffer[14]
            self.radarConfigError = self._readDigitalBuffer[15]
            if self.radarConfigError == 1:
                print('Radar configuration error. Check initial radar settings.')
                self.terminate()

            self.TOFDistance = self._readOtherBuffer[0:64]
            self.TOFSigma = self._readOtherBuffer[64:128]
            self.pressure = self._readOtherBuffer[128]
            self.tempWeather = self._readOtherBuffer[129]
            self.humidity = self._readOtherBuffer[130]
            self.colorClear = self._readOtherBuffer[131]
            self.colorRGB = self._readOtherBuffer[132:135]
            self.colorIR = self._readOtherBuffer[135]
            self.TOFReflectance = self._readOtherBuffer[136:200]
            self.TOFNumberOfTargets = self._readOtherBuffer[200:264]
            self.gyro = self._readOtherBuffer[264:267]
            self.accelerometer = self._readOtherBuffer[267:270]
            self.magnetometer = self._readOtherBuffer[270:273]
            self.tempThermo = self._readOtherBuffer[273]
            self.tempThermoChip = self._readOtherBuffer[274]
            self.tempIMU = self._readOtherBuffer[275]
            self.tempCPU = self._readOtherBuffer[276]

            if self._radarEn:
                self.radarStart = self._readOtherBuffer[277]
                self.radarLength = self._readOtherBuffer[278]
                self.radarPoints = self._readOtherBuffer[279]
                self.radarService = self._readOtherBuffer[280]
                distanceEnd = 281+self._radDistLen
                self.radarDistances = self._readOtherBuffer[281:distanceEnd]
                amplitudeEnd = distanceEnd + self._radAmpLen
                self.radarAmplitudes = self._readOtherBuffer[distanceEnd:amplitudeEnd]

                if self.radarService == 2: # presence
                    self.radarDistances = self.radarDistances[0]
                    self.radarAmplitudes = self.radarAmplitudes[0]
                if self.radarService == 6: # sparse
                    self.radarDistances = self.radarDistances[0]

            else:
                self.radarStart = np.float64(0)
                self.radarLength = np.float64(0)
                self.radarPoints = np.float64(0)
                self.radarService = np.float64(0)
                self.radarDistances = np.float64(0)
                self.radarAmplitudes  = np.float64(0)
                amplitudeEnd = 283

            if self._ultraEn:
                self.ultraStart = self._readOtherBuffer[amplitudeEnd]
                self.ultraLength = self._readOtherBuffer[amplitudeEnd+1]
                self.ultraPoints = self._readOtherBuffer[amplitudeEnd+2]
                self.ultraDistance = self._readOtherBuffer[amplitudeEnd+3]
                distanceStart = amplitudeEnd+4
                distanceEnd = distanceStart+self._ultDistLen
                self.ultraIQDistances = self._readOtherBuffer[distanceStart:distanceEnd]
                # amplitudeEnd = distanceEnd + self._ultraAmpLen+1
                self.ultraIQAmplitudes = self._readOtherBuffer[distanceEnd:]
            else:
                self.ultraStart = np.float64(0)
                self.ultraLength = np.float64(0)
                self.ultraPoints = np.float64(0)
                self.ultraDistance = self._readOtherBuffer[amplitudeEnd+3]
                self.ultraIQDistances = np.float64(0)
                self.ultraIQAmplitudes = np.float64(0)

    def terminate(self):
        """
        Cleanly shuts down and terminates the connection with
        the Mechatronics Sensors Trainer.

        Notes
        -----
        This function stops any active tasks and
        closes the connection to the hardware.

        **Terminates the device after setting final values for ???.
        Also terminates the task reader.
        """

        try:
            if not self._HilError:
                self.write_leds(0, 0)  # Turn off LEDs

                if self._readMode == 1:
                    self.card.task_stop(self._readTask)
                    self.card.task_delete(self._readTask)

                # self.card.watchdog_clear()
                # self.card.watchdog_stop()
                print('Sensors Trainer closed gracefully.')

        except HILError as h:
            print('Error during termination/closing.')
            print('Try restarting the device if needed.')
            print(h.get_error_message())

        finally:
            self.card.close()

    def __enter__(self):
        """
        Used for the `with` statement.

        Returns
        -------
        SensorsTrainer
            The current instance of the class.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Used for the `with` statement.
        Ensures cleanup and terminates the connection
        with the Mechatronic Sensors Trainer.
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

        # if exc_type is UserWarning:
        #     self.terminate()
        #     return True  # Suppress the exception

        # If another exception occurred, handle it
        if exc_type is not None:
            print(f"Exception occurred: {exc_type.__name__}: {exc_value}")

        # Always terminate the connection
        self.terminate()

        # Returning False allows other exceptions to propagate
        # for example, if error is ValueError,
        # traceback helps to pinpoint the error
        return False


class SensorsDisplay():
    '''A class to configure Quanser's Mechatronic Sensors Trainer's Display.
    The touch panel samples at up to 120 Hz.'''

    def __init__(
            self,
            id=0,
            darkMode=True,
            rotation=False):

        """
        Initializes and configures the Sensors Trainer LCD display.

        Parameters
        ----------
        id : int, optional
            Board identifier id number, defaults to 0.
            Use the same id from Sensors Trainer initialization.
        darkMode : bool, optional
            Enables dark mode for the display. Defaults to True.
        rotation : bool, optional
            Enables rotation for the display. Defaults to False.

        Raises
        ------
        DeviceError
            If there is an error initializing the display.

        Notes
        -----
        The touch panel samples at up to 120 Hz or 8.33 ms.
        The LCD update rate, at best, is about 26 Hz or 38.5 ms.

        """

        self._id = str(id)
        boardIdentifier = self._id

        try:
            # Open the Card
            self.display = QuanserMechatronicSensorsTrainerDisplay()
            uri = "lcd://localhost:" + boardIdentifier
            self.display.open(uri)
            self.touch = LCDTouch()

            if darkMode:
                self.display.setDarkMode(True)
                self.set_text_color([255, 255, 255])
                # blackSquare = np.ones([3, 3, 3], dtype=np.uint8) * 0
                # self.draw_image(blackSquare, 0, 0)
            else:
                self.display.setDarkMode(False)
                self.set_text_color([0, 0, 0])
                # whiteSquare = np.ones([3, 3, 3], dtype=np.uint8) * 255
                # self.draw_image(whiteSquare, 0, 0)

            if rotation:
                self.display.setRotation(True)
            else:
                self.display.setRotation(False)

        except DeviceError as e:
            print(e.get_error_message())
            sys.exit()

    def read_touch(self):
        """
        Reads touch input from the Mechatronics Sensors Trainer LCD.
        The device can read up to 5 fingers.

        Returns
        -------
        tuple
            A tuple containing:
            - new (bool): Indicates if there is new touch information.
            - touch (LCDTouch): The touch object containing
                details of the touch.

        Notes
        -----
        The `touch` object contains the following details:
        - `num_fingers` (int): Number of fingers on the screen.
        - `fingers` (list): An array of up to 10 finger structures,
            each containing:
            - `r` (int): Pixel row of the finger.
            - `c` (int): Pixel column of the finger.
            - `id` (int): Identifier associated with the finger.
            THE FOLLOWING DETAILS ARE NOT TESTED AND MIGHT NOT WORK.
            - `event` (int): Event type (0 = put down, 1 = put up,
                                         2 = contact, 3 = no event).
            - `weight` (float): Touch weight
                    (valid points in X * valid points in Y / 2).
            - `speed` (int): Speed of the touch
                    (0 = static, 1 = normal, 2 = high speed).
            - `direction` (int): Direction of the touch
                    (0 = up, 1 = down, 2 = left, 3 = right).
            - `area` (float): Area covered by the touch.

            self.touch.num_fingers /
            self.touch.fingers[0].r /
            self.touch.fingers[0].c
        """

        new = self.display.getTouchInformation(self.touch)
        # new if there is new information, self.touch has the touch object
        return new, self.touch

    def draw_image(self, image, column=0, row=0):
        """
        Draws an image on the Mechatronics Sensors Trainer LCD.

        Image can be color or greyscale, in OpenCV BGR format.

        Parameters
        ----------
        image : numpy.ndarray
            Image to be drawn on the LCD.
        column : int, optional
            Column-coordinate of the image. Defaults to 0.
        row : int, optional
            Row-coordinate of the image. Defaults to 0.

        Notes
        -----
        Display is 800x480 pixels.
        Image can be color or greyscale, in OpenCV BGR format.
        The LCD update rate, at best, is about 26 Hz or 38.5 ms
        """

        # Greyscale has 2 dimensions vs 3 in colored images.

        greyscale = True if image.ndim == 2 else False

        if not greyscale:
            self.display.drawImage(
                pixel_row=row,
                pixel_column=column,
                image_size=image.shape[:2],
                image_format=ImageFormat.ROW_MAJOR_INTERLEAVED_BGR,
                image=image)
        else:
            self.display.drawImage(
                pixel_row=row,
                pixel_column=column,
                image_size=image.shape,
                image_format=ImageFormat.ROW_MAJOR_GREYSCALE,
                image=image)

    def draw_image_blend(self, image, mask, column=0, row=0):
        """
        Draws an image on the Mechatronics Sensors Trainer LCD.
        Uses the given mask as the alpha component of the image.
        The image is blended with the current screen contents
        according to the mask.

        Image can be color or greyscale, in OpenCV BGR format.

        Parameters
        ----------
        image : numpy.ndarray
            Image to be drawn on the LCD.
        mask : numpy.ndarray
            Mask used as the alpha component for blending the image
            with the current display contents.
            A mask pixel of 0 will not write that pixel to the display,
            while a mask pixel value of 255 will fully write that image
            pixel to the display. Any mask pixel value in between
            blends the image with the display contents proportional to
            the mask pixel value. The mask must be in grayscale format
            matching the color image
                (OpenCV format or MATLAB image format).
        column : int, optional
            Column-coordinate of the image. Defaults to 0.
        row : int, optional
            Row-coordinate of the image. Defaults to 0.
        matlab : bool, optional
            Set to True if the image is in MATLAB RGB format.
            Defaults to False.
            Use when not using OpenCVs interleaved BGR format.

        Notes
        -----
        The display is 800x480 pixels.

        The display is not cleared before drawing the image, so multiple
        images may be drawn at different locations on the display.
        """

        # Greyscale has 2 dimensions vs 3 in colored images.
        greyscale = True if image.ndim == 2 else False

        if not greyscale:
            self.display.drawImageWithBlend(
                pixel_row=row,
                pixel_column=column,
                image_size=image.shape[:2],
                image_format=ImageFormat.ROW_MAJOR_INTERLEAVED_BGR,
                image=image,
                mask=mask)
        else:
            self.display.drawImageWithBlend(
                pixel_row=row,
                pixel_column=column,
                image_size=image.shape,
                image_format=ImageFormat.ROW_MAJOR_GREYSCALE,
                image=image,
                mask=mask)


    def draw_image_mask(self, image, mask, column=0, row=0):
        """
        Draws an image on the Mechatronics Sensors Trainer LCD. The image
        is written to the display wherever the mask pixels are non-zero.

        Image can be color or greyscale, in OpenCV BGR format.

        Parameters
        ----------
        image : numpy.ndarray
            Image to be drawn on the LCD.
        mask : numpy.ndarray # ai
            Mask used to determine which pixels are written to the display.
            A mask pixel of 0 will not write that pixel to the display,
            while a non-zero mask pixel value will write that image pixel
            to the display. The mask must be in grayscale format
            matching the color image (OpenCV format or MATLAB image format).
        column : int, optional
            Column-coordinate of the image. Defaults to 0.
        row : int, optional
            Row-coordinate of the image. Defaults to 0.


        Notes
        -----
        The display is 800x480 pixels.

        The display is not cleared before drawing the image, so multiple
        images may be drawn at different locations on the display.

        """
        # Greyscale has 2 dimensions vs 3 in colored images.
        greyscale = True if image.ndim == 2 else False


        if not greyscale:
            self.display.drawImageWithMask(
                pixel_row=row,
                pixel_column=column,
                image_size=image.shape[:2],
                image_format=ImageFormat.ROW_MAJOR_INTERLEAVED_BGR,
                image=image,
                mask=mask)
        else:
            self.display.drawImageWithMask(
                pixel_row=row,
                pixel_column=column,
                image_size=image.shape,
                image_format=ImageFormat.ROW_MAJOR_GREYSCALE,
                image=image,
                mask=mask)


    def begin_draw(self):
        """
        Begins a drawing session on the Mechatronics Sensors Trainer LCD.

        Notes
        -----
        Use this function when multiple elements need to be drawn.
        After calling `begin_draw`, add all the elements to be drawn,
        then call `end_draw` to apply all changes in a single screen update.
        """
        self.display.beginDraw()

    def end_draw(self):
        """
        Ends a drawing session on the Mechatronics Sensors Trainer LCD.

        Notes
        -----
        This function finalizes the drawing session started with
        `begin_draw` and applies all pending changes to the display.
        """
        self.display.endDraw()

    def set_text_color(self, rgb=[255, 255, 255]):
        """
        Sets the text color on the Mechatronics Sensors Trainer LCD.

        Parameters
        ----------
        rgb : list of int, optional
            RGB color values for the text.
            Defaults to [255, 255, 255] (white).
        """
        self.display.setTextColor(rgb[0], rgb[1], rgb[2])

    def print_text(self,
                   message,
                   column=0,
                   line=0,
                   setColor=False,
                   rgb=[255, 255, 255]):
        """
        Prints text on the Mechatronics Sensors Trainer LCD.

        Parameters
        ----------
        message : str
            Message to be printed on the LCD.
        column : int, optional
            Column-coordinate of the message. Defaults to 0.
        line : int, optional
            Row-coordinate of the message. Defaults to 0 (max 23 lines).
        setColor : bool, optional
            Whether to set the text color before printing. Defaults to False.
            If multiple messages will have the same color,
            use the `set_text_color` function only once instead
        rgb : list of int, optional
            RGB color values for the text. Used only if `setColor` is True.
            Defaults to [255, 255, 255] (white).

        Notes
        -----
        If multiple messages will have the same color,
        use the `set_text_color` function once instead
        of setting the color for each message.
        """

        if setColor:
            self.set_text_color(rgb)

        try:
            self.display.printText(line, column, message, len(message))
        except DeviceError as e:
            print(e.get_error_message())

    def get_lcd_image(self, greyscale = False):
        """
        Return the current LCD screen content as a NumPy array of dtype uint8.
        Image can be color or greyscale, in OpenCV BGR format.

        Parameters
        ----------
        greyscale : bool, optional
            If True, return a 2-D greyscale image of shape (480, 800).
            If False, return a 3-D color image of shape (480, 800, 3).
            Default is False.

        Returns
        -------
        image_data : numpy.ndarray
            uint8 array containing the display image.
            Shape is (480, 800) for greyscale and (480, 800, 3) for color images.
            When a color image is returned, the channel order is BGR.

        Notes
        -----
        - The returned resolution corresponds to the device display (480 rows × 800 columns).
        - If you need an RGB image, convert using OpenCV:
          cv2.cvtColor(image_data, cv2.COLOR_BGR2RGB).

        """

        if not greyscale:
            # color openCV format
            image_data = np.zeros((480, 800, 3), dtype=np.uint8)
            self.display.getImage(ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8, image_data)
        else:
            # greyscale openCV format
            image_data = np.zeros((480, 800), dtype=np.uint8)
            self.display.getImage(ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8, image_data)

        return image_data

    def save(self, filename):
        """
        Saves the current contents of the display to a PBM image file.

        Parameters
        ----------
        filename : str
            Name of the file to save the image. If the `.pbm` extension
            is not included, it will be added automatically.

        Notes
        -----
        The saved file is in PBM format, which is a portable bitmap format.
        """

        root, ext = os.path.splitext(filename)
        if not ext:
            ext = '.pbm'
        path = root + ext

        self.display.save(path)

    def clear(self):
        """
        Clears the LCD display and resets it to the default background color.

        Notes
        -----
        This function removes all content from the display.
        """
        self.display.clear()

    def terminate(self):
        """
        Cleanly shuts down and terminates the connection with
        the Mechatronics Sensors Trainer LCD.

        Notes
        -----
        This function closes the connection to the LCD display.
        ****Terminates the device after setting final values for ???.
        """
        try:
            self.display.close()
            print('Board display closed gracefully.')
        except DeviceError as e:
            print(e.get_error_message())
        except Exception as e:
            print(e)

    def __enter__(self):
        """
        Used for the `with` statement.

        Returns
        -------
        SensorsDisplay
            The current instance of the class.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Used for the `with` statement.
        Terminates the connection with the Sensors Trainer Display.

        Parameters
        ----------
        exc_type : Exception type
            The exception type, if any.
        exc_value : Exception value
            The exception value, if any.
        traceback : Traceback
            The traceback object, if any.
        """
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

        # If another exception occurred, handle it
        if exc_type is not None:
            print(f"Exception occurred: {exc_type.__name__}: {exc_value}")

        # Always terminate the connection
        self.terminate()

        # Returning False allows other exceptions to propagate
        return False


class SensorsCamera(Camera2D):
    """ Class for accessing the camera in the Mechatronics Sensor Board.

    This class provides an interface to configure and access the camera on
    the Mechatronics Sensor Board. Camera data is stored
    in `self.imageData` after calling the `read` function.

    Notes
    -----
    - This class inherits from `Camera2D` and
        uses its functionality for camera configuration and data acquisition.
    - The `read` function must be called to populate
        `self.imageData` with the latest camera frame.
    """

    def __init__(
            self,
            cameraID = 0,
            frameWidth=640,
            frameHeight=480,
            frameRate=30,
            focalLength=np.array([[None], [None]], dtype=np.float64),
            principlePoint=np.array([[None], [None]], dtype=np.float64),
            skew=None,
            position=np.array([[None], [None], [None]], dtype=np.float64),
            orientation=np.array(
                [[None, None, None], [None, None, None], [None, None, None]],
                dtype=np.float64),
            imageFormat=0,  # 1 is greyscale
            brightness=None,
            contrast=None,
            gain=None,
            exposure=None):

        """
        Class for accessing the camera in the Mechatronics Sensor Board.

        Parameters
        ----------
        frameWidth : int, optional
            Width of the camera frame in pixels. Defaults to 640.
        frameHeight : int, optional
            Height of the camera frame in pixels. Defaults to 400.
        frameRate : int, optional
            Frame rate of the camera in frames per second. Defaults to 30.
        focalLength : numpy.ndarray, optional
            Camera focal length in pixels.
            Defaults to `np.array([[None], [None]], dtype=np.float64)`.
        principlePoint : numpy.ndarray, optional
            Principal point of the camera in pixels.
            Defaults to `np.array([[None], [None]], dtype=np.float64)`.
        skew : float, optional
            Skew factor for the camera. Defaults to None.
        position : numpy.ndarray, optional
            Position of the camera in the device's frame of reference.
            Should be a 3x1 array.
            Defaults to `np.array([[None], [None], [None]], dtype=np.float64)`.
        orientation : numpy.ndarray, optional
            Orientation of the camera in the device's frame of reference.
            Should be a 3x3 array.
            Defaults to `np.array([[None, None, None], [None, None, None], [None, None, None]], dtype=np.float64)`.
        imageFormat : int, optional
            Format of the camera image. Use 0 for color and 1 for greyscale.
            Defaults to 0.
        brightness : float, optional
            Brightness setting for the camera. Defaults to None.
        contrast : float, optional
            Contrast setting for the camera. Defaults to None.
        gain : float, optional
            Gain setting for the camera. Defaults to None.
        exposure : float, optional
            Exposure setting for the camera. Defaults to None.

        Notes
        -----
        - The `read` function must be called to populate
            `self.imageData` with the latest camera frame.
        """

        deviceId = str(cameraID)

        super().__init__(
            cameraId=str(deviceId),
            frameWidth=frameWidth,
            frameHeight=frameHeight,
            frameRate=frameRate,
            focalLength=focalLength,
            principlePoint=principlePoint,
            skew=skew,
            position=position,
            orientation=orientation,
            imageFormat=imageFormat,
            brightness=brightness,
            contrast=contrast,
            gain=gain,
            exposure=exposure
        )



def find_audio_in(partial_name = 'Sensors Trainer'):
    """
    Finds the index of an audio input device whose name contains the given substring.

    Parameters
    ----------
    partial_name : str
        Substring to search for in the device name.

    Returns
    -------
    int
        Index of the matching audio input device.

    Raises
    ------
    ValueError
        If no input device matching the substring is found.

    Notes
    -----
    Uses the `sounddevice` library to query available audio devices.
    Only devices with at least one input channel are considered.
    """
    import sounddevice as sd

    for i, device in enumerate(sd.query_devices()):
        if partial_name in device['name'] and device['max_input_channels'] > 0:
            print("Using input device:", device['name'], "ID:" , i)
            return i
    raise ValueError(f"No input device matching '{partial_name}' found")


def find_audio_out(partial_name = 'Sensors Trainer'):
    """
    Finds the index of an audio output device whose name contains the given substring.

    Parameters
    ----------
    partial_name : str
        Substring to search for in the device name.

    Returns
    -------
    int
        Index of the matching audio output device.

    Raises
    ------
    ValueError
        If no output device matching the substring is found.

    Notes
    -----
    Uses the `sounddevice` library to query available audio devices.
    Only devices with at least one output channel are considered.
    """
    import sounddevice as sd

    for i, device in enumerate(sd.query_devices()):
        if partial_name in device['name'] and device['max_output_channels'] > 0:
            print("Using output device:", device['name'], "ID:" , i)
            return i
    raise ValueError(f"No output device matching '{partial_name}' found")
