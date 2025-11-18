import numpy as np
import subprocess
import os
import sys

from pal.products.actuators import ActuatorsTrainer
from pal.utilities.probe import Probe
from pal.utilities.timing import Timer
from pal.utilities.math import SignalGenerator

simulationTime = 120 # will run for this amount of seconds
frequency = 120 # Hz
counter = 0 # counter to track scopes
prevSpeed = 0
encoderRatio = 1
squareWaveVoltage = 12

# Square wave command generator at a 12 Volt amplitude and 4 second period
squareWaveGenerator = SignalGenerator().square(squareWaveVoltage, 4)
dc_command = next(squareWaveGenerator)

# model parameters
speedGain   = 0 # rads / s / V
beta        = 0.15  # filter parameter

# Scopes for motor voltage, encoder and speed
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=1, name='Motor Voltage')
probe.add_scope(numSignals=1, name='Motor Encoder')
probe.add_scope(numSignals=1, name='Motor Speed')
probe.add_scope(numSignals=2, name='Motor Model')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()

# Initialize timer
timer = Timer(frequency, simulationTime)

with ActuatorsTrainer(block = 2) as actuators:

    actuators.enable_motors()

    while timer.check() and probe.connected:

        # get current timestamp and read data from encoder & tach
        currentTime = timer.get_current_time()
        actuators.read_outputs()

        # update voltage command, as well as motor position & speed
        dc_command = squareWaveGenerator.send(currentTime)
        position   = encoderRatio*actuators.encoder
        speed      = encoderRatio*actuators.tach
        mdlSpeed   = (((1-beta)*prevSpeed) + (beta*speedGain*dc_command))

        # update scopes every second sample
        if counter%2 == 0:
            probe.send(name='Motor Voltage',
                        scopeData=(currentTime,[dc_command]))
            probe.send(name='Motor Encoder',
                        scopeData=(currentTime,[position]))
            probe.send(name='Motor Speed',
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

probe.terminate()