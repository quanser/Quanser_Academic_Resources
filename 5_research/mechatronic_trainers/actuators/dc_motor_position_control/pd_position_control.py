# DC Motor - PD position control

# region: Python level imports
import numpy as np
import subprocess
import sys
import os

from pal.products.actuators import ActuatorsTrainer
from pal.utilities.probe import Probe
from pal.utilities.timing import Timer
from pal.utilities.math import SignalGenerator
# endregion 

#region: Scope setup
# Scopes for motor voltage, encoder and speed
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=1, name='Motor Voltage')
probe.add_scope(numSignals=1, name='Motor Current')
probe.add_scope(numSignals=2, name='Motor Position')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer_position.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()
# endregion


# region: Experiment constants
simulationTime = 120 # will run for this amount of seconds
frequency = 300 # Hz
counter = 0 # counter to track scopes
encoderRatio = 2*np.pi/(4096*27)

position = np.pi/4
# Square wave command generator for position and 5 second period
squareWaveGenerator = SignalGenerator().square(position, 4)
desiredPosition = next(squareWaveGenerator)

k_p, k_d = (8.5, 0.15)

# region: Main Loop
with ActuatorsTrainer(block = 3) as actuators:
    # Initialize timer
    timer = Timer(frequency, simulationTime)

    actuators.enable_motors()

    while timer.check() and probe.connected:

        # get current timestamp and read data from encoder & tach
        currentTime = timer.get_current_time()
        actuators.read_outputs()

        counts = actuators.encoder # counts
        tachometer = actuators.tach # counts/s

        current = actuators.dcMotorCurrent

        # update voltage command, as well as motor position & speed
        desiredPosition = squareWaveGenerator.send(currentTime)
        motorPosition   = encoderRatio*counts
        speed      = encoderRatio*tachometer
        voltage = k_p * (desiredPosition - motorPosition) - k_d * ( speed )

        # update scopes every fourth sample
        if counter%4 == 0:
            probe.send(name='Motor Voltage',
                        scopeData=(currentTime,[voltage]))
            probe.send(name='Motor Current',
                        scopeData=(currentTime,[current]))
            probe.send(name='Motor Position',
                        scopeData=(currentTime,[motorPosition, desiredPosition]))

        # The update_dc function accepts commands from -1 to 1 that
        # map to -12 to 12 V. This is the conversion.
        actuators.update_dc(voltage/12, limitCmd=False)
        actuators.write_motors()

        counter += 1
        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()
#endregion