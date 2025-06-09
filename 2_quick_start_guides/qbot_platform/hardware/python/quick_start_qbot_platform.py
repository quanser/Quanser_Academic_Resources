#-----------------------------------------------------------------------------#
#-----------------------Quick Start Guide for Python--------------------------#
#-----------------------------------------------------------------------------#
#------------------QBot Platform with Mobile Robotics Lab----------------------#
#-----------------------------------------------------------------------------#

# Imports
import os
import sys
import platform
import cv2
import numpy as np
import platform
import time
from quanser.devices import (
    RangingMeasurements,
    RangingMeasurementMode,
    DeviceError,
    RangingDistance
)
from quanser.multimedia import Video3D, Video3DStreamType, VideoCapture, \
    MediaError, ImageFormat, ImageDataType, VideoCapturePropertyCode, \
    VideoCaptureAttribute
from quanser.communications import Stream, StreamError, PollFlag
try:
    from quanser.common import Timeout
except:
    from quanser.communications import Timeout

from quanser.devices import GameController

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

class BasicStream:
    '''Class object consisting of basic stream server/client functionality'''
    def __init__(self, uri, agent='S', receiveBuffer=np.zeros(1, dtype=np.float64), sendBufferSize=2048, recvBufferSize=2048, nonBlocking=False, verbose=False):
        '''
        This functions simplifies functionality of the quanser_stream module to provide a
        simple server or client. \n
         \n
        uri - IP server and port in one string, eg. 'tcpip://IP_ADDRESS:PORT' \n
        agent - 'S' or 'C' string representing server or client respectively \n
        receiveBuffer - numpy buffer that will be used to determine the shape and size of data received \n
        sendBufferSize - (optional) size of send buffer, default is 2048 \n
        recvBufferSize - (optional) size of recv buffer, default is 2048 \n
        nonBlocking - set to False for blocking, or True for non-blocking connections \n
         \n
        Stream Server as an example running at IP 192.168.2.4 which receives two doubles from the client: \n
        >>> myServer = BasicStream('tcpip://localhost:18925', 'S', receiveBuffer=np.zeros((2, 1), dtype=np.float64))
         \n
        Stream Client as an example running at IP 192.168.2.7 which receives a 480 x 640 color image from the server: \n
        >>> myClient = BasicStream('tcpip://192.168.2.4:18925', 'C', receiveBuffer=np.zeros((480, 640, 3), dtype=np.uint8))

        '''
        self.agent 			= agent
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize
        self.uri 			= uri
        self.receiveBuffer  = receiveBuffer
        self.verbose        = verbose
        # If the agent is a Client, then Server isn't needed.
        # If the agent is a Server, a Client will also be needed. The server can start listening immediately.

        self.clientStream = Stream()
        if agent=='S':
            self.serverStream = Stream()

        # Set polling timeout to 10 milliseconds
        self.t_out = Timeout(seconds=0, nanoseconds=10000000)

        # connected flag initialized to False
        self.connected = False

        try:
            if agent == 'C':
                self.connected = self.clientStream.connect(uri, nonBlocking, self.sendBufferSize, self.recvBufferSize)
                if self.connected and self.verbose:
                    print('Connected to a Server successfully.')

            elif agent == 'S':
                if self.verbose:
                    print('Listening for incoming connections.')
                self.serverStream.listen(self.uri, nonBlocking)
            pass

        except StreamError as e:
            if self.agent == 'S' and self.verbose:
                print('Server initialization failed.')
            elif self.agent == 'C' and self.verbose:
                print('Client initialization failed.')
            print(e.get_error_message())

    def checkConnection(self, timeout=Timeout(seconds=0, nanoseconds=100)):
        '''When using non-blocking connections (nonBlocking set to True), the constructor method for this class does not block when
        listening (as a server) or connecting (as a client). In such cases, use the checkConnection method to attempt continuing to
        accept incoming connections (as a server) or connect to a server (as a client).  \n
         \n
        Stream Server as an example \n
        >>> while True:
        >>> 	if not myServer.connected:
        >>> 		myServer.checkConnection()
        >>>		if myServer.connected:
        >>> 		yourCodeGoesHere()
         \n
        Stream Client as an example \n
        >>> while True:
        >>> 	if not myClient.connected:
        >>> 		myClient.checkConnection()
        >>>		if myClient.connected:
        >>> 		yourCodeGoesHere()
         \n
        '''
        if self.agent == 'C' and not self.connected:
            try:
                pollResult = self.clientStream.poll(timeout, PollFlag.CONNECT)

                if (pollResult & PollFlag.CONNECT) == PollFlag.CONNECT:
                    self.connected = True
                    if self.verbose: print('Connected to a Server successfully.')

            except StreamError as e:
                if e.error_code == -33:
                    self.connected = self.clientStream.connect(self.uri, True, self.sendBufferSize, self.recvBufferSize)
                else:
                    if self.verbose: print('Client initialization failed.')
                    print(e.get_error_message())

        if self.agent == 'S' and not self.connected:
            try:
                pollResult = self.serverStream.poll(self.t_out, PollFlag.ACCEPT)
                if (pollResult & PollFlag.ACCEPT) == PollFlag.ACCEPT:
                    self.connected = True
                    if self.verbose: print('Found a Client successfully...')
                    self.clientStream = self.serverStream.accept(self.sendBufferSize, self.recvBufferSize)

            except StreamError as e:
                if self.verbose: print('Server initialization failed...')
                print(e.get_error_message())

    def terminate(self):
        '''Use this method to correctly shutdown and then close connections. This method automatically closes all streams involved (Server will shutdown server streams as well as client streams). \n
         \n
        Stream Server as an example \n
        >>> while True:
        >>> 	if not myServer.connected:
        >>> 		myServer.checkConnection()
        >>>		if myServer.connected:
        >>> 		yourCodeGoesHere()
        >>>			if breakCondition:
        >>>				break
        >>> myServer.terminate()
         \n
        Stream Client as an example	 \n
        >>> while True:
        >>> 	if not myClient.connected:
        >>> 		myClient.checkConnection()
        >>>		if myClient.connected:
        >>> 		yourCodeGoesHere()
        >>>			if breakCondition:
        >>>				break
        >>> myClient.terminate()

        '''

        if self.connected:
            self.clientStream.shutdown()
            self.clientStream.close()
            if self.verbose: print('Successfully terminated clients...')

        if self.agent == 'S':
            self.serverStream.shutdown()
            self.serverStream.close()
            if self.verbose: print('Successfully terminated servers...')

    def receive(self, iterations=1, timeout=Timeout(seconds=0, nanoseconds=10)):
        '''
        This functions populates the receiveBuffer with bytes if available. \n \n

        Accepts: \n
        iterations - (optional) number of times to poll for incoming data before terminating, default is 1 \n
         \n
        Returns: \n
        receiveFlag - flag indicating whether the number of bytes received matches the expectation. To check the actual number of bytes received, use the bytesReceived class object. \n
         \n
        Stream Server as an example \n
        >>> while True:
        >>> 	if not myServer.connected:
        >>> 		myServer.checkConnection()
        >>>		if myServer.connected:
        >>> 		flag = myServer.receive()
        >>>			if breakCondition or not flag:
        >>>				break
        >>> myServer.terminate()
         \n
        Stream Client as an example	 \n
        >>> while True:
        >>> 	if not myClient.connected:
        >>> 		myClient.checkConnection()
        >>>		if myClient.connected:
        >>> 		flag = myServer.receive()
        >>>			if breakCondition or not flag:
        >>>				break
        >>> myClient.terminate()

        '''

        self.t_out = timeout
        counter = 0
        dataShape = self.receiveBuffer.shape

        # Find number of bytes per array cell based on type
        numBytesBasedOnType = len(np.array([0], dtype=self.receiveBuffer.dtype).tobytes())

        # Calculate total dimensions
        dim = 1
        for i in range(len(dataShape)):
            dim = dim*dataShape[i]

        # Calculate total number of bytes needed and set up the bytearray to receive that
        totalNumBytes = dim*numBytesBasedOnType
        self.data = bytearray(totalNumBytes)
        self.bytesReceived = 0
        # print(totalNumBytes)
        # Poll to see if data is incoming, and if so, receive it. Poll a max of 'iteration' times
        try:
            while True:

                # See if data is available
                pollResult = self.clientStream.poll(self.t_out, PollFlag.RECEIVE)
                counter += 1
                if not (iterations == 'Inf'):
                    if counter > iterations:
                        break
                if not ((pollResult & PollFlag.RECEIVE) == PollFlag.RECEIVE):
                    continue # Data not available, skip receiving

                # Receive data
                self.bytesReceived = self.clientStream.receive_byte_array(self.data, totalNumBytes)

                # data received, so break this loop
                break

            #  convert byte array back into numpy array and reshape.
            self.receiveBuffer = np.reshape(np.frombuffer(self.data, dtype=self.receiveBuffer.dtype), dataShape)

        except StreamError as e:
            print(e.get_error_message())
        finally:
            receiveFlag = self.bytesReceived==1
            return receiveFlag, totalNumBytes*self.bytesReceived

    def send(self, buffer):
        """
        This functions sends the data in the numpy array buffer
        (server or client). \n \n

        INPUTS: \n
        buffer - numpy array of data to be sent \n

        OUTPUTS: \n
        bytesSent - number of bytes actually sent (-1 if send failed) \n
         \n
        Stream Server as an example \n
        >>> while True:
        >>> 	if not myServer.connected:
        >>> 		myServer.checkConnection()
        >>>		if myServer.connected:
        >>> 		sent = myServer.send()
        >>>			if breakCondition or sent == -1:
        >>>				break
        >>> myServer.terminate()
         \n
        Stream Client as an example	 \n
        >>> while True:
        >>> 	if not myClient.connected:
        >>> 		myClient.checkConnection()
        >>>		if myClient.connected:
        >>> 		sent = myServer.send()
        >>>			if breakCondition or sent == -1:
        >>>				break
        >>> myClient.terminate()

        """

        # Set up array to hold bytes to be sent
        byteArray = buffer.tobytes()
        self.bytesSent = 0

        # Send bytes and flush immediately after
        try:
            self.bytesSent = self.clientStream.send_byte_array(byteArray, len(byteArray))
            self.clientStream.flush()
        except StreamError as e:
            print(e.get_error_message())
            self.bytesSent = -1 # If an error occurs, set bytesSent to -1 for user to check
        finally:
            return self.bytesSent

class Camera3D():
    def __init__(
            self,
            mode='RGB, Depth',
            frameWidthRGB=1920,
            frameHeightRGB=1080,
            frameRateRGB=30.0,
            frameWidthDepth=1280,
            frameHeightDepth=720,
            frameRateDepth=15.0,
            frameWidthIR=1280,
            frameHeightIR=720,
            frameRateIR=15.0,
            deviceId='0',
            readMode=1,
            focalLengthRGB=np.array([[None], [None]], dtype=np.float64),
            principlePointRGB=np.array([[None], [None]], dtype=np.float64),
            skewRGB=None,
            positionRGB=np.array([[None], [None], [None]], dtype=np.float64),
            orientationRGB=np.array(
                [[None, None, None], [None, None, None], [None, None, None]],
                dtype=np.float64),
            focalLengthDepth=np.array([[None], [None]], dtype=np.float64),
            principlePointDepth=np.array([[None], [None]], dtype=np.float64),
            skewDepth=None,
            positionDepth=np.array([[None], [None], [None]], dtype=np.float64),
            orientationDepth=np.array(
                [[None, None, None], [None, None, None], [None, None, None]],
                dtype=np.float64)
        ):
        """This class configures RGB-D cameras (eg. Intel Realsense) for use.

        By default, mode is set to RGB&DEPTH, which reads both streams.
        Set it to RGB or DEPTH to get exclusive RGB or DEPTH streaming.
        If you specify focal lengths, principle points, skew as well as
        camera position & orientation in the world/inertial frame,
        camera instrinsics/extrinsic matrices can also be extracted
        using corresponding methods in this class.
        """

        self.mode = mode
        self.readMode = readMode
        self.streamIndex = 0

        self.imageBufferRGB = np.zeros(
            (frameHeightRGB, frameWidthRGB, 3),
            dtype=np.uint8
        )
        self.imageBufferDepthPX = np.zeros(
            (frameHeightDepth, frameWidthDepth, 1),
            dtype=np.uint16
        )
        self.imageBufferDepthM = np.zeros(
            (frameHeightDepth, frameWidthDepth, 1),
            dtype=np.float32
        )
        self.imageBufferIRLeft = np.zeros(
            (frameHeightIR, frameWidthIR, 1),
            dtype=np.uint8
        )
        self.imageBufferIRRight = np.zeros(
            (frameHeightIR, frameWidthIR, 1),
            dtype=np.uint8
        )

        self.frameWidthRGB = frameWidthRGB
        self.frameHeightRGB = frameHeightRGB
        self.frameWidthDepth = frameWidthDepth
        self.frameHeightDepth = frameHeightDepth
        self.frameWidthIR = frameWidthIR
        self.frameHeightIR = frameHeightIR

        self.focalLengthRGB = 2*focalLengthRGB
        self.focalLengthRGB[0, 0] = -self.focalLengthRGB[0, 0]
        self.principlePointRGB = principlePointRGB
        self.skewRGB = skewRGB
        self.positionRGB = positionRGB
        self.orientationRGB = orientationRGB

        self.focalLengthDepth = 2*focalLengthDepth
        self.focalLengthDepth[0, 0] = -self.focalLengthDepth[0, 0]
        self.principlePointDepth = principlePointDepth
        self.skewDepth = skewDepth
        self.positionDepth = positionDepth
        self.orientationDepth = orientationDepth

        try:
            self.video3d = Video3D(deviceId)
            self.streamOpened = False
            if 'rgb' in self.mode.lower():
                self.streamRGB = self.video3d.stream_open(
                    Video3DStreamType.COLOR,
                    self.streamIndex,
                    frameRateRGB,
                    frameWidthRGB,
                    frameHeightRGB,
                    ImageFormat.ROW_MAJOR_INTERLEAVED_BGR,
                    ImageDataType.UINT8
                )
                self.streamOpened = True
            if 'depth' in self.mode.lower():
                self.streamDepth = self.video3d.stream_open(
                    Video3DStreamType.DEPTH,
                    self.streamIndex,
                    frameRateDepth,
                    frameWidthDepth,
                    frameHeightDepth,
                    ImageFormat.ROW_MAJOR_GREYSCALE,
                    ImageDataType.UINT16
                )
                self.streamOpened = True
            if 'ir' in self.mode.lower():
                self.streamIRLeft = self.video3d.stream_open(
                    Video3DStreamType.INFRARED,
                    1,
                    frameRateIR,
                    frameWidthIR,
                    frameHeightIR,
                    ImageFormat.ROW_MAJOR_GREYSCALE,
                    ImageDataType.UINT8
                )
                self.streamIRRight = self.video3d.stream_open(
                    Video3DStreamType.INFRARED,
                    2,
                    frameRateIR,
                    frameWidthIR,
                    frameHeightIR,
                    ImageFormat.ROW_MAJOR_GREYSCALE,
                    ImageDataType.UINT8
                )
                self.streamOpened = True
            # else:
            #     self.streamRGB = self.video3d.stream_open(
            #         Video3DStreamType.COLOR,
            #         self.streamIndex,
            #         frameRateRGB,
            #         frameWidthRGB,
            #         frameHeightRGB,
            #         ImageFormat.ROW_MAJOR_INTERLEAVED_BGR,
            #         ImageDataType.UINT8
            #     )
            #     self.streamDepth = self.video3d.stream_open(
            #         Video3DStreamType.DEPTH,
            #         self.streamIndex,
            #         frameRateDepth,
            #         frameWidthDepth,
            #         frameHeightDepth,
            #         ImageFormat.ROW_MAJOR_GREYSCALE,
            #         ImageDataType.UINT8
            #     )
            #     self.streamOpened = True
            self.video3d.start_streaming()
        except MediaError as me:
            print(me.get_error_message())

    def terminate(self):
        """Terminates all started streams correctly."""

        try:
            self.video3d.stop_streaming()
            if self.streamOpened:
                if 'rgb' in self.mode.lower():
                    self.streamRGB.close()
                if 'depth' in self.mode.lower():
                    self.streamDepth.close()
                if 'ir' in self.mode.lower():
                    self.streamIRLeft.close()
                    self.streamIRRight.close()

            self.video3d.close()

        except MediaError as me:
            print(me.get_error_message())

    def read_RGB(self):
        """Reads an image from the RGB stream. It returns a timestamp
            for the frame just read. If no frame was available, it returns -1.
        """

        timestamp = -1
        try:
            frame = self.streamRGB.get_frame()
            while not frame:
                if not self.readMode:
                    break
                frame = self.streamRGB.get_frame()
            if not frame:
                pass
            else:
                frame.get_data(self.imageBufferRGB)
                timestamp = frame.get_timestamp()
                frame.release()
        except KeyboardInterrupt:
            pass
        except MediaError as me:
            print(me.get_error_message())
        finally:
            return timestamp

    def read_depth(self, dataMode='PX'):
        """Reads an image from the depth stream. Set dataMode to
            'PX' for pixels or 'M' for meters. Use the corresponding image
            buffer to get image data. If no frame was available, it returns -1.
        """
        timestamp = -1
        try:
            frame = self.streamDepth.get_frame()
            while not frame:
                if not self.readMode:
                    break
                frame = self.streamDepth.get_frame()
            if not frame:
                pass
            else:
                if dataMode == 'PX':
                    frame.get_data(self.imageBufferDepthPX)
                elif dataMode == 'M':
                    frame.get_meters(self.imageBufferDepthM)
                timestamp = frame.get_timestamp()
                frame.release()
        except KeyboardInterrupt:
            pass
        except MediaError as me:
            print(me.get_error_message())
        finally:
            return timestamp

    def read_IR(self, lens='LR'):
        """Reads an image from the left and right IR streams
            based on the lens parameter (L or R). Use the corresponding
            image buffer to get image data. If no frame was available,
            it returns -1.
        """
        timestamp = -1
        try:
            if 'l' in lens.lower():
                frame = self.streamIRLeft.get_frame()
                while not frame:
                    if not self.readMode:
                        break
                    frame = self.streamIRLeft.get_frame()
                if not frame:
                    pass
                else:
                    frame.get_data(self.imageBufferIRLeft)
                    timestamp = frame.get_timestamp()
                    frame.release()
            if 'r' in lens.lower():
                frame = self.streamIRRight.get_frame()
                while not frame:
                    if not self.readMode:
                        break
                    frame = self.streamIRRight.get_frame()
                if not frame:
                    pass
                else:
                    frame.get_data(self.imageBufferIRRight)
                    timestamp = frame.get_timestamp()
                    frame.release()
        except KeyboardInterrupt:
            pass
        except MediaError as me:
            print(me.get_error_message())
        finally:
            return timestamp

    def extrinsics_rgb(self):
        """Provides the Extrinsic Matrix for the RGB Camera"""
        # define rotation matrix from camera frame into the body frame
        transformFromCameraToBody = np.concatenate(
            (np.concatenate((self.orientationRGB, self.positionRGB), axis=1),
                [[0, 0, 0, 1]]),
            axis=0
        )

        return np.linalg.inv(transformFromCameraToBody)



    def intrinsics_rgb(self):
        """Provides the Intrinsic Matrix for the RGB Camera"""
        # construct the intrinsic matrix
        return np.array(
            [[self.focalLengthRGB[0,0], self.skewRGB,
                    self.principlePointRGB[0,0]],
             [0, self.focalLengthRGB[1,0], self.principlePointRGB[1,0]],
             [0, 0, 1]],
            dtype = np.float64
        )

    def extrinsics_depth(self):
        """Provides the Extrinsic Matrix for the Depth Camera"""
        # define rotation matrix from camera frame into the body frame
        transformFromCameraToBody = np.concatenate(
            (np.concatenate((self.orientationDepth, self.positionDepth),
                axis=1), [[0, 0, 0, 1]]),
            axis=0
        )

        return np.linalg.inv(transformFromCameraToBody)


    def intrinsics_depth(self):
        """Provides the Intrinsic Matrix for the Depth Camera"""
        # construct the intrinsic matrix
        return np.array(
            [[self.focalLengthDepth[0,0], self.skewDepth,
                self.principlePointDepth[0,0]],
             [0, self.focalLengthDepth[1,0], self.principlePointDepth[1,0]],
             [0, 0, 1]],
            dtype = np.float64
        )


    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.terminate()

class Camera2D():
    def __init__(
            self,
            cameraId="0",
            frameWidth=820,
            frameHeight=410,
            frameRate=30.0,
            focalLength=np.array([[None], [None]], dtype=np.float64),
            principlePoint=np.array([[None], [None]], dtype=np.float64),
            skew=None,
            position=np.array([[None], [None], [None]], dtype=np.float64),
            orientation=np.array(
                [[None,None,None], [None,None,None], [None,None,None]],
                dtype=np.float64),
            imageFormat = 0,
            brightness = None,
            contrast = None,
            gain = None,
            exposure = None,

        ):
        """Configures the 2D camera based on the cameraId provided.

        If you specify focal lengths, principle points, skew as well as
            camera position & orientation in the world/inertial frame,
            camera intrinsics/extrinsic matrices can also be extracted
            using corresponding methods in this class.

            image format defaults to 0. Outputs BGR images. If value is 1,
            will be set as greyscale.
        """
        self.url = "video://localhost:"+cameraId

        self.frameWidth = frameWidth
        self.frameHeight = frameHeight

        self.focalLength = 2*focalLength
        self.focalLength[0, 0] = -self.focalLength[0, 0]
        self.principlePoint = principlePoint
        self.skew = skew
        self.position = position
        self.orientation = orientation
        attributes = []

        if imageFormat == 0:
            self.imageFormat = ImageFormat.ROW_MAJOR_INTERLEAVED_BGR
            self.imageData = np.zeros((frameHeight, frameWidth, 3), dtype=np.uint8)
        else:
            self.imageFormat = ImageFormat.ROW_MAJOR_GREYSCALE
            self.imageData = np.zeros((frameHeight, frameWidth), dtype=np.uint8)

        if brightness is not None:
            attributes.append(VideoCaptureAttribute(VideoCapturePropertyCode.BRIGHTNESS, brightness, True))
        if contrast is not None:
            attributes.append(VideoCaptureAttribute(VideoCapturePropertyCode.CONTRAST, contrast, True))
        if gain:
            attributes.append(VideoCaptureAttribute(VideoCapturePropertyCode.GAIN, gain, True, False))
        if exposure is not None:
            attributes.append(VideoCaptureAttribute(VideoCapturePropertyCode.EXPOSURE, exposure, True, False))

        if not attributes:
            attributes = None
            numAttributes = 0
        else:
            numAttributes = len(attributes)


        try:
            self.capture = VideoCapture(
                self.url,
                frameRate,
                frameWidth,
                frameHeight,
                self.imageFormat,
                ImageDataType.UINT8,
                attributes,
                numAttributes
            )
            self.capture.start()
        except MediaError as me:
            print(me.get_error_message())

    def read(self):
        """Reads a frame, updating the corresponding image buffer. Returns a flag
        indicating whether the read was successful."""
        flag = False
        try:
            flag = self.capture.read(self.imageData)
        except MediaError as me:
            print(me.get_error_message())
        except KeyboardInterrupt:
            print('User Interrupted')
        finally:
            return flag

    def reset(self):
        """Resets the 2D camera stream by stopping and starting
            the capture service.
        """

        try:
            self.capture.stop()
            self.capture.start()
        except MediaError as me:
            print(me.get_error_message())

    def terminate(self):
        """Terminates the 2D camera operation. """
        try:
            self.capture.stop()
            self.capture.close()
        except MediaError as me:
            print(me.get_error_message())

    def extrinsics(self):
        """Provides the Extrinsic Matrix for the Camera"""
        # define rotation matrix from camera frame into the body frame
        transformFromCameraToBody = np.concatenate(
            (np.concatenate((self.orientation, self.position), axis=1),
                [[0, 0, 0, 1]]), axis=0)

        return np.linalg.inv(transformFromCameraToBody)

    def intrinsics(self):
        """Provides the Intrinsic Matrix for the Camera"""
        # construct the intrinsic matrix
        return np.array(
            [[self.focalLength[0,0], self.skew, self.principlePoint[0,0]],
             [0, self.focalLength[1,0], self.principlePoint[1,0]], [0, 0, 1]],
            dtype = np.float64
        )

    def __enter__(self):
        """Used for with statement."""
        return self

    def __exit__(self, type, value, traceback):
        """Used for with statement. Terminates the Camera"""
        self.terminate()

class Lidar():
    """A class for interacting with common LiDAR devices.

    This class provides an interface for working with LiDAR devices, such as
    RPLidar and Leishen MS10 or M10P. It simplifies the process of reading measurements
    and managing connections with these devices.

    Attributes:
        numMeasurements (int): The number of measurements per scan.
        distances (numpy.ndarray): An array containing distance measurements.
        angles (numpy.ndarray): An array containing the angle measurements.

    Example usage:

    .. code-block:: python

        from lidar import Lidar

        # Initialize a Lidar device (e.g. RPLidar)
        lidar_device = Lidar(type='RPLidar')

        # Read LiDAR measurements
        lidar_device.read()

        # Access measurement data
        print((lidar_device.distances, lidar_device.angles))

        # Terminate the LiDAR device connection
        lidar_device.terminate()

    """

    def __init__(
            self,
            type='RPLidar',
            numMeasurements=384,
            rangingDistanceMode=2,
            interpolationMode=0,
            interpolationMaxDistance=0,
            interpolationMaxAngle=0
        ):
        """Initialize a Lidar device with the specified configuration.

        Args:
            type (str, optional): The type of LiDAR device
                ('RPLidar' or 'LeishenMS10' or 'LeishenM10P'). Defaults to 'RPLidar'.
            numMeasurements (int, optional): The number of measurements
                per scan. Defaults to 384.
            rangingDistanceMode (int, optional): Ranging distance mode
                (0: Short, 1: Medium, 2: Long). Defaults to 2.
            interpolationMode (int, optional): Interpolation mode
                (0: Normal, 1: Interpolated). Defaults to 0.
            interpolationMaxDistance (float, optional): Maximum distance
                for interpolation. Defaults to 0.
            interpolationMaxAngle (float, optional): Maximum angle for
                interpolation. Defaults to 0.
        """

        self.numMeasurements = numMeasurements
        self.distances = np.zeros((numMeasurements,1), dtype=np.float32)
        self.angles = np.zeros((numMeasurements,1), dtype=np.float32)
        self._measurements = RangingMeasurements(numMeasurements)
        self._rangingDistanceMode = rangingDistanceMode
        self._interpolationMode = interpolationMode
        self._interpolationMaxDistance = interpolationMaxDistance
        self._interpolationMaxAngle = interpolationMaxAngle

        if type.lower() == 'rplidar':
            self.type = 'RPLidar'
            from quanser.devices import RPLIDAR as RPL
            self._lidar = RPL()
            if not hasattr(self, "url"):
                self.url = ("serial-cpu://localhost:2?baud='115200',"
                        "word='8',parity='none',stop='1',flow='none',dsr='on'")
            # Open the lidar device with ranging mode settings.
            self._lidar.open(self.url, self._rangingDistanceMode)

        elif type.lower() == 'leishenms10':
            self.type = 'LeishenMS10'
            from quanser.devices import LeishenMS10
            self._lidar = LeishenMS10()
            if not hasattr(self, "url"):
                self.url = ("serial-cpu://localhost:2?baud='460800',"
                        "word='8',parity='none',stop='1',flow='none'")
            self._lidar.open(self.url, samples_per_scan = self.numMeasurements)

        elif type.lower() == 'leishenm10p':
            self.type = 'LeishenM10P'
            from quanser.devices import LeishenM10P
            self._lidar = LeishenM10P()
            if not hasattr(self, "url"):
                self.url = ("serial://localhost:0?baud='512000',"
                        "word='8',parity='none',stop='1',flow='none',device='/dev/lidar'") #serial://localhost:0?device='/dev/lidar',baud='512000',word='8',parity='none',stop='1',flow='none'
            self._lidar.open(self.url, samples_per_scan = self.numMeasurements)

        else:
            # TODO: Assert error
            return

        try:
            # Ranging distance mode check
            if rangingDistanceMode == 2:
                self._rangingDistanceMode = RangingDistance.LONG
            elif rangingDistanceMode == 1:
                self._rangingDistanceMode = RangingDistance.MEDIUM
            elif rangingDistanceMode == 0:
                self._rangingDistanceMode = RangingDistance.SHORT
            else:
                print('Unsupported Ranging Distance Mode provided.'
                        'Configuring LiDAR in Long Range mode.')
                self._rangingDistanceMode = RangingDistance.LONG

            # Interpolation check (will be used in the read method)
            if interpolationMode == 0:
                self._interpolationMode = RangingMeasurementMode.NORMAL
            elif interpolationMode == 1:
                self._interpolationMode = RangingMeasurementMode.INTERPOLATED
                self._interpolationMaxAngle = interpolationMaxAngle
                self._interpolationMaxDistance = interpolationMaxDistance
            else:
                print('Unsupported Interpolation Mode provided.'
                        'Configuring LiDAR without interpolation.')
                self._interpolationMode = RangingMeasurementMode.NORMAL

        except DeviceError as de:
            if de.error_code == -34:
                pass
            else:
                print(de.get_error_message())

    def read(self):
        """Read a scan and store the measurements

        Read a scan from the LiDAR device and store the measurements in the
        'distances' and 'angles' attributes.
        """
        flag = False
        try:
            numValues = self._lidar.read(
                self._interpolationMode,
                self._interpolationMaxDistance,
                self._interpolationMaxAngle,
                self._measurements
            )
            if numValues > 0:
                self.distances = np.array(self._measurements.distance)
                self.angles = np.array(self._measurements.heading)
                flag = True
        except DeviceError as de:
            if de.error_code == -34:
                pass
            else:
                print(de.get_error_message())
        finally:
            return flag

    def terminate(self):
        """Terminate the LiDAR device connection correctly."""
        try:
            self._lidar.close()
            # print("lidar closed")
        except DeviceError as de:
            if de.error_code == -34:
                pass
            else:
                print(de.get_error_message())

    def __enter__(self):
        """Return self for use in a 'with' statement."""
        return self

    def __exit__(self, type, value, traceback):
        """
        Terminate the LiDAR device connection when exiting a 'with' statement.
        """
        self.terminate()

class Probe():
    '''Class object to send data to a remote Observer.
    Includes support for Displays (for video data), Plots (standard polar
    plot as an image) and Scope (standard time series plotter).'''

    def __init__(self,
                 ip = 'localhost'):

        self.remoteHostIP = ip
        self.agents = dict()
        self.agentType = []
        # agentType =>  0 Video Display
        #               1 Polar Plot
        #               2 Scope
        self.numDisplays = 0
        self.numPlots = 0
        self.numScopes = 0
        self.connected = False

    def add_display(self,
            imageSize = [480,640,3],
            scaling = True,
            scalingFactor = 2,
            name = 'display'
        ):

        self.numDisplays += 1
        _display = RemoteDisplay(ip = self.remoteHostIP,
            id = self.numDisplays,
            imageSize = imageSize,
            scaling = scaling,
            scalingFactor = scalingFactor
            )

        if name == 'display':
            name = 'display_'+str(self.numDisplays)
        # agent type => 0
        self.agents[name] = (_display, 0)

        return True

    def add_plot(self,
            numMeasurements = 1680,
            scaling = True,
            scalingFactor = 2,
            name = 'plot'
        ):
        self.numPlots += 1
        _plot = RemotePlot(ip = self.remoteHostIP,
                           numMeasurements=numMeasurements,
                           id=self.numPlots,
                           scaling = scaling,
                           scalingFactor = scalingFactor)

        if name == 'plot':
            name = 'plot_'+str(self.numDisplays)
        # agent type => 1
        self.agents[name] = (_plot, 1)

        return True

    def add_scope(self,
            numSignals = 1,
            name = 'scope'
        ):
        self.numScopes += 1

        _scope = RemoteScope(numSignals=numSignals, id=self.numScopes, ip=self.remoteHostIP)

        if name == 'scope':
            name = 'scope_'+str(self.numDisplays)
        # agent type => 2
        self.agents[name] = (_scope, 2)

        return True

    def check_connection(self):
        '''Attempts to connect every unconnected probe in the agentList.
        Returns True if every probe is successfully connected.'''
        self.connected = True

        for key in self.agents:
            if not self.agents[key][0].connected:
                self.agents[key][0].check_connection()
            self.connected = self.connected and self.agents[key][0].connected
        return self.connected

    def send(self, name,
             imageData=None,
             lidarData=None,
             scopeData=None):
        '''Ensure that at least one of imageData, lidarData, scopeData is provided,
        and that the type of data provided matches the expected name, otherwise an
        error message is printed and the method returns False.

        imageData => numpy array conforming to imageSize used in display definition \n
        lidarData => (ranges, angles) tuple, where ranges and angles are numpy arrays conforming to numMeasurements used in plot definition \n
        scopeData => (time, data) tuple, with data being a numpy array conforming to numSignals used in scope definition and time is the timestamp \n
        '''

        flag = False
        agentType = self.agents[name][1]
        if agentType == 0:
            if imageData is None:
                print("Image data not provided for a display agent.")
            else:
                flag = self.agents[name][0].send(imageData)
        elif agentType == 1:
            if lidarData is None:
                print("Lidar data not provided for a plot agent.")
            else:
                flag = self.agents[name][0].send(distances=lidarData[0], angles=lidarData[1])
        elif agentType == 2:
            if scopeData is None:
                print("Scope data not provided for a scope agent")
            else:
                flag = self.agents[name][0].send(scopeData[0], data=scopeData[1])

        return flag

    def terminate(self):
        for key in self.agents:
            self.agents[key][0].terminate()

class RemoteDisplay: # works as a client
    '''Class object to send camera feed to a device. Works as a client.'''
    def __init__(
            self,
            ip = 'localhost',
            id = 0,
            imageSize = [480,640,3],
            scaling = True,
            scalingFactor = 2
        ):

        '''
        ip - IP address of the device receiving the data as a string, eg. '192.168.2.4' \n
        id - unique identifier for sending and receiving data. Needs to match the ID in the receiveCamera object. \n
        imageSize - list defining image size. eg. [height, width, # of channels] \n
        scaling - Boolean describing if image will be scaled when sending data. This will decrease its size by the factor in scalingFactor.Default is True \n
        scalingFactor - Factor by which the image will be decreased by. Default is 2. If original image is 480x640, sent image will be 240x320\n
         \n
        Consideration: values for id, imageSize, scaling and scalingFactor need to be the same on the SendCamera and ReceiveCamera objects.
        '''
        if scaling and scalingFactor < 1:
            scalingFactor == 1

        if (scaling and
            (imageSize[0] % scalingFactor != 0 or
            imageSize[1] % scalingFactor != 0)):
            sys.exit('Select a scaling factor that is a factor of both width and height of image')

        if scaling:
            imageSize[0] = int(imageSize[0]/scalingFactor)
            imageSize[1] = int(imageSize[1]/scalingFactor)
            self.newSize = (imageSize[1], imageSize[0])

        bufferSize = np.prod(imageSize)
        # if scaling:
        #     print('Remote Display will stream an image of dimension', self.newSize, 'for', bufferSize, 'bytes.')
        # else:
        #     print('Remote Display will stream an image of dimension', imageSize, 'for', bufferSize, 'bytes.')

        id = np.clip(id,0,80)
        port = 18800+id
        uriAddress  = 'tcpip://' + str(ip) + ':' + str(port)

        self.client = BasicStream(uriAddress, agent='C',
                                  sendBufferSize=bufferSize,
                                  nonBlocking=True)
        self.scaling = scaling
        self.scalingFactor = scalingFactor
        self.connected = self.client.connected

        self.timeout = Timeout(seconds=0, nanoseconds=10000000)

    def check_connection(self):
        '''Checks if the sendCamera object is connected to its server. returns True or False.'''
        # First check if the server was connected.
        self.client.checkConnection(timeout=self.timeout)
        self.connected = self.client.connected

    def send(self,image):
        '''Resizes the image if needed and sends the image added as the input.
         \n
        image - image to send, needs to match imageSize defined while initializing the object'''
        if self.client.connected:
            # add some sort of compression
            if self.scaling:
                image2 = cv2.resize(image, self.newSize)

                sent = self.client.send(image2)
            else:
                sent = self.client.send(image)
            if sent == -1:
                return False
            else:
                return True

    def terminate(self):
        '''Terminates the connection.'''
        self.client.terminate()

class RemotePlot: # works as a client

    def __init__(
            self,
            ip = 'localhost',
            id = 1,
            numMeasurements = 1680,
            scaling = True,
            scalingFactor = 4
        ):
        self.scalingFactor = scalingFactor
        self.scaling = scaling
        self.numMeasurements = numMeasurements
        if scaling:
            self.numMeasurements = int(numMeasurements/self.scalingFactor)
        bufferSize = self.numMeasurements * 2 * 4 # 4 bytes per float and 2 for distances + angles
        port = 18600+id
        uriAddress  = 'tcpip://' + ip + ':'+ str(port)
        self.client = BasicStream(uriAddress, agent='C',
                                  sendBufferSize=bufferSize,
                                  nonBlocking=True)
        self.connected = self.client.connected
        self.timeout = Timeout(seconds=0, nanoseconds=1)

    def check_connection(self):
        '''Checks if the sendCamera object is connected to its server. returns True or False.'''
        # First check if the server was connected.
        self.client.checkConnection(timeout=self.timeout)
        self.connected = self.client.connected

    def send(self, distances = None, angles = None):
        if distances is None or angles is None:
            return False

        if self.client.connected:
            if self.scaling:
                data = np.concatenate((np.reshape(distances[0:-1:self.scalingFactor], (-1, 1)), np.reshape(angles[0:-1:self.scalingFactor], (-1, 1))), axis=1)
            else:
                data = np.concatenate((np.reshape(distances, (-1, 1)), np.reshape(angles, (-1, 1))), axis=1)
            result = self.client.send(data)
            if result == -1:
                return False
            else:
                return True

    def terminate(self):
        '''Terminates the connection.'''
        self.client.terminate()

class RemoteScope():
    def __init__(
            self,
            numSignals = 1,
            id = 1,
            ip = 'localhost'
        ):

        self.numMeasurements = numSignals
        bufferSize = (self.numMeasurements+1) * 8 # 8 bytes per double
        port = 18700+id
        uriAddress  = 'tcpip://' + ip + ':'+ str(port)
        self.client = BasicStream(uriAddress, agent='C',
                                  sendBufferSize=bufferSize,
                                  nonBlocking=True)
        self.connected = self.client.connected
        self.timeout = Timeout(seconds=0, nanoseconds=1000000)

    def check_connection(self):
        '''Checks if the sendCamera object is connected to its server. returns True or False.'''
        # First check if the server was connected.
        self.client.checkConnection(timeout=self.timeout)
        self.connected = self.client.connected

    def send(self, time, data = None):
        if data is None:
            return False

        if self.client.connected:
            timestamp = np.array([time], dtype=np.float64)
            flag = self.client.send(np.concatenate((timestamp, data)))
            if flag == -1:
                return False
            else:
                return True

    def terminate(self):
        '''Terminates the connection.'''
        self.client.terminate()

IS_PHYSICAL_QBOTPLATFORM = (('nvidia' == os.getlogin())
                            and ('aarch64' == platform.machine()))
"""A boolean constant indicating if the current device is a physical QBot
Platform.

This constant is set to True if both the following conditions are met:
1. The current user's login name is 'nvidia'.
2. The underlying system's hardware architecture is 'aarch64'.

It's intended to be used for configuring execution as needed depending on if
the executing platform is a physical and virtual QBot Platform.
"""

class QBotPlatformDriver():
    """Driver class for performing basic QBot Platform IO

    Args:
            mode (int, optional): Determines the driver mode. Defaults to 1.
                1 & 2 are designed for education, 3 & 4 are designed for
                research. 1 and 3 are body mode, 2 and 4 are wheeled mode.
            ip (str): IP address of the QBot Platform.
    """

    def __init__(self, mode=1, ip='192.168.2.15') -> None:

        # QBot reads
        self.wheelPositions = np.zeros((2), dtype = np.float64)
        self.wheelSpeeds    = np.zeros((2), dtype = np.float64)
        self.motorCmd       = np.zeros((2), dtype = np.float64)
        self.accelerometer  = np.zeros((3), dtype = np.float64)
        self.gyroscope      = np.zeros((3), dtype = np.float64)
        self.currents       = np.zeros((2), dtype = np.float64)
        self.battVoltage    = np.zeros((1), dtype = np.float64)
        self.watchdog       = np.zeros((1), dtype = np.float64)

        # QBot Platform Driver listening on port 18888
        self.uri = 'tcpip://'+ip+':18888'

        # 1 ms timeout parameter
        self._timeout = Timeout(seconds=0, nanoseconds=1000000)

        # establish stream object to communicate with QBot Platform Driver
        self._handle = BasicStream(uri=self.uri,
                                    agent='C',
                                    receiveBuffer=np.zeros((17),
                                                           dtype=np.float64),
                                    sendBufferSize=2048,
                                    recvBufferSize=2048,
                                    nonBlocking=True)

        # Only set mode on initialization, this value is not set in read-write
        self._sendPacket = np.zeros((10), dtype=np.float64)
        self._sendPacket[0] = mode
        self._mode = mode

        # if connected to the Driver, proceed, else, try to connect.
        # self.status_check('Connected to QBot Platform Driver.', iterations=20)
        self.status_check('', iterations=20)
        # there is no return here.

    def status_check(self, message, iterations=10):
        # blocking method to establish connection to the server stream.
        self._timeout = Timeout(seconds=0, nanoseconds=1000) #1000000
        counter = 0
        while not self._handle.connected:
            self._handle.checkConnection(timeout=self._timeout)
            counter += 1
            if self._handle.connected:
                print(message)
                break
            elif counter >= iterations:
                print('Driver error: status check failed.')
                break

            # once you connect, self._handle.connected goes True, and you
            # leave this loop.

    def read_write_std(self,
                       timestamp,
                       arm = 1,
                       commands=np.zeros((2), dtype=np.float64),
                       userLED=False,
                       color=[1, 0, 1],
                       hold = 0):

        # data received flag
        new = False

        # 1 us timeout parameter
        self._timeout = Timeout(seconds=0, nanoseconds=10000000)

        # set User LED color values if desired
        if userLED:
            self._sendPacket[1] = 1.0 # User LED packet
            self._sendPacket[2:5] = np.array([color[0], color[1], color[2]])
        else:
            self._sendPacket[1] = 0.0 # User LED packet
            self._sendPacket[2:5] = np.array([0, 0, 0])

        # set remaining packet to send
        self._sendPacket[5] = arm
        self._sendPacket[6] = hold
        self._sendPacket[7] = commands[0]
        self._sendPacket[8] = commands[1]
        self._sendPacket[9] = timestamp

        # if connected to driver, send/receive
        if self._handle.connected:
            self._handle.send(self._sendPacket)
            new, bytesReceived = self._handle.receive(timeout=self._timeout, iterations=5)
            # print(new, bytesReceived)
            # if new is True, full packet was received
            if new:
                self.wheelPositions = self._handle.receiveBuffer[0:2]
                self.wheelSpeeds = self._handle.receiveBuffer[2:4]
                self.motorCmd = self._handle.receiveBuffer[4:6]
                self.accelerometer = self._handle.receiveBuffer[6:9]
                self.gyroscope = self._handle.receiveBuffer[9:12]
                self.currents = self._handle.receiveBuffer[12:14]
                self.battVoltage = self._handle.receiveBuffer[14]
                self.watchdog = self._handle.receiveBuffer[15]
                self.timeStampRecv = self._handle.receiveBuffer[16]

        else:
            self.status_check('Reconnected to QBot Platform Driver.')

        # if new is False, data is stale, else all is good
        return new

    def terminate(self):
        self._handle.terminate()

class QBotPlatformLidar(Lidar):
    """
    QBotPlatfromLidar class represents the LIDAR sensor on the QBot Platform.

    Inherits from Lidar class in pal.utilities.lidar

    Args:
        numMeasurements (int): The number of LIDAR measurements.
        interpolationMode (int): The interpolation mode.
        interpolationMaxDistance (int): The maximum interpolation distance.
        interpolationMaxAngle (int): The maximum interpolation angle.
    """

    # Initializes a new instance of the QBotPlatformLidar class.

    def __init__(
        self,
        numMeasurements=1680,
        interpolationMode=0,
        interpolationMaxDistance=0,
        interpolationMaxAngle=0
        ):

        if IS_PHYSICAL_QBOTPLATFORM:
            self.url = ("serial://localhost:0?baud='512000',"
                        "word='8',parity='none',stop='1',flow='none',device='/dev/lidar'")
        else:
            self.url = "tcpip://localhost:18918"

        super().__init__(
            type='leishenm10p',
            numMeasurements=numMeasurements,
            interpolationMode=interpolationMode,
            interpolationMaxDistance=interpolationMaxDistance,
            interpolationMaxAngle=interpolationMaxAngle
        )

class QBotPlatformRealSense(Camera3D):
    """
    A class for accessing 3D camera data from the RealSense camera on the QBot
    Platform.

    Inherits from Camera3D class in pal.utilities.vision

    Args:
        mode (str): Mode to use for capturing data. Default is 'RGB&DEPTH'.
        frameWidthRGB (int): Width of the RGB frame. Default is 640.
        frameHeightRGB (int): Height of the RGB frame. Default is 400.
        frameRateRGB (int): Frame rate of the RGB camera. Default is 30.
        frameWidthDepth (int): Width of the depth frame. Default is 640.
        frameHeightDepth (int): Height of the depth frame. Default is 400.
        frameRateDepth (int): Frame rate of the depth camera. Default is 15.
        frameWidthIR (int): Width of the infrared (IR) frame. Default is 640.
        frameHeightIR (int): The height of the IR frame. Default is 400.
        frameRateIR (int): Frame rate of the IR camera. Default is 15.
        readMode (int): Mode to use for reading data from the camera.
            Default is 1.
        focalLengthRGB (numpy.ndarray): RGB camera focal length in pixels.
            Default is np.array([[None], [None]], dtype=np.float64).
        principlePointRGB (numpy.ndarray): Principle point of the RGB camera
            in pixels. Default is np.array([[None], [None]], dtype=np.float64).
        skewRGB (float): Skew factor for the RGB camera. Default is None.
        positionRGB (numpy.ndarray): An array of shape (3, 1) that holds the
            position of the RGB camera in the QBot's frame of reference.
        orientationRGB (numpy.ndarray): An array of shape (3, 3) that holds the
            orientation of the RGB camera in the QBot's frame of reference.
        focalLengthDepth (numpy.ndarray): An array of shape (2, 1) that holds
            the focal length of the depth camera.
        principlePointDepth (numpy.ndarray): An array of shape (2, 1) that
            holds the principle point of the depth camera.
        skewDepth (float, optional): Skew of the depth camera
        positionDepth (numpy.ndarray, optional): An array of shape (3, 1) that
            holds the position of the depth camera
        orientationDepth (numpy.ndarray): An array of shape (3, 3) that holds
            the orientation of the Depth camera in the QBot's reference frame.
    """
    def __init__(
            self,
            mode='RGB&DEPTH',
            frameWidthRGB=640,
            frameHeightRGB=480,
            frameRateRGB=30.0,
            frameWidthDepth=640,
            frameHeightDepth=480,
            frameRateDepth=30.0,
            frameWidthIR=640,
            frameHeightIR=480,
            frameRateIR=30.0,
            readMode=0,
            focalLengthRGB=np.array([[None], [None]], dtype=np.float64),
            principlePointRGB=np.array([[None], [None]], dtype=np.float64),
            skewRGB=None,
            positionRGB=np.array([[None], [None], [None]], dtype=np.float64),
            orientationRGB=np.array([[None, None, None], [None, None, None],
                                     [None, None, None]], dtype=np.float64),
            focalLengthDepth=np.array([[None], [None]], dtype=np.float64),
            principlePointDepth=np.array([[None], [None]], dtype=np.float64),
            skewDepth=None,
            positionDepth=np.array([[None], [None], [None]], dtype=np.float64),
            orientationDepth=np.array([[None, None, None], [None, None, None],
                                       [None, None, None]], dtype=np.float64)
        ):

        if IS_PHYSICAL_QBOTPLATFORM:
            deviceId = '0'
        else:
            deviceId = "0@tcpip://localhost:18917"
            frameWidthRGB = 640
            frameHeightRGB = 480
            frameRateRGB = 30
            frameWidthDepth = 640
            frameHeightDepth = 480
            frameRateDepth = 30
            frameWidthIR = 640
            frameHeightIR = 480
            frameRateIR = 30

        super().__init__(
            mode,
            frameWidthRGB,
            frameHeightRGB,
            frameRateRGB,
            frameWidthDepth,
            frameHeightDepth,
            frameRateDepth,
            frameWidthIR,
            frameHeightIR,
            frameRateIR,
            deviceId,
            readMode,
            focalLengthRGB,
            principlePointRGB,
            skewRGB,
            positionRGB,
            orientationRGB,
            focalLengthDepth,
            principlePointDepth,
            skewDepth,
            positionDepth,
            orientationDepth
        )

class QBotPlatformCSICamera(Camera2D):

    """Class for accessing the QBot Platform CSI camera.

    Args:
        frameWidth (int, optional): Width of the camera frame.
            Defaults to 640.
        frameHeight (int, optional): Height of the camera frame.
            Defaults to 400.
        frameRate (int, optional): Frame rate of the camera.
            Defaults to 30.

    """

    def __init__(

            self,
            frameWidth=640,
            frameHeight=400,
            frameRate=60.0,
            focalLength=np.array([[None], [None]], dtype=np.float64),
            principlePoint=np.array([[None], [None]], dtype=np.float64),
            skew=None,
            position=np.array([[None], [None], [None]], dtype=np.float64),
            orientation=np.array(
                [[None,None,None], [None,None,None], [None,None,None]],
                dtype=np.float64),
            brightness = None, #won't work on qbot platform downward facing
            contrast = None, #won't work on qbot platform downward facing
            gain = None,
            exposure = None
        ):

        if IS_PHYSICAL_QBOTPLATFORM:
            deviceId = '0'
        else:
            deviceId = "0@tcpip://localhost:18915"
            frameRate = 30.0
        super().__init__(
            cameraId=deviceId,
            frameWidth=frameWidth,
            frameHeight=frameHeight,
            frameRate=frameRate,
            focalLength = focalLength,
            principlePoint = principlePoint,
            skew = skew,
            position=position,
            orientation=orientation,
            imageFormat=1,
            brightness = brightness,
            contrast = contrast,
            gain = gain,
            exposure = exposure
        )

# Section A - Setup
os.system('quarc_run -q -Q -t tcpip://localhost:17000 *.rt-linux_qbot_platform -d /tmp')
time.sleep(5)
os.system('quarc_run -r -t tcpip://localhost:17000 qbot_platform_driver_physical.rt-linux_qbot_platform  -d /tmp -uri tcpip://localhost:17099')
time.sleep(3)
print('Driver deployed')

ipHost, ipDriver = '192.168.3.6', 'localhost'
commands, arm, noKill = np.zeros((2), dtype = np.float64), 0, True
frameRate, sampleRate = 60.0, 1/60.0
endFlag, counter, counterRS, counterDown, counterLidar = False, 0, 0, 0, 0
simulationTime = 90.0
startTime = time.time()
def elapsed_time():
    return time.time() - startTime
timeHIL, prevTimeHIL = elapsed_time(), elapsed_time() - 0.017

try:
    # Section B - Initialization
    myQBot       = QBotPlatformDriver(mode=1, ip=ipDriver)
    downCam      = QBotPlatformCSICamera(exposure = 10)
    realSenseCam = QBotPlatformRealSense()
    lidar        = QBotPlatformLidar()
    gpad         = LogitechF710(1)

    # Section C - Initialization to send data to main computer
    probe        = Probe(ip = ipHost)
    probe.add_display(imageSize = [400, 640, 1], scaling = True,
                      scalingFactor= 2, name="Downward Camera Image")
    probe.add_display(imageSize = [480, 640, 3], scaling = True,
                      scalingFactor= 2, name="RealSense RGB Image")
    probe.add_display(imageSize = [480, 640, 1], scaling = True,
                      scalingFactor= 2, name="RealSense Depth Image")
    probe.add_plot(numMeasurements=1680, scaling=True,
                      scalingFactor= 8, name='Leishen Lidar')
    startTime = time.time()
    time.sleep(0.5)
    print('Connecting to Observer')
    
    # Main loop
    while noKill and not endFlag:
        t = elapsed_time()
        
        if not probe.connected:
            probe.check_connection()

        if probe.connected:
            os.system('clear')    
            print('Connected to Observer')
            # Section D - Send and Receive Data
            # QBot Hardware
            newHIL = myQBot.read_write_std(timestamp = time.time() - startTime,
                                            arm = arm,
                                            commands = commands)
            if newHIL:
                timeHIL = time.time()

                # Downward camera, RealSense camera & Lidar acquisition
                newDownCam = downCam.read()
                newRealSenseDepth = realSenseCam.read_depth(dataMode='M')
                newRealSenseRGB = realSenseCam.read_RGB()
                newLidar = lidar.read()

                # Section E - Sending data to Observer in main computer
                # Remote probe
                if newDownCam: counterDown += 1
                if newRealSenseDepth or newRealSenseRGB: counterRS += 1
                if newLidar: counterLidar += 1
                if counterDown%4 == 0:
                    sending = probe.send(name="Downward Camera Image",
                                         imageData=downCam.imageData)
                if counterRS%4 == 2:
                    sending = probe.send(name="RealSense Depth Image",
                                         imageData=cv2.convertScaleAbs(realSenseCam.imageBufferDepthM, alpha=(255.0/3.0)))
                elif counterRS%4 == 0:
                    sending = probe.send(name="RealSense RGB Image",
                                         imageData=realSenseCam.imageBufferRGB)
                if counterLidar%6 == 0:
                    sending = probe.send(name="Leishen Lidar",
                                         lidarData=(lidar.distances, (np.pi/2 - lidar.angles)) )
                prevTimeHIL = timeHIL

            # End condition
            endFlag = t > simulationTime
            if endFlag:
                print("Application completed successfully")

            # Section F - Joystick to commands
            # Joystick Driver
            new = gpad.read()
            if new:
                turnSpd = 3.564*gpad.leftJoystickX/2
                forSpd = 0.7*gpad.rightJoystickY/2
                arm = gpad.buttonLeft
                commands = np.array([forSpd, turnSpd], dtype = np.float64)
                if gpad.buttonRight:
                    print("Operator: Emergency Stop")
                    noKill = False

except KeyboardInterrupt:
    print('User interrupted.')

finally:
    # Termination
    downCam.terminate()
    myQBot.terminate()
    realSenseCam.terminate()
    lidar.terminate()
    probe.terminate()
