This example demonstrates how to send joystick commands from python to a
Simulink-generated Real-time executable. It uses Quanser's legacy Stream API
for communication. Two classes are written in the 'commander.py' module and
used to implement this example.

Requirements:
-------------

- Ensure you have the Quanser QUARC Python APIs. The recommended way to install
this will be via the Research Resources Zip that you should have received.

File Contents
--------------
- rt_models/ - folder containing the RT models
- joystick_commands.py - script to send joystick commands
- qlabs_setup.py - script to setup the qlabs workspace
- waypoint_commands - script to send discrete waypoints/trajectories
- commander.py - module for communicating with Mission server
- qlabs_vrpn_server.exe - to broadcast virtual qdrone2 pose via vrpn

How to Run:
-----------

1. Open Quanser Interactive Labs, open the QDrone2 workspace and select the
Warehouse workspace.

2. Open visual studio code (recommended) and ensure you're current folder is the folder
containing this README. You may use your preferred IDE, or Windows command prompt.

3. Open and run the 'joystick_commands.py' python script. This will (in the
order below):
    a. call the qlabs_setup script to refresh the QLabs workspace, spawn a virtual
    QDrone2. If the USE_VRPN constant is set, the qlabs_setup script also starts
    the QLabs vrpn server.
    b. Open a connection to the mission server
    c. Start the Mission server RT model - this may be MissionServerLegacy or MissionServerVRPN
        depending on if the USE_VRPN constant is set or not.
    d. Start the Dronestack/stabilizer RT model
    e. start sending joystick commands to the Mission Server

4. User input (case insensitive):
    The user will be prompted to:
    - Arm (y/n)
    - TakeOff (y/n)
    - Land or Send Waypoints (l/w)
        If Key 'W' is pressed on the keyboard, the virtual drone goes into WAYPOINT MODE.
        If Key 'L' is pressed on the keyboard, the virtual drone will Land.

    - Sending Waypoints/Trajectories
        When the QDrone2 has taken off, run (in a separate terminal), the
        'waypoint_commands.py' file to send either discrete waypoints or a smooth trajectory,
        depending on your settings in the 'waypoint_commands.py' file.
        Use Ctrl+C to stop the script at any time.

    - Reading IMU/State data
        When the QDrone2 has taken off, run (in a separate terminal), the
        'stream_stack_client_qd2'.py file to receive IMU/state data from the
        QDrone2. Use Ctrl + C to stop the script at anytime.

    - Terminate the 'joystick_commands.py' file at any time using Ctrl + C

5. You can monitor the status of the simulation from the QUARC Console.
   For virtual only, if using VRPN, you can monitor the vrpn connection via
   the qlabs_vrpn_server terminal window.

