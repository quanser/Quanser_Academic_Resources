# region: system imports
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.scope import MultiScope
# endregion 

# region: observer definition 
simulationTime = 10 # will run for this amount of seconds

scope = MultiScope(rows= 1, cols =1,
            title='Voltage Measurement',
            fps=60 )

# Voltage scope
window = simulationTime
scope.addAxis(row=0,
            col=0,
            timeWindow=window,
            yLabel='Voltage (V)',
            yLim=(0, 3.3))
scope.axes[0].attachSignal(name='Measured voltage')


# endregion


# region: experiment constants
frequency = 200 # Hz
counter = 0
# endregion


# region: experiment
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

with SensorsTrainer() as sensors:

    while timer.check():
        currentTime = timer.get_current_time()

        sensors.read_outputs()
        
        infrared = sensors.IRDistance

        scope.axes[0].sample(currentTime, infrared)
        MultiScope.refreshAll()
        

        timer.sleep()
input("Press Enter to exit...")
# endregion



