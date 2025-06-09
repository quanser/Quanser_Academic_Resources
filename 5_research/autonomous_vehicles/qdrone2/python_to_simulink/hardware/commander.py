from pal.utilities.stream import BasicStream
import numpy as np
import time as t
import keyboard


class JoystickCommands:
    '''
    This class is used to send commands to, and recveive data from a \n
    mission server for QDrone2. The data sent is an array consisting of \n
    joystick commands.

    '''
    def __init__(self, uri, recBuff=np.zeros((5, 1), dtype=np.float64), recBuffSize=40*2):
        '''
        Initialize CommandMission object
        \n
        Params:\n
            _received_flag      -   int, check if data is received, 0 if False, 1 if True \n

            _bytes_received     -   int, no of bytes received \n

            uri                 -   string, unique resource identifier in the form "tcpip://ipaddress:port" \n

            recBuff             -   a 5x1 numpy array buffer to hold the received data [Arm, Takeoff, Estop, JoystickIssue, IsTracking]  \n

            recBuffSize         -   Expected data size times 2 ie. 5 * 8 bytes multiplied by 2 \n

            armed               -   int, 0 if not armed, 1 if armed\n

            takenoff            -   int, 0 if drone has not taken off, 1 if drone has taken off\n

            Estop               -   int, 0 if Emergency stop command not issued, 1 if Emergency stop command issued \n

            joystickIssue       -   int, emulates the joystick issue flag, 1 if there is a communication issue and 0 if not.\n

            mode                -   int, determines the flight mode. 0 by default and for hover only. Set to 1 \n
                                    to enable the sending of trajectories/waypoints.\n

            IsTracking          -   int, 1 if virtual pose data is not being sent to Mission server or 0 if not \n

            connected           -   int, 1 if connection has been established with Mission server or 0 if not\n

            commander           -   Stream, a stream object that makes connection with the mission server model \n
                                    See BasicStream() for details.\n

            joystick_commands   -   numpy array, Emulates joystick commands as an array of the form \n
                                    [arm, take_off, Estop, Joystick Issue, mode]\n

        Usage:
            >>> myQdrone = JoystickCommands(uri="tcpip://192.168.0.1:14001")
            >>> while True:
            >>>     if not myQdrone.connected:
            >>>         myQdrone.check_connection()
            >>>     else:
            >>>         ...yourCodeWhenConnectionIsMad...
            \n
            As mentioned, for details about the Stream object 'commander', see BasicStream()\n
        '''
        self._received_flag = 0
        self._bytes_received = 0
        self.uri = uri
        self.recBuff = recBuff
        self.recBuffSize = recBuffSize
        self.armed, self.takenoff, self.Estop, self.joystickIssue, self.mode, self.IsTracking = [0 for i in range(6)]
        self.connected = 0

        self.commander = BasicStream(uri=self.uri,
                                    agent='S',
                                    receiveBuffer=self.recBuff,
                                    sendBufferSize=2048,
                                    recvBufferSize=self.recBuffSize,
                                    nonBlocking=False,
                                    verbose=True,
                                    reshapeOrder='C')

        self.connected = self.commander.connected
        self.joystick_commands = np.zeros((5, 1), dtype=np.float64)


    def _send_commands(self, buff):
        '''
        This function sends the buffer array via Stream to the Simulink Mission Server.\n
        It is used internally and the user does not have to call this function.\n
        \n
        The buffer array is a 5-dimension numpy array of the form \n
        [arm, takeoff, Estop, joystickIssue, mode]. \n
        \n
        Returns: None\n
        '''
        self.commander.send(buffer=buff)


    def arm(self):
        '''
        This function is used to arm the drone. \n
        \n
        Usage:\n
            >>> myQdrone.arm()
        \n
        Returns: None
        '''
        if not self.takenoff:
            self.joystick_commands = np.array([1, 0, 0, 0, 0], dtype=np.float64)
            self._send_commands(self.joystick_commands)


    def takeoff(self):
        '''
        This function is used to takeoff \n.
        \n
        Usage:\n
            >>> myQdrone.takeoff()
        \n
        Returns: None
        '''
        if self.armed:
            self.joystick_commands = np.array([self.armed, 1, 0, 0, 0], dtype=np.float64)
            self._send_commands(self.joystick_commands)
            print("TAKING OFF", end='', flush=True)
            for i in range(8):
                print('.', end='', flush=True)
                t.sleep(1)
            print("TAKEOFF COMPLETED --> DRONE IN HOVER MODE!")


    def land(self):
        '''
        This function is used to Land the drone.\n
        \n
        Usage:\n
            >>> myQdrone.land()
        \n
        Returns: None
        '''
        if self.armed:
            print("LANDING...")
            self.joystick_commands = np.array([self.armed, 0, 0, 0, 0], dtype=np.float64)
            self._send_commands(self.joystick_commands)


    def activate_waypoint_mode(self):
        '''
        This function is used to activate way point mode. In this mode, the \n
        user can send either discrete waypoints or a smooth trajectory.\n
        \n
        Usage:\n
            >>> if (user selects waypoint mode):
            >>>     myqdrone.activate_waypoint_mode()
        \n
        Returns: None
        '''
        if not self.armed and not self.takenoff:
            print("Drone Must be in flight before requesting waypoints!")

        self.mode = 1
        self.joystick_commands = np.array([self.armed, self.takenoff, 0, 0, self.mode], dtype=np.float64)
        self._send_commands(self.joystick_commands)


    def activate_hover_mode(self):
        '''
        This function is used to activate Hover mode, the default mode after\n
        take off.\n
        \n
        Usage:\n
            >>> if (user selects hover mode):
            >>>     myqdrone.activate_hover_mode()
        \n
        Returns: None
        '''
        if not self.armed and not self.takenoff:
            print("Drone Must be in flight!")

        self.mode = 0
        self.joystick_commands = np.array([self.armed, self.takenoff, 0, 0, self.mode], dtype=np.float64)
        self._send_commands(self.joystick_commands)


    def check_connection(self):
        '''
        This function replicates the function of the 'commander.checkConnection()'\n
        function, which is used to poll the incoming remote client connection. \n
        \n
        Usage:\n
        >>> while True:
        >>>     if not myQdrone.connected:
        >>>         myQdrone.check_connection()
        >>>     else:
        >>>         ...yourCodeWhenConnectionIsMad...
        \n
        Returns:\n
            int, 0 if not connected and 1 if connected.
        '''
        self.commander.checkConnection()
        self.connected = self.commander.connected


    def receive_data(self):
        '''
        This function receives data from the client via the connection made\n
        in the __init__(). The data received is stored in the 'recBuff' array.\n

        \n
        Returns:\n
            5-dimensnion array of the form: \n
            [armed, takenoff, Estop, joystickIssue, IsTracking]\n
        \n
        Usage:\n
            >>> _data = np.zeros((5,1), dtype=np.float64)
            >>> _data = myQdrone.receive_data()
        '''
        self._received_flag, self._bytes_received = self.commander.receive()
        self.recBuff = self.commander.receiveBuffer
        self.armed, self.takenoff, self.Estop, self.joystickIssue, self.IsTracking = \
            [ self.recBuff[i][0] for i in range(self.recBuff.shape[0]) ]

        return self.recBuff


    def terminate(self):
        '''
        This function terminates the Stream connection gracefully.\n
        \n
        Usage:\n
            >>> myQdrone.terminate()
        '''
        self.commander.terminate()



class WaypointTrajectory(JoystickCommands):
    '''
    This class inherits from the JoystickCommands class and adds functionality specific\n
    to sending trajectories instead of joystick commands.\n
    \n
    '''

    def __init__(self, uri, recBuff=np.zeros((8, 1), dtype=np.float64), recBuffSize=64*2):
        '''
        Initialize WayPointTrajectory.

            params:\n
            recBuff         -   an 8x1 numpy array buffer to hold the received data\n
                                [x, y, z, roll, pitch, yaw, IsTracking, mode]  \n

            recBuffSize     -   Expected data size times 2 ie. 8 * 8 bytes multiplied by 2 \n

            traj_commands   -   numpy array, for sending trajectory commands of the form \n
                                [x, y, z, yaw, mode]\n

            x               -   float, x position\n

            y               -   float, y position\n

            z               -   float, z position\n

            roll            -   float, roll angle\n

            pitch           -   float, pitch angle\n

            yaw             -   float, yaw angle\n

        '''
        super().__init__(uri, recBuff, recBuffSize)
        self.traj_commands = np.zeros((5, 1), dtype=np.float64)
        self.x, self.y, self.z, self.roll, self.pitch, self.yaw = [0 for i in range(6)]


    def receive_data(self):
        '''
        This function receives data from the client via the connection made\n
        in the __init__(). The data received is stored in the 'recBuff' array.\n

        \n
        Returns:\n
            8-dimensnion float array of the form: \n
            [x, y, z, roll, pitch, yaw, IsTracking, mode]\n
        \n
        Usage:\n
            >>> _data = np.zeros((8,1), dtype=np.float64)
            >>> _data = myQdrone.receive_data()
        '''
        self._received_flag, self._bytes_received = self.commander.receive()
        self.recBuff = self.commander.receiveBuffer
        self.x, self.y, self.z, self.roll, self.pitch, self.yaw, self.IsTracking, self.mode = \
            [ self.recBuff[i][0] for i in range(self.recBuff.shape[0]) ]

        return self.recBuff


    def send_trajectory(self, traj):
        '''
        This function sends a trajectory of the form [x, y, z, yaw] to the Mission server\n
        \n
        Usage: \n
            >>> if ready_to_send_trajectory:
            >>>     myQdrone.mode = 1
            >>>     desired_traj = np.array([0.5, 0.1, -pi/6], dtype=np.float64)
            >>>     send_trajectory(traj=desired_traj)
            >>> else:
            >>>     DoSomethingElseMaybe()

        '''
        self._mode = np.array([self.mode], dtype=np.float64)
        self.traj_commands = np.concatenate((traj, self._mode))
        self._send_commands(buff=self.traj_commands)