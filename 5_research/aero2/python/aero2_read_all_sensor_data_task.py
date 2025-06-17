## aero2_read_all_sensor_data_task_qscope.py
# This examples shows how to read data from all the sensors on the Aero2 using task-based (time-based I/O) mode
# where you do not have to handle the timing yourself. It also shows how to plot the data in real-time with the
# 'scope' library using multiple scopes.
#--------------------------------------------------------------------------------------------------------------
# imports
import time
import numpy as np
from pal.products.aero2 import Aero2
from pal.utilities.scope import MultiScope
from threading import Thread
import signal

# Setup Thread killing using keyboard interrupts
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True

signal.signal(signal.SIGINT, sig_handler)


# add multiple signals to a multiscope
def add_scope_signals(multscope, ax=0, signals=["x", "y"]):
    # add signals to scope object
    for sig in signals:
        multscope.axes[ax].attachSignal(name=sig)


# Create Multiscope
scope = MultiScope(rows=2,cols=4,title="Aero2 Raw Sensor data", fps=30)

# Add each axis of the multiscope and attach the corresponding signals
scope.addAxis(row=0, col=0, timeWindow=15, yLabel="motor position (rad)")
add_scope_signals(multscope=scope, ax=0, signals=["motor0_pos", "motor1_pos"])

scope.addAxis(row=1, col=0, timeWindow=15, xLabel="Time (s)", yLabel="motor speed (rad/s)")
add_scope_signals(multscope=scope, ax=1, signals=["motor0_speed", "motor1_speed"])

scope.addAxis(row=0, col=1, timeWindow=15, yLabel="Angular velocity (rad/s)")
add_scope_signals(multscope=scope, ax=2, signals=["gyro_x", "gyro_y", "gyro_z"])

scope.addAxis(row=1, col=1, timeWindow=5, xLabel="Time (s)", yLabel="Angular Acceleration (rad/s^2)")
add_scope_signals(multscope=scope, ax=3, signals=["accel_x", "accel_y", "accel_z"])

scope.addAxis(row=0, col=2, timeWindow=15, yLabel="motor current (Amps)")
add_scope_signals(multscope=scope, ax=4, signals=["motor0_current", "motor1_current"])

scope.addAxis(row=1, col=2, timeWindow=15, xLabel="Time (s)", yLabel="Attitude (rad)")
add_scope_signals(multscope=scope, ax=5, signals=["pitch_angle", "yaw_angle"])

scope.addAxis(row=0, col=3, rowSpan=2, timeWindow=15, xLabel="Time (s)", yLabel="Attitude rates (rad/s)")
add_scope_signals(multscope=scope, ax=6, signals=["pitch_rate", "yaw_rate"])


# Initialize Aero2
myAero2 = Aero2(id=0, hardware=0, readMode=1, frequency=500)


def control_loop():
    # timing
    startTime = time.time()
    timestamp = 0
    runTime = 20

    # initialize led color
    color = np.array([0, 1, 0], dtype=np.float64)

    try:
        while (timestamp <= runTime) and (not KILL_THREAD):
            # read sensor information
            myAero2.read_analog_encoder_other_channels()

            # set voltage commands
            voltage0, voltage1 = np.array([7, 4], dtype=np.float64)

            # write commands
            myAero2.write_led(color)
            myAero2.write_voltage(voltage0, voltage1)

            # update scopes
            scope.axes[0].sample(timestamp, [myAero2.motorPosition[0], myAero2.motorPosition[1]])
            scope.axes[1].sample(timestamp, [myAero2.motorSpeed[0], myAero2.motorSpeed[1]])
            scope.axes[2].sample(timestamp, [myAero2.gyroscope[0], myAero2.gyroscope[1], myAero2.gyroscope[2]])
            scope.axes[3].sample(timestamp, [myAero2.accelerometer[0], myAero2.accelerometer[1], myAero2.accelerometer[2]])
            scope.axes[4].sample(timestamp, [myAero2.motorCurrent[0], myAero2.motorCurrent[1]])
            scope.axes[5].sample(timestamp, [myAero2.pitchAngle, myAero2.yawAngle])
            scope.axes[6].sample(timestamp, [myAero2.pitchRate, myAero2.yawRate])
            
            # timing
            timestamp = time.time() - startTime
    
    except KeyboardInterrupt:
        "User interrupted!"
    
    finally:
        myAero2.terminate()
        input("Press ENTER to continue!")


# Create and run thread
sensor_read = Thread(target=control_loop)
sensor_read.start()

while sensor_read.is_alive() and (not KILL_THREAD):
    MultiScope.refreshAll()
    time.sleep(0.01)