"""qarm_mini: Classes to simplify interactions with the QArm Mini.

This module provides a set of API classes and tools to facilitate working with
the QArm Mini. It is designed to make it easy to read and write
all available inputs/outputs of the QArm Mini.
"""

import numpy as np
from quanser.hardware import HIL, HILError, MAX_STRING_LENGTH
from pal.utilities.vision import Camera2D

class QArmMini():

    HOME_POSE  = np.array([0, np.pi / 2, -np.pi / 2, np.pi / 2], dtype=np.float64)
    SLEEP_POSE = np.array([0, 0, 0, np.pi / 2], dtype=np.float64)

    LIMITS_MAX = np.array([4*np.pi/3, 13*np.pi/12, np.pi/6, 8*np.pi/9], dtype=np.float64)
    LIMITS_MIN = np.array([-10*np.pi/18, -np.pi/6, -5*np.pi/6, -np.pi/10], dtype=np.float64)

    def __init__(self,
                 id=0,
                 hardware=1,
                 boardSpecificOptions = ('j0_mode=0;j1_mode=0;j2_mode=0;j3_mode=0;'
                 'gripper_mode=0;j0_profile_velocity=6.2832;j0_profile_acceleration=6.2832;'
                 'j1_profile_velocity=6.2832;j1_profile_acceleration=6.2832;'
                 'j2_profile_velocity=6.2832;j2_profile_acceleration=6.2832;'
                 'j3_profile_velocity=6.2832;j3_profile_acceleration=6.2832;'
                 'gripper_profile_velocity=6.2832;gripper_profile_acceleration=6.2832;'),
                 pGain = [5, 10, 10, 10, 20],
                 iGain = [-1, 0.036, 0.036, -1, -1],
                 dGain = [200, 0, 0, 0, 0],
                 ffVGain = [-1, -1, -1, -1, -1],
                 ffAGain = [-1, -1, -1, -1, -1]
        ):
        """This function initializes and configures the QArm Mini.

        Args:
            id (int, optional): Board identifier id number for virtual
                use only. Defaults to 0.
            hardware (int, optional): Indicates whether to use hardware
                or virtual QArm Mini. (0 for virtual, 1 for hardware). Defaults to 0.
            frequency (int, optional): Sampling frequency
                (used when readMode is set to 1). Defaults to 100.
            readMode (int, optional): Indicates the read mode.
                (0 for immediate I/O, 1 for task-based I/O). Defaults to 0.  # delete this and frequency
            boardSpecificOptions (str, optional): board specific options
                for the QArm Mini.
        """

        # Channels - particular input or output signal from data acquisition card

        self.WRITE_OTHER_CHANNELS = np.array(
            [1000, 1001, 1002, 1003, 1004,
             11000, 11001, 11002, 11003, 11004],
            dtype=np.uint32)

        self.READ_ANALOG_CHANNELS = np.array(
            [0, 1, 2, 3, 4],
            dtype=np.uint32)
        self.READ_OTHER_CHANNELS = np.array(
            [1000, 1001, 1002, 1003, 1004,
             3000, 3001, 3002, 3003, 3004,
            10000, 10001, 10002, 10003, 10004,
            11000, 11001, 11002, 11003, 11004],
            dtype=np.uint32)

        # Internal read buffers
        self._readAnalogBuffer = np.zeros(
            len(self.READ_ANALOG_CHANNELS),
            dtype=np.float64)
        self._readOtherBuffer = np.zeros(
            len(self.READ_OTHER_CHANNELS),
            dtype=np.float64)

        # External read buffers
        self.positionMeasured = np.zeros(4, dtype=np.float64)
        self.gripperPositionMeasured = np.zeros(1, dtype=np.float64)

        self.speedMeasured = np.zeros(4, dtype=np.float64)
        self.gripperSpeedMeasured = np.zeros(1, dtype=np.float64)

        self.currentMeasured = np.zeros(4, dtype=np.float64)
        self.gripperCurrentMeasured = np.zeros(1, dtype=np.float64)

        readMode=0
        frequency=100

        self._hardware = hardware
        self._readMode = readMode
        self._id = str(id)
        self._boardSpecificOptions = boardSpecificOptions

        #boardIdentifier

        if self._hardware:
            boardIdentifier = self._id
        else:
            boardIdentifier = self._id + "@tcpip://localhost:18916?nagle='off'"

        try:
            # Open the Card
            self.card = HIL("qarm_mini", boardIdentifier)

            if self.card.is_valid():
                # Set PWM options
                self.card.set_card_specific_options(
                    self._boardSpecificOptions,
                    MAX_STRING_LENGTH)

                properties = np.array( # in order, yaw, shoulder, elbow and wrist joint + gripper
                    [128, 129, 130, 131, 132, # position P gain
                     133, 134, 135, 136, 137, # position I gain
                     138, 139, 140, 141, 142, # position D gain
                     143, 144, 145, 146, 147, # feedforward velocity gain
                     148, 149, 150 ,151, 152], # feedforward acceleration gain
                     dtype=np.int32)

                # pGain             >  Proportional Gain (0 to 127  or -1 for default)
                # iGain             > Integral Gain (0 to 0.24  or -1 for default)
                # dGain             > Derivative Gain (0 to 1023  or -1 for default)
                # velocityGain      > Velocity FF Gain (0 to 4095  or -1 for default)
                # accelerationGain  > Acceleration FF Gain (0 to 4095  or -1 for default)
                bufferProperties = np.concatenate(
                    [pGain,
                     iGain,
                     dGain,
                     ffVGain,
                     ffAGain],
                     dtype=np.float64)

                self.card.set_double_property(properties,
                                              len(properties),
                                              bufferProperties)

                print('QArm Mini configured successfully.')

        except HILError as h:
            print(h.get_error_message())

    def write_joint_positions(self,
                      joints = np.array([0, np.pi/2, -np.pi/2, np.pi/2], dtype=np.float64)):
        """Writes joint position commands to the QArm Mini.
            Makes PWM commands all 0 to prevent both being written at the same time.
        Args:
            joints (ndarray, float): commanded joint position (rad) [yaw, shoulder, elbow, wrist]
        """

        # in rads
        if len(joints) != 4:
            print ('Please provide all 4 joint positions. Going HOME instead.')
            joints = self.HOME_POSE

        thetaBias = [0,
                     -np.pi/2,
                     np.pi/2,
                     -np.pi/2]

        actuatorBias = [np.pi - 1.178,
                        np.pi +  0.1834,
                        np.pi - 0.1834 + 0.07,
                        np.pi]

        joints = np.clip(joints, self.LIMITS_MIN, self.LIMITS_MAX) + thetaBias + actuatorBias
        pwm =  np.array([0, 0, 0, 0])

        values = np.concatenate([joints, pwm])

        writeChannels = np.concatenate(
            [self.WRITE_OTHER_CHANNELS[0:4],
             self.WRITE_OTHER_CHANNELS[5:9]])
        try:
            self.card.write_other(
                writeChannels,
                len(writeChannels),
                np.array(values, dtype=np.float64))

        except HILError as h:
            print(h.get_error_message())

    def write_gripper_position(self, gripper = 0):
        """Writes gripper position command to the QArm Mini.
            Makes PWM command 0 to prevent both being written at the same time.
        Args:
            gripper (float): commanded joint position (%) [0-1]
        """

        gripper = np.array([gripper])
        np.clip(gripper, 0, 1, out = gripper)

        gripper = gripper * -1.8 - 0.9

        thetaBias = [0]
        actuatorBias = [np.pi]
        gripper = gripper + thetaBias + actuatorBias

        gripperPwm =  np.array([0])

        values = np.concatenate([gripper, gripperPwm])

        writeChannels = np.array(
            [self.WRITE_OTHER_CHANNELS[4],
             self.WRITE_OTHER_CHANNELS[9]])

        try:
            self.card.write_other(
                writeChannels,
                len(writeChannels),
                np.array(values, dtype=np.float64))

        except HILError as h:
            print(h.get_error_message())

    def write_joint_PWM(self,
                      jointsPWM = np.array([0, 0, 0, 0], dtype=np.float64)):
        """
        Writes joint PWM commands to the QArm Mini.
            Makes position commands all 0 to prevent both being written at the same time.
        Args:
            jointsPWM (ndarray, float): commanded joint PWM (%) [-1 - 1] [yaw, shoulder, elbow, wrist]
        """

        # in percentage (- 1 to 1)
        if len(jointsPWM) != 4:
            print ('Joint values 0. Please provide all 4 joint positions.')
            jointsPWM = np.array([0, 0, 0, 0], dtype=np.float64)

        np.clip(jointsPWM, -1, 1, out = jointsPWM)

        writeChannels = self.WRITE_OTHER_CHANNELS[5:9]

        try:
            self.card.write_other(
                writeChannels,
                len(writeChannels),
                np.array(jointsPWM, dtype=np.float64))

        except HILError as h:
            print(h.get_error_message())

    def write_gripper_PWM(self, gripperPWM = 0):
        """
        Writes gripper PWM command to the QArm Mini.
            Makes position command all 0 to prevent both being written at the same time.
        Args:
             gripper (float): commanded joint position (%) [0-1]
        """
        gripperPWM = np.array([gripperPWM])
        np.clip(gripperPWM, -1, 1, out = gripperPWM)

        writeChannels = self.WRITE_OTHER_CHANNELS[9]

        try:
            self.card.write_other(
                writeChannels,
                len(writeChannels),
                np.array(gripperPWM, dtype=np.float64))

        except HILError as h:
            print(h.get_error_message())

    def read_outputs(self):
        """
        Reads the outputs and stores them in their respective member variables.

        These are the read variables:

        self.positionMeasured (ndarray, float): measured joint position (rad) [yaw, shoulder, elbow, wrist]
        self.gripperPositionMeasured (float): measured gripper position (%)

        self.speedMeasured (ndarray, float): measured joint speed (rad/s) [yaw, shoulder, elbow, wrist]
        self.gripperSpeedMeasured (float): measured gripper speed (%/s)

        self.currentMeasured (ndarray, float): measured joint current (Amps) [yaw, shoulder, elbow, wrist]
        self.gripperCurrentMeasured (float): measured gripper current (Amps)
        """
        try:
            if self._readMode == 1:
                self.card.task_read(
                    self._readTask,
                    self.samplesToRead,
                    self._readAnalogBuffer,
                    None,
                    None,
                    self._readOtherBuffer
                )
            else:
                self.card.read(
                    self.READ_ANALOG_CHANNELS,
                    len(self.READ_ANALOG_CHANNELS),
                    None,
                    0,
                    None,
                    0,
                    self.READ_OTHER_CHANNELS,
                    len(self.READ_OTHER_CHANNELS),
                    self._readAnalogBuffer,
                    None,
                    None,
                    self._readOtherBuffer
                )

        except HILError as h:
            print(h.get_error_message())
        finally:

            thetaBias = [0,
                        np.pi/2,
                        -np.pi/2,
                        np.pi/2]
            actuatorBias = [-(np.pi - 1.178),
                            -(np.pi +  0.1834),
                            -(np.pi - 0.1834 + 0.07),
                            -(np.pi)]

            self.positionMeasured = self._readOtherBuffer[0:4] + thetaBias + actuatorBias

            thetaBias = [0]
            actuatorBias = [-np.pi]
            self.gripperPositionMeasured = self._readOtherBuffer[4]  + thetaBias + actuatorBias
            self.gripperPositionMeasured = (self.gripperPositionMeasured - 0.9) / -1.8

            self.speedMeasured = self._readOtherBuffer[5:9]
            self.gripperSpeedMeasured = self._readOtherBuffer[9]

            self.currentMeasured = self._readAnalogBuffer[0:4]
            self.gripperCurrentMeasured = self._readAnalogBuffer[4]

    def read_write_std(self, joints = np.array([0, np.pi/2, -np.pi/2, np.pi/2], dtype=np.float64), gripper = 0):

        writeFlag = True
        if len(joints) != 4:
            print ('Please provide all 4 joint positions. Going HOME instead.')
            writeFlag = False

        thetaBias = [0,
                     -np.pi/2,
                     np.pi/2,
                     -np.pi/2]

        actuatorBias = [np.pi - 1.178,
                        np.pi +  0.1834,
                        np.pi - 0.1834 + 0.07,
                        np.pi]

        joints = np.clip(joints, self.LIMITS_MIN, self.LIMITS_MAX) + thetaBias + actuatorBias

        gripper = np.array([gripper])
        np.clip(gripper, 0, 1, out = gripper)

        gripper = gripper * 1.68 - 0.9

        gripper = gripper + [np.pi]
        pwm =  np.array([0, 0, 0, 0])
        gripperPWM =  np.array([0])

        values = np.concatenate([joints, gripper, pwm, gripperPWM])

        writeChannels = self.WRITE_OTHER_CHANNELS

        try:
            if writeFlag:
                self.card.write_other(
                    writeChannels,
                    len(writeChannels),
                    np.array(values, dtype=np.float64))

            self.card.read(
                self.READ_ANALOG_CHANNELS,
                len(self.READ_ANALOG_CHANNELS),
                None,
                0,
                None,
                0,
                self.READ_OTHER_CHANNELS,
                len(self.READ_OTHER_CHANNELS),
                self._readAnalogBuffer,
                None,
                None,
                self._readOtherBuffer
            )

        except HILError as h:
            print(h.get_error_message())
        finally:

            self.positionMeasured = self._readOtherBuffer[0:4] - thetaBias - actuatorBias

            self.gripperPositionMeasured = self._readOtherBuffer[4]  + [-np.pi]
            self.gripperPositionMeasured = (self.gripperPositionMeasured + 0.9) / 1.68

            self.speedMeasured = self._readOtherBuffer[5:9]
            self.gripperSpeedMeasured = self._readOtherBuffer[9]

            self.currentMeasured = self._readAnalogBuffer[0:4]
            self.gripperCurrentMeasured = self._readAnalogBuffer[4]

        pass

    def terminate(self):
        """Cleanly shutdown and terminate connection with QArm Mini

        Terminates the QArm Mini card after setting final values for joints to 0.
        Also terminates the task reader.
        """
        try:
            self.write_joint_positions()

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
        """Used for with statement.
           Terminates the connection with QArm Mini."""
        self.terminate()


# class QArmMiniCamera(Camera2D):

#     """Class for accessing the QBot Platform CSI camera.

#     Args:
#         frameWidth (int, optional): Width of the camera frame.
#             Defaults to 640.
#         frameHeight (int, optional): Height of the camera frame.
#             Defaults to 400.
#         frameRate (int, optional): Frame rate of the camera.
#             Defaults to 30.

#     """

#     def __init__(

#             self,
#             frameWidth=640,
#             frameHeight=400,
#             frameRate=60.0,
#             focalLength=np.array([[None], [None]], dtype=np.float64),
#             principlePoint=np.array([[None], [None]], dtype=np.float64),
#             skew=None,
#             position=np.array([[None], [None], [None]], dtype=np.float64),
#             orientation=np.array(
#                 [[None,None,None], [None,None,None], [None,None,None]],
#                 dtype=np.float64),
#             brightness = None, #won't work on qbot platform downward facing
#             contrast = None, #won't work on qbot platform downward facing
#             gain = None,
#             exposure = None,
#         ):

#         if IS_PHYSICAL_QBOTPLATFORM:
#             deviceId = '6'
#         else:
#             deviceId = "6@tcpip://localhost:18915"
#         super().__init__(
#             cameraId=deviceId,
#             frameWidth=frameWidth,
#             frameHeight=frameHeight,
#             frameRate=frameRate,
#             focalLength = focalLength,
#             principlePoint = principlePoint,
#             skew = skew,
#             position=position,
#             orientation=orientation,
#             imageFormat=1,
#             brightness = brightness,
#             contrast = contrast,
#             gain = gain,
#             exposure = exposure
#         )
