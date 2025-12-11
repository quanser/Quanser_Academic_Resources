# Encoder 

# Understanding encoder values and the driving signals for it.

# region: Python level imports
import numpy as np
import subprocess
import os
import sys

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
# endregion 

#region: Scope setup
# Scopes for encoder pulses and counts
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=2, name='Encoder Pulses')
probe.add_scope(numSignals=1, name='Encoder Counts')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()
# endregion

# region: Experiment constants
simulationTime = 500 # will run for this amount of seconds
frequency = 300 # Hz

counter = 0 # counter to track scopes
counterHalfSec = 0
# endregion

# region: Main Loop
with SensorsTrainer(knobEncQuad=4) as sensors:
    timer = Timer(sampleRate=frequency, totalTime=simulationTime)

    while timer.check():
        
        currentTime = timer.get_current_time()

        sensors.read_outputs()

        encoder = sensors.encoder0
        encoderPulses = sensors.encoderPulses
        
        # update scopes every 4 samples
        if counter%4 == 0:
            probe.send(name='Encoder Pulses',
                        scopeData=(currentTime,[encoderPulses[0], encoderPulses[1]]))
            probe.send(name='Encoder Counts',
                        scopeData=(currentTime,[encoder]))
            
        # Do something every half second
        if counterHalfSec%150 == 0:  # half of the frequency will give us half a second.
            countsPerRev = 0
            
        counter += 1
        counterHalfSec += 1
        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()
# endregion





