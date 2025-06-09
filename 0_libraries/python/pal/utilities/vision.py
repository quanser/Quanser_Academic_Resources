"""vision.py: A module for simplifying interaction with various camera types.

This module provides a set of classes designed to make it easier to interface
with different types of cameras, such as standard 2D cameras, depth cameras,
or stereo cameras. The classes include functionality for connecting to cameras,
reading image data, and performing necessary conversions or transformations.
"""
import numpy as np

from quanser.multimedia import Video3D, Video3DStreamType, VideoCapture, \
    MediaError, ImageFormat, ImageDataType, VideoCapturePropertyCode, \
    VideoCaptureAttribute


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
            dtype=np.uint8
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
                    ImageDataType.UINT8
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
