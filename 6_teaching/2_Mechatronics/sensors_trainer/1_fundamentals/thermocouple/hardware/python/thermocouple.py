# Thermocouple 

# Understanding how to read a thermocouple.

# region: Python level imports
import subprocess
import sys
import os

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
# endregion 

#region: Scope setup
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=2, name='Temperatures')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()
# endregion

# region: Experiment constants
simulationTime = 150 # will run for this amount of seconds
frequency = 200 # Hz
counter = 0
# endregion

# region: Main Loop
with SensorsTrainer() as sensors:
    timer = Timer(sampleRate=frequency, totalTime=simulationTime)

    while timer.check():
        currentTime = timer.get_current_time()

        sensors.read_outputs()

        tempThermoChip = sensors.tempThermoChip
        tempThermo = sensors.tempThermo

        # add some filtering?
        
        if counter%10 == 0:
            probe.send(name='Temperatures',
                        scopeData=(currentTime, [tempThermoChip, tempThermo]))

        counter += 1

        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()
# endregion



