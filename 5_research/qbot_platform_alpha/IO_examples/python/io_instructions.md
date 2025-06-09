**Version:0**
**Date: 9/7/2023**

# Instructions

1. Turn on the QBot Platform by pressing the silver button on the back of
    the QBot Platform next to the LCD once. The LCD screen should turn on.

2. Ensure that a connection to the robot is established by pinging it. Type in
    a terminal window:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ping - t 192.168.X.X
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    where the X's are your robots IP address displayed on the LCD. If it can't
    be pinged make sure you are on the same network as the QBot Platform.

3. Change the **ipAddress** variable in the **io_example.py** file to the ip
    address of your robot.

4. Transfer the files (both the driver rt file and the io_example.py file) to
    the QBot Platform. This can be done using WinSCP or through the terminal
    using scp.  See the **Connectivity User Manual** for more details.

5. Run the file. This can be done by connecting to the robot either through
    the terminal or VNC or your method of choice. Look at the **Connectivity
    User Manual** for more information. This can be done through the terminal
    through ssh,
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ssh 192.168.X.X
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    where the X's are replaced with your robots IP
    address. This will prompt you to log in with your user ('**pi**') and
    password ('**QuanserPi4**') and navigating to where this file is stored.

6. Run the driver. This can be done in the terminal using the command:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    sudo quarc_run -t tcpip://localhost:17000 -Q qbot_driver_v_1_22.rt-linux_pi_arm64
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    You should see the lights begin to flash white on the QBot Platform if the
    driver has started properly.

    ## General Notes on the Driver Model:
    The driver model has been created for safety purposes with driving the QBot
    Platform. There are several different inputs that get sent to driver model:

    #### On Initialization:
    - Mode
    - IP Address

    #### Reading & Writing:
    - Hold (0 or 1)
    - User LED (0 or 1)
    - Color (3x1 array of values between 0 and 1)
    - Enable Motors/Arming (0 or 1)
    - Commands (which in this example is forward linear velocity (rads/s) and
        rotational angular velocity (rads/s))
    - Timestamp

    If you set the **hold** variable to be 1, the robot will hold its current
    position, even when bumped or pushed.  By default in this model, we've set
    this to 0.

    #### Built in Driver LEDs

    The driver also has some LED colors built into it to let you know when the
    QBot Platform is in different states.

    - Once you run the model in step 6 the lights will turn **green**, this
    shows that your model is running and the motors have been enabled.
    - If you set the variable enableMotors to 0, the light will turn
    **blue**.
    - If your battery is too low, the lights will turn **purple** to let
    you know you need to charge your robot.
    - If your lights turn **yellow**, it means you've caused a stall or
    overcurrent condition.
    - You can override the blue or green values with your own input by
    changing the **userLED** variable to be True and changing the **color**
    variable to be a color of your choice.

    #### Debugging Note:
    If you see the lights flicker from green to white,
    it means the QBot Platform is struggling to connect to your Wi-Fi and
    has disconnected for more then 1 second. Moving your robot closer to the
    router should solve this problem.

7.  Make sure the QBot has space around it.  This test will cause the robot to
    turn in place while running the cameras, lidar and other sensors onboard.
    Run the **io_example.py** file by running the command in terminal:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    sudo PYTHONPATH=$PYTHONPATH python3 io_example.py
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Initially, the **motorEnable** variable is set to **1**, so that we can
    command the motor positions.  This will make the QBot Platform start
    spinning in place. If it is set to 0, all motors are off. If you want it to
    spin to the other direction, change the sign on the inputted
    **turningVelocity** variable in the io_example.py script and retransfer the
     file over to the QBot Platform before running the file.

    **NOTE:** The maximum forward linear velocity and rotational angular
    velocity that the QBot Platform can reach is 0.7 m/s and 3.564 m/s
    respectively. The QBot Platform driver ran in step 6 has a speed controller
    to maintain speed under different conditions. This is for safety purposes
    and teaching.  If you want to work with higher speeds, change the mode to
    2 or 3 (2 is wheeled, 3 is body).

9. When the lidar and cameras have stopped running, a window will pop up with 6
    scope outputs.

    ### Scope Outputs

    1. The first scope is the **Wheel Position** - Using the tachometer on each
        wheel the scope is showing its position in radians.
    2. The second is the **Wheel Speed & Motor Commanded**. Using the
        tachometers in the wheels and the motor commanded in volts used to
        maintain those speeds. Since the robot is turning on the spot, both
        values for right and left wheels should be equal and opposite.
    3. The following scope, shows the acceleration using the **Accelerometer**
        in the robots X,Y and Z values.
    4. The next scope shows the **Gyroscope** sensor divided by the robot's X,
        Y and Z values.
    5. The second last scope shows the **Motor Current** output of each of the
        two motors in Amps.
    6. Finally the last scope shows the battery voltage of the current battery
        being used by the QBot. If the current battery is under 12 V, the QBot
        will switch to use the other available battery. The QBot will turn off
        if the battery/batteries go under 11.5 volts.

10. To end the program from running, you will need to **close the scope pop up
    window**.

11. When you're done, stop the driver from running on the QBot Platform by
    running this command:
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    sudo quarc_run -t tcpip://localhost:17000 -Q -q qbot_driver_v_1_22.rt-linux_pi_arm64
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

