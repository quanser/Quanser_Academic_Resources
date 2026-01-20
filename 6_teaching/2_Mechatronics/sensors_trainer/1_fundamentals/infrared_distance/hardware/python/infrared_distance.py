# region: system imports
import numpy as np
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.scope import MultiScope
# endregion 

# region: observer definition 
simulationTime = 60 # will run for this amount of seconds

scope = MultiScope(rows= 2, cols =1,
            title='Infrared Measurement',
            fps=60 )

# Distance scope
window = simulationTime/2
scope.addAxis(row=0,
            col=0,
            timeWindow=window,
            yLabel='Voltage (V)',
            yLim=(0, 3.3))
scope.axes[0].attachSignal(name='Measured Voltage')

# Voltage scope
scope.addAxis(row=1,
            col=0,
            timeWindow=window,
            yLabel='Distance (m)',
            yLim=(0, 1))
scope.axes[1].attachSignal(name='Measured Distance (m)')
# endregion


# region: experiment constants
frequency = 200 # Hz
amplitude = 0
exponent = 0
# endregion


# region: experiment
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

with SensorsTrainer() as sensors:

    while timer.check():
        currentTime = timer.get_current_time()

        sensors.read_outputs()
        
        infrared = sensors.IRDistance

        distance = amplitude*np.power(infrared, exponent)
        print(f"Voltage: {infrared:.3f}     Distance (m): {distance:.3f}")
        scope.axes[0].sample(currentTime, infrared)
        scope.axes[1].sample(currentTime, distance)
        MultiScope.refreshAll()
        

        timer.sleep()

# endregion

input("Press Enter to close...")


