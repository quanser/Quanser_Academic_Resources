# Weather 

# Understanding weather sensor and how it updates.

# region: Python level imports
import subprocess
import sys
import os

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
# endregion 

#region: Scope setup
# Scopes for temperature, pressure & humidity
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=1, name='Temperature')
probe.add_scope(numSignals=1, name='Pressure')
probe.add_scope(numSignals=1, name='Humidity')
probe.add_scope(numSignals=1, name='Altitude Above Sea Level')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()
# endregion

# region: Experiment constants
simulationTime = 300 # will run for this amount of seconds
frequency = 10 # Hz
# endregion

# region: Main Loop
with SensorsTrainer() as sensors:
    timer = Timer(sampleRate=frequency, totalTime=simulationTime)
    while timer.check():
        currentTime = timer.get_current_time()

        sensors.read_outputs()

        tempWeather = sensors.tempWeather
        pressure = sensors.pressure
        humidity = sensors.humidity

        seaLevelhPa = 1013.25
        
        altitude = 0 # altitude in meters
    
        probe.send(name='Temperature',
                    scopeData=(currentTime, [tempWeather]))
        probe.send(name='Pressure',
                    scopeData=(currentTime, [pressure]))
        probe.send(name='Humidity',
                    scopeData=(currentTime, [humidity]))
        probe.send(name='Altitude Above Sea Level',
                    scopeData=(currentTime, [altitude]))


        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()
#endregion



