## aero2_1dof_rotor_0_pi_control_immediate.py
# This example implements a Proportional-Integral (PI) controller for rotor 0 of the Aero2 in the
# 1-dof configuration and uses immediate I/O where you have to handle the timing by yourself. 
# In this example, the sample frequency is 150 Hz. This example also plots the data in real-time 
# using the 'scope' library.
#---------------------------------------------------------------------------------------------------

import time
import numpy as np
from pal.products.aero2 import Aero2
from pal.utilities.math import SignalGenerator
from pal.utilities.scope import Scope

def elapsed_time():
    return time.time() - startTime


def PID(sampleTime, kp, ki, kd=0, init_control_input=0):
    control_input = init_control_input
    integral = 0
    while True:
        # yield control_input, wait for next measured, desired, derivative of measured
        measured, desired, derivative_of_measured = yield control_input
        error = desired - measured
        integral += (error * sampleTime)
        control_input = init_control_input + (kp * error) + ki * integral - (kd * derivative_of_measured)


# run time setup
timestamp = 0
runTime, frequency = (15, 150)
sampleTime = 1/frequency

# initialize led RGB variable
color = np.array([0, 1, 0], dtype=np.float64)

# PI Controller
kp_r, ki_r = (0.067, 0.6794)
PI_controller = PID(sampleTime, kp_r, ki_r)
PI_controller.send(None)

# initialize reference
signalGen = SignalGenerator()
squareWave = signalGen.square(120, 5)
next(squareWave)

# create scope to plot data
scope = Scope(title="Rotor 0 speed response", timeWindow=5, xLabel='Time(s)', yLabel='Speed(rad/s)')
scope.attachSignal(name="desired_speed")
scope.attachSignal(name="measured_speed")

scope1 = Scope(name="Commanded voltage", timeWindow=5, xLabel="Time(s)", yLabel="Voltage(V)")
scope1.attachSignal(name="motor_0_input_voltage")

# Initialize Aero2
myAero2 = Aero2(id=0, hardware=0, readMode=0, frequency=500)

# timing - for immediate I/O define this after creating the Aero2 object
startTime = time.time()

try:
    while timestamp < runTime:
        compStart = time.time()

        motor_0_desired_speed = squareWave.send(timestamp)

        # get speed of motor 0
        myAero2.read_analog_encoder_other_channels()
        motor_0_meas_speed = myAero2.motorSpeed[0]

        # compute control input
        cmd_voltage0 = PI_controller.send([motor_0_meas_speed, motor_0_desired_speed, 0])
       
        # write control commands
        myAero2.write_led(color)
        myAero2.write_voltage(cmd_voltage0)

        # plot data in real-time
        scope.sample(timestamp, [motor_0_desired_speed, motor_0_meas_speed])
        scope1.sample(timestamp, [cmd_voltage0])
        Scope.refreshAll()

        # timing
        computation_time = time.time() - compStart
        time.sleep(sampleTime - (computation_time % sampleTime))
        timestamp = elapsed_time()
        

except KeyboardInterrupt:
    "User interrupted!"

finally:
    # terminate Aero2
    myAero2.terminate() 
    input("Press ENTER to continue!")