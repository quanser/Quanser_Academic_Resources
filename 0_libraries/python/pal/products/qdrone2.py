"""qdrone 2: Classes to simplify interactions with the QDrone 2.

This module provides a set of API classes and tools to facilitate working with
the QDrone 2. It is designed to make it easy to set up and read
data from various QDrone 2 sensors and its perception stack.

"""
import numpy as np
from quanser.common import Timeout
from pal.utilities.stream import BasicStream


class QDrone2StreamStack():
    """Stream class for capturing flight data from the QDrone 2 (HW or Virtual)

    Args:
            ip (str): IP address of the QDrone 2.
    """

    def __init__(self, ip='192.168.2.15') -> None:

        # QDrone2 reads
        self.imu_0_raw      = np.zeros((6), dtype = np.float64)
        self.imu_1_raw      = np.zeros((6), dtype = np.float64)
        self.state_vec_0    = np.zeros((9), dtype = np.float64)
        self.state_vec_1    = np.zeros((9), dtype = np.float64)
        self.state_vec      = np.zeros((9), dtype = np.float64)
        self.motorCurrent   = np.zeros((1), dtype = np.float64)
        self.motorCmd       = np.zeros((4), dtype = np.float64)
        self.battVoltage    = np.zeros((1), dtype = np.float64)
        self.lowBattery     = np.zeros((1), dtype = np.float64)
        self.timestampREC   = np.zeros((1), dtype = np.float64)

        # QDrone2 Dronestack URI for reading state data
        self.uri = 'tcpip://'+ip+':18491'

        # 1 ms timeout parameter
        self._timeout = Timeout(seconds=0, nanoseconds=1000000)

        # establish stream object to communicate with QBot Platform Driver
        self._handle = BasicStream(uri=self.uri,
                                    agent='C',
                                    receiveBuffer=np.zeros((47),
                                                        dtype=np.float64),
                                    sendBufferSize=2048,
                                    recvBufferSize=2048,
                                    nonBlocking=True)

        # initialize timestamp packet to send
        self._sendPacket = np.zeros((1), dtype = np.float64)

        # if connected to the Stream Server, proceed, else, try to connect.
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
                print('Stream Stack: status check failed.')
                break

            # once you connect, self._handle.connected goes True, and you
            # leave this loop.

    def read(self, timestamp):

        # data received flag
        new = False

        # 1 us timeout parameter
        self._timeout = Timeout(seconds=0, nanoseconds=10000000)

        # set User LED color values if desired
        self._sendPacket[0] = timestamp

        # if connected to driver, send/receive
        if self._handle.connected:
            self._handle.send(self._sendPacket)
            new, bytesReceived = self._handle.receive(timeout=self._timeout, iterations=5)

            # if new is True, full packet was received
            if new:
                self.imu_0_raw      = self._handle.receiveBuffer[0:6]
                self.imu_1_raw      = self._handle.receiveBuffer[6:12]
                self.state_vec_0    = self._handle.receiveBuffer[12:21]
                self.state_vec_1    = self._handle.receiveBuffer[21:30]
                self.state_vec      = self._handle.receiveBuffer[30:39]
                self.motorCurrent   = self._handle.receiveBuffer[39]
                self.motorCmd       = self._handle.receiveBuffer[40:44]
                self.battVoltage    = self._handle.receiveBuffer[44]
                self.lowBattery     = self._handle.receiveBuffer[45]
                self.timestampREC   = self._handle.receiveBuffer[46]

        else:
            self.status_check('Reconnected to Stream Stack.')

        # if new is False, data is stale, else all is good
        return new

    def terminate(self):
        self._handle.terminate()