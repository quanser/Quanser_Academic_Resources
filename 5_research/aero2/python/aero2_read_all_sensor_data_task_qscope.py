## aero2_read_all_sensor_data_task_qscope.py
# This examples shows how to read data from all the sensors on the Aero2 using task-based (time-based I/O) mode
# where you do not have to handle the timing yourself. It also shows how to plot the data in real-time with the
# q_scopes library.
#--------------------------------------------------------------------------------------------------------------
# imports
import time
import numpy as np
from pal.products.aero2 import Aero2
from pal.utilities.scope import Scope

def elapsed_time():
    return time.time() - startTime

def create_scopes(n=2, mode="pan", span=5):
    # creates n scopes
    scopes = []
    for i in range(n):
        scopes.append(Scope(name="q_scope"+str(i+1), mode=mode, span=span))

    return scopes

def add_scope_signals(scopes, signals=["x", "y"], k=1):
    # add signals to scope object
    for sig in signals:
        scopes[k].add_signal(sig)

# run time settings
startTime = time.time()
timestamp = 0
runTime = 20

# initialize led color
color = np.array([0, 1, 0], dtype=np.float64)

# create and add signals to scopes for plotting
qscope = create_scopes(7) # create 7 scopes
add_scope_signals(qscope, ["motor0_pos", "motor1_pos"], 0)
add_scope_signals(qscope, ["motor0_speed", "motor1_speed"], 1)
add_scope_signals(qscope, ["gyro_x", "gyro_y", "gyro_z"], 2)
add_scope_signals(qscope, ["accel_x", "accel_y", "accel_z"], 3)
add_scope_signals(qscope, ["motor0_current", "motor1_current"], 4)
add_scope_signals(qscope, ["pitch_angle", "yaw_angle"], 5)
add_scope_signals(qscope, ["pitch_rate", "yaw_rate"], 6)

# Initialize Aero2
myAero2 = Aero2(id='0', hardware=0, readMode=1, frequency=500)

try:
    while timestamp < runTime:
        # read sensor information
        myAero2.read_analog_encoder_other_channels()

        # set voltage commands
        voltage0, voltage1 = np.array([7, 4], dtype=np.float64)

        # write commands
        myAero2.write_led(color)
        myAero2.write_voltage(voltage0, voltage1)

        # update scopes
        qscope[0].sample(timestamp, [myAero2.motorPosition[0], myAero2.motorPosition[1]])
        qscope[1].sample(timestamp, [myAero2.motorSpeed[0], myAero2.motorSpeed[1]])
        qscope[2].sample(timestamp, [myAero2.gyroscope[0], myAero2.gyroscope[1], myAero2.gyroscope[2]])
        qscope[3].sample(timestamp, [myAero2.accelerometer[0], myAero2.accelerometer[1], myAero2.accelerometer[2]])
        qscope[4].sample(timestamp, [myAero2.motorCurrent[0], myAero2.motorCurrent[1]])
        qscope[5].sample(timestamp, [myAero2.pitchAngle, myAero2.yawAngle])
        qscope[6].sample(timestamp, [myAero2.pitchRate, myAero2.yawRate])
        Scope.refreshAll()

        # timing
        timestamp = elapsed_time()

except KeyboardInterrupt:
    print("User interrupted!")

finally:

    myAero2.terminate()
    input('Press ENTER to continue')