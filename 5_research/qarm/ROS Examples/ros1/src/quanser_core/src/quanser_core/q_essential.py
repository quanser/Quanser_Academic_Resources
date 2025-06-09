from quanser.hardware import HIL, HILError, PWMMode
from quanser.multimedia import Video3D, VideoCapture, Video3DStreamType, MediaError, ImageFormat, ImageDataType
from quanser.devices import RPLIDAR, RangingMeasurements, RangingMeasurementMode, DeviceError, RangingDistance
from .q_misc import Utilities
import numpy as np
import pygame
import time

saturate = Utilities.saturate

# region: Cameras

class Camera3D():
    def __init__(self, mode='RGB&DEPTH', frame_width_RGB=1920, frame_height_RGB=1080, frame_rate_RGB=30.0, frame_width_depth=1280, frame_height_depth=720, frame_rate_depth=15.0, device_id='0'):
        '''This function configures the Intel Realsense RGB and depth cameras for use.
        
        Outputs:
        video3d - video3d object, you must call video3d.start_streaming() before your main loop
        stream_RGB - stream object to be passed to the read method
        image_buffer_RGB - buffer array that will be updated by the read method
        stream_depth - stream object to be passed to the read method
        image_buffer_depth - buffer array that will be updated by the read method'''
        self.mode = mode
        self.stream_index = 0
        self.image_buffer_RGB = np.zeros((frame_height_RGB, frame_width_RGB, 3), dtype=np.uint8)
        self.image_buffer_depth_px = np.zeros((frame_height_depth, frame_width_depth, 1), dtype=np.uint8)
        self.image_buffer_depth_m = np.zeros((frame_height_depth, frame_width_depth, 1), dtype=np.float32)
        try:
            self.video3d = Video3D(device_id)
            if mode == 'RGB':
                self.stream_RGB = self.video3d.stream_open(Video3DStreamType.COLOR, self.stream_index, frame_rate_RGB, frame_width_RGB, frame_height_RGB, ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8)
            elif mode == 'DEPTH':
                self.stream_depth = self.video3d.stream_open(Video3DStreamType.DEPTH, self.stream_index, frame_rate_depth, frame_width_depth, frame_height_depth, ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)        
            else:
                self.stream_RGB = self.video3d.stream_open(Video3DStreamType.COLOR, self.stream_index, frame_rate_RGB, frame_width_RGB, frame_height_RGB, ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8)
                self.stream_depth = self.video3d.stream_open(Video3DStreamType.DEPTH, self.stream_index, frame_rate_depth, frame_width_depth, frame_height_depth, ImageFormat.ROW_MAJOR_GREYSCALE, ImageDataType.UINT8)
            self.video3d.start_streaming()                
        except MediaError as me:
            print(me.get_error_message())
            
    def terminate(self):
        '''This function terminates the RGB and depth video and stream objects correctly.
        
        Inputs:
        video3d - video object from the configure method
        stream_RGB - RGB stream object from the configure method
        stream_depth - depth stream object from the configure method '''

        try:
            self.video3d.stop_streaming()
            if self.mode == 'RGB':
                self.stream_RGB.close()
            elif self.mode == 'DEPTH':
                self.stream_depth.close()
            else:
                self.stream_RGB.close()
                self.stream_depth.close()

            self.video3d.close()

        except MediaError as me:
            print(me.get_error_message())
    
    def read_RGB(self):
        '''This function reads an image from the RGB camera for use.
        
        Outputs:
        timestamp - timestamp corresponding to the frame read '''
        timestamp = -1
        try:
            frame = self.stream_RGB.get_frame()
            while not frame:
                frame = self.stream_RGB.get_frame() 
            frame.get_data(self.image_buffer_RGB)
            timestamp = frame.get_timestamp()
            frame.release()
        except KeyboardInterrupt:
            pass
        except MediaError as me:
            print(me.get_error_message())
        finally:
            return timestamp

    def read_depth(self, dataMode='px'):
        '''This function reads an image from the depth camera for use.
        dataMode is 'px' for pixels or 'm' for meters. Use corresponding image buffer.
        
        Outputs:
        timestamp - timestamp corresponding to the frame read '''
        timestamp = -1
        try:
            frame = self.stream_depth.get_frame()
            while not frame:
                frame = self.stream_depth.get_frame()
            if dataMode == 'px':
                frame.get_data(self.image_buffer_depth_px)
            elif dataMode == 'm':
                frame.get_meters(self.image_buffer_depth_m)
            timestamp = frame.get_timestamp()
            frame.release()
        except KeyboardInterrupt:
            pass
        except MediaError as me:
            print(me.get_error_message())
        finally:
            return timestamp

class Camera2D():
    def __init__(self, camera_id="0", frame_width=640, frame_height=480, frame_rate=30.0):
        '''This function configures the 2D camera for use based on the camera_id provided.'''

        self.url = "video://localhost:"+camera_id
        self.image_data = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

        try:
            self.capture = VideoCapture(self.url, frame_rate, frame_width, frame_height, ImageFormat.ROW_MAJOR_INTERLEAVED_BGR, ImageDataType.UINT8, self.image_data, None, 0)
            self.capture.start()
        except MediaError as me:
            print(me.get_error_message())
        
    def read(self):
        '''This function reads a frame, updating the corresponding image buffer.'''
        try:
            self.capture.read()
        except MediaError as me:
            print(me.get_error_message())
        except KeyboardInterrupt:
            print('User Interupted')

    def reset(self):
        '''This function resets the 2D camera stream by stopping and starting the capture service.'''

        try:
            self.capture.stop()
            self.capture.start()
        except MediaError as me:
            print(me.get_error_message())

    def terminate(self):
        '''This function terminates the 2D camera operation.'''
        try:
            self.capture.stop()
            self.capture.close()
        except MediaError as me:
            print(me.get_error_message())

# endregion


# region: LIDAR

class LIDAR():
    def __init__(self, num_measurements=720, max_distance=10.0):
        self.num_measurements = num_measurements
        # self.measurements = [RangingMeasurement() for x in range(self.num_measurements)]
        self.measurements = RangingMeasurements(num_measurements)
        self.distances = np.zeros((num_measurements,1), dtype=np.float64)
        self.angles = np.linspace(0, 2*np.pi-(2*np.pi/num_measurements), num_measurements, dtype=np.float64)
        self.lidar = RPLIDAR()
        self.maxDistance = max_distance
        try:
            self.lidar.open("serial-cpu://localhost:2?baud='115200',word='8',parity='none',stop='1',flow='none',dsr='on'", RangingDistance.SHORT)
        except DeviceError as de:
            if de.error_code == -34:
                pass
            else:
                print(de.get_error_message())

    def terminate(self):
        try:
            self.lidar.close()
        except DeviceError as de:
            if de.error_code == -34:
                pass
            else:
                print(de.get_error_message())

    def read(self):
        try:
            self.lidar.read(RangingMeasurementMode.INTERPOLATED, 0.05, self.measurements)
            self.distances = np.array(self.measurements.distance)
            self.distances = np.append(  np.flip( self.distances[0:int(self.num_measurements/4)] ) , 
                                         np.flip( self.distances[int(self.num_measurements/4):]) )
            self.distances[self.distances > self.maxDistance] = self.maxDistance
            # self.angles = np.array(self.measurements.heading)
            
        except DeviceError as de:
            if de.error_code == -34:
                pass
            else:
                print(de.get_error_message())

# endregion