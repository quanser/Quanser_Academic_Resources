## example balance_control_qube.py
# This example does balance control of the Qube Servo's Pendulum attachment.
# This example uses either a virtual or Physical Qube Servo 2 or Qube Servo 3 device,
# in a task-based (time-based IO) mode where you do not have to handle timing yourself.
# (task based mode is recommended for most applications).

# IF USING HARDWARE, LIFT THE PENDULUM MANUALLY FOR THE CONTROLLER TO KICK IN
# IF USING VIRTUAL, USE THE LIFT PENDULUM BUTTON IN QUANSER INTERACTIVE LABS
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# imports
from threading import Thread
import signal
import time
import math
import numpy as np
from pal.products.qube import QubeServo2, QubeServo3
from pal.utilities.math import SignalGenerator, ddt_filter
from pal.utilities.scope import Scope

# Setup to enable killing the data generation thread using keyboard interrupts
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)


#region: Setup
simulationTime = 30 # will run for 30 seconds
color = np.array([0, 1, 0], dtype=np.float64)


scopePendulum = Scope(
    title='Pendulum encoder - alpha (rad)',
    timeWindow=10,
    xLabel='Time (s)',
    yLabel='Position (rad)')
scopePendulum.attachSignal(name='Pendulum - alpha (rad)',  width=1)

scopeBase = Scope(
    title='Base encoder - theta (rad)',
    timeWindow=10,
    xLabel='Time (s)',
    yLabel='Position (rad)')
scopeBase.attachSignal(name='Base - theta (rad)',  width=1)

scopeVoltage = Scope(
    title='Motor Voltage',
    timeWindow=10,
    xLabel='Time (s)',
    yLabel='Voltage (volts)')
scopeVoltage.attachSignal(name='Voltage',  width=1)

#endregion

# Code to control the Qube Hardware
# CHANGE qubeVersion, hardware and pendulum VARIABLES FOR DIFFERENT SETUPS
def control_loop():

    # set as 2 or 3 if using a Qube Servo 2 or 3 respectively
    qubeVersion = 3

    # Set as 0 if using virtual Qube Servo
    # Set as 1 if using physical Qube Servo
    hardware = 1

    # Only matters when using virtual Qube. 
    # Set as 0 for virtual DC Motor and 1 for virtual pendulum
    # KEEP AS 1, THIS EXAMPLE USES A PENDULUM
    # not important if using virtual
    pendulum = 1


    frequency = 500# Hz
    state_theta_dot = np.array([0,0], dtype=np.float64)
    state_alpha_dot = np.array([0,0], dtype=np.float64)

    # Limit sample rate for scope to 50 hz
    countMax = frequency / 50
    count = 0

    if qubeVersion == 2:
        QubeClass = QubeServo2
        K = np.array([-1, 34.75, -1.495, 3.111])
    else:
        QubeClass = QubeServo3
        K = np.array([-1.2247, 24.9044, -0.6877, 3.1321])

    with QubeClass(hardware=hardware, pendulum=pendulum, frequency=frequency) as myQube:

        startTime = 0
        timeStamp = 0
        def elapsed_time():
            return time.time() - startTime
        startTime = time.time()

        while timeStamp < simulationTime and not KILL_THREAD:

            # Read sensor information
            myQube.read_outputs()

            theta = myQube.motorPosition * -1
            alpha_f =  myQube.pendulumPosition
            alpha = np.mod(alpha_f, 2*np.pi) - np.pi
            alpha_degrees = abs(math.degrees(alpha))

            # Calculate angular velocities with filter of 50 and 100 rad
            theta_dot, state_theta_dot = ddt_filter(theta, state_theta_dot, 50, 1/frequency)
            alpha_dot, state_alpha_dot = ddt_filter(alpha, state_alpha_dot, 100, 1/frequency)

            command_deg = 0

            states = command_deg*np.array([np.pi/180, 0, 0, 0]) - np.array([theta, alpha, theta_dot, alpha_dot])

            if alpha_degrees > 10:
                voltage = 0
            else:
                voltage = -1*np.dot(K, states)

            # # Write commands
            myQube.write_voltage(voltage)

            # Plot to scopes
            count += 1
            if count >= countMax:
                scopePendulum.sample(timeStamp, [states[1]])
                scopeBase.sample(timeStamp, [states[0]])
                scopeVoltage.sample(timeStamp,[voltage])
                count = 0

            timeStamp = elapsed_time()



# Setup data generation thread and run until complete
thread = Thread(target=control_loop)
thread.start()

while thread.is_alive() and (not KILL_THREAD):

    # This must be called regularly or the scope windows will freeze
    # Must be called in the main thread.
    Scope.refreshAll()
    time.sleep(0.01)


input('Press the enter key to exit.')
