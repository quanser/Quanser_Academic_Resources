# LCD - LCD input
# Understanding how to read the LCD and 
# the type of information we get from touch data.

# region: Python level imports
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer, SensorsDisplay
# endregion 


# region: Experiment constants
simulationTime = 500 # will run for this amount of seconds
frequency = 300 # Hz
singleFinger = True

counterHalfSec = 0 # counter for printing
# endregion


# region: Main Loop
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

with SensorsTrainer() as sensors, SensorsDisplay() as lcd:

    print("Touch input ready. Waiting for touch input...")
    while timer.check():
        
        currentTime = timer.get_current_time()

        sensors.read_outputs()
        new, touch = lcd.read_touch()
    
        if counterHalfSec >= frequency/2:
            if singleFinger:
                # keep trying until new is high, then restart counter
                if new and touch.num_fingers>0:
                    print(f'finger ID: {touch.fingers[0].id} ',
                          f'Column: {touch.fingers[0].c} ',
                          f'Row: {touch.fingers[0].r}')
                    
                    counterHalfSec = 0

            else:
                # keep trying until new is high, then restart counter
                if new and touch.num_fingers>0:
                    for x in range(touch.num_fingers):
                        print(f'finger ID: {touch.fingers[x].id} ',
                              f'Column: {touch.fingers[x].c} ',
                              f'Row: {touch.fingers[x].r}  | ', 
                              end = "")
                    print(' ')
            
                    counterHalfSec = 0
    
        counterHalfSec += 1
        timer.sleep()
# endregion






