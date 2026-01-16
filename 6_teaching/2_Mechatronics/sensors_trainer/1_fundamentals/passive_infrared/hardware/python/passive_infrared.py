import subprocess
import sys
import os

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe


# System variables
simulationTime = 45 # will run for this amount of seconds
frequency = 400 # Hz

cntr1s = 0
cntr3s = 0
counter = 0

timer = Timer(sampleRate=frequency, totalTime=simulationTime)

# Scopes for motor voltage, encoder and speed
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=1, name='Passive Infrared')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()



# Main application loop
with SensorsTrainer() as sensors:

    while timer.check():
        currentTime = timer.get_current_time()

        sensors.read_outputs()

        pir = sensors.passiveIR

        # add some filtering?
        
        if counter%5 == 0:

            probe.send(name='Passive Infrared',
                        scopeData=(currentTime, [pir]))

        counter += 1

        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()