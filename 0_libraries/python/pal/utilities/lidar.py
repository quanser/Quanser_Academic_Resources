"""lidar: A module for simplifying interactions with common LiDAR devices.

This module provides a Lidar class to facilitate working with common LiDAR
devices, such as RPLidar and Leishen M10. It is designed to make it easy to
interface with these devices, read their measurements, and manage their
connections.
"""
import numpy as np
from quanser.devices import (
    RangingMeasurements,
    RangingMeasurementMode,
    DeviceError,
    RangingDistance
)

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