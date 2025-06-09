## example read_write_qube2.py
# This example reads and writes all available IO in the Qube Servo 2.
# This example uses either a virtual or physical Qube Servo 2 device,
# in a task-based (time-based IO) mode where you do not have to handle timing yourself
# (task based mode is recommended for most applications).
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# imports
from threading import Thread
import signal
import time
import random
import numpy as np
from pal.products.qube import QubeServo2
from pal.utilities.math import SignalGenerator
from pal.utilities.scope import MultiScope

# Setup to enable killing the data generation thread using keyboard interrupts
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)

#region: Setup
simulationTime = 10 # will run for 10 seconds
color = np.array([0, 1, 0], dtype=np.float64)

sineWave = SignalGenerator().sine(5, 1)
next(sineWave)

multiScope = MultiScope(
    rows=2,
    cols=3,
    title="Qube-Servo 2 Read Signals"
)

multiScope.addAxis(row=0, col=0, timeWindow=5)
multiScope.axes[0].attachSignal(name='Motor encoder counts')
multiScope.axes[0].attachSignal(name='Motor counts/sec')

multiScope.addAxis(row=0, col=1, timeWindow=5)
multiScope.axes[1].attachSignal(name='Pendulum encoder counts')

multiScope.addAxis(row=0, col=2, timeWindow=5)
multiScope.axes[2].attachSignal(name='Motor Current')

multiScope.addAxis(row=1, col=0, timeWindow=5)
multiScope.axes[3].attachSignal(name='Motor encoder position (rad)')
multiScope.axes[3].attachSignal(name='Motor speed (rad/s)')

multiScope.addAxis(row=1, col=1, timeWindow=5)
multiScope.axes[4].attachSignal(name='Pendulum encoder position (rad)')

multiScope.addAxis(row=1, col=2, timeWindow=5)
multiScope.axes[5].attachSignal(name='Amplifier Fault')
multiScope.axes[5].attachSignal(name='Motor Stall Detected')
multiScope.axes[5].attachSignal(name='Motor Stall Error')



#endregion - SETUP FINISHED

# Code to control the Qube Hardware
# CHANGE hardware AND pendulum VARIABLE IF USING VIRTUAL QUBE
def control_loop():

    # Limit sample rate for scope to 50 hz
    # (Qube default frequency in task based IO is 500Hz)
    countMax = 500 / 50
    count = 0

    timeStamp = 0
    timeSeconds = 0

    # Set as 0 if using virtual Qube Servo 2
    # Set as 1 if using physical Qube Servo 2
    hardware = 1

    # only important when using virtual Qube. 
    # Set as 0 if using virtual QUBE 2 - DC Motor
    # Set as 1 if using virtual QUBE 2 - Pendulum
    pendulum = 0

    with QubeServo2(hardware = hardware, pendulum = pendulum) as myQube:
        startTime = 0
        timeStamp = 0
        def elapsed_time():
            return time.time() - startTime
        startTime = time.time()

        while timeStamp < simulationTime and not KILL_THREAD:

            # Read sensor information
            myQube.read_outputs()

            # Command square wave
            voltageIn = sineWave.send(timeStamp)

            # Write commands
            myQube.write_voltage(voltageIn)
            # change LED color randomly every second
            if (timeStamp - timeSeconds) >= 1:
                myQube.write_led(
                    np.array(
                    [random.random(), random.random(), random.random()],
                    dtype=np.float64))

            timeSeconds = int(timeStamp)

            # plot to scopes
            count += 1
            if count >= countMax:
                multiScope.axes[0].sample(
                    timeStamp,
                    [myQube.motorEncoderCounts, myQube.motorCountsPerSecond])
                multiScope.axes[1].sample(
                    timeStamp,
                    [myQube.pendulumEncoderCounts])
                multiScope.axes[2].sample(
                    timeStamp,
                    [myQube.motorCurrent])
                multiScope.axes[3].sample(
                    timeStamp,
                    [myQube.motorPosition, myQube.motorSpeed])
                multiScope.axes[4].sample(
                    timeStamp,
                    [myQube.pendulumPosition])
                multiScope.axes[5].sample(
                    timeStamp,
                    [myQube.amplifierFault,
                     myQube.motorStallDetected,
                     myQube.motorStallError])
                count = 0

            timeStamp = elapsed_time()



# Setup data generation thread and run until complete
thread = Thread(target=control_loop)
thread.start()

while thread.is_alive() and (not KILL_THREAD):

    # This must be called regularly or the scope windows will freeze
    # Must be called in the main thread.
    multiScope.refresh()
    time.sleep(0.01)

input('Press the enter key to exit.')
