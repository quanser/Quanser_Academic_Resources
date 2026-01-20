# DC Motor - drive

# Characterizing a DC motor.

# region: Python level imports
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
probe.add_scope(numSignals=1, name='Motor Encoder')
probe.add_scope(numSignals=1, name='Tachometer (Motor Speed)')
probe.add_scope(numSignals=2, name='Motor Model')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()
# endregion


# region: Experiment constants
simulationTime = 120 # will run for this amount of seconds
frequency = 120 # Hz
counter = 0 # counter to track scopes
prevSpeed = 0
encoderRatio = 1
squareWaveVoltage = 12

# model parameters
speedGain   = 0 # rads / s / V
beta        = 0.15  # filter parameter
# endregion

# Square wave command generator at a 12 Volt amplitude and 4 second period
squareWaveGenerator = SignalGenerator().square(squareWaveVoltage, 4)
dc_command = next(squareWaveGenerator)


# region: Main Loop
with ActuatorsTrainer(block = 2) as actuators:
    # Initialize timer
    timer = Timer(frequency, simulationTime)

    actuators.enable_motors()

    while timer.check() and probe.connected:

        # get current timestamp and read data from encoder & tach
        currentTime = timer.get_current_time()
        actuators.read_outputs()

        counts = actuators.encoder # counts
        tachometer = actuators.tach # counts/s

        # update voltage command, as well as motor position & speed
        dc_command = squareWaveGenerator.send(currentTime)
        position   = encoderRatio*counts
        speed      = encoderRatio*tachometer
        mdlSpeed   = (((1-beta)*prevSpeed) + (beta*speedGain*dc_command))

        # update scopes every second sample
        if counter%2 == 0:
            probe.send(name='Motor Voltage',
                        scopeData=(currentTime,[dc_command]))
            probe.send(name='Motor Encoder',
                        scopeData=(currentTime,[position]))
            probe.send(name='Tachometer (Motor Speed)',
                        scopeData=(currentTime,[speed]))
            probe.send(name='Motor Model',
                        scopeData=(currentTime,[speed, mdlSpeed]))

        # The update_dc function accepts commands from -1 to 1 that
        # map to -12 to 12 V. This is the conversion.
        actuators.update_dc(dc_command/12, limitCmd=False)
        actuators.write_motors()

        counter += 1
        prevSpeed = mdlSpeed
        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()
#endregion