# LCD - LCD input
# Understanding how to read the LCD and 
# the type of information we get from touch data.
# For example on how to draw to the LCD, see test_draw_modes.py located in 
# 6_teaching/2_Mechatronics/sensors_trainer/1_fundamentals/lcd_input/hardware/python/test_draw_modes.py

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






