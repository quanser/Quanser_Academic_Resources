# LCD - LCD input
# Exploring how to plot the LCD touch information. 

# region: Python level imports
from threading import Thread
import signal
import time
import numpy as np
from pal.products.sensors import SensorsTrainer, SensorsDisplay
from pal.utilities.scope import MultiScope, XYScope
from pal.utilities.timing import Timer
# endregion 

plotTouch = False  # Set to True to enable XY Scope to show touch input

#region: Scope update
def update_plot(timeStamp, sensors, touch):
    if plotTouch:
        finger1 = ([touch.fingers[0].c, touch.fingers[0].r] 
               if touch.num_fingers > 0 else [np.nan, np.nan])
        finger2 = ([touch.fingers[1].c, touch.fingers[1].r] 
                   if touch.num_fingers>1 else [np.nan, np.nan])
        finger3 = ([touch.fingers[2].c, touch.fingers[2].r] 
                   if touch.num_fingers>2 else [np.nan, np.nan])

        xy_plot.sample(timeStamp,[finger1, finger2, finger3])

        if sensors.buttons[0]:
            xy_plot.clear()
# endregion
    
# region: Experiment constants
simulationTime = 300 # will run for this amount of seconds
frequency = 200 # Hz
         
squareSize = 5
# Define colors as BGR tuples and generate squares
#heightxwidthx3
color1 = (176, 114, 76)   # blue
colorSquare1 = np.full((squareSize, squareSize, 3), color1, dtype=np.uint8)

color2 = (104, 168, 85)   # green
colorSquare2 = np.full((squareSize, squareSize, 3), color2, dtype=np.uint8)

color3 = (86, 217, 248)   # yellow
colorSquare3 = np.full((squareSize, squareSize, 3), color3, dtype=np.uint8)
#endregion

# region: Main Loop
def control_loop():
    # these variables cannot be global since they will be modified in the loop
    counterScope = 0
    image  = np.zeros([490,810,3], dtype=np.uint8)
    mask  = np.zeros([490,810,1], dtype=np.uint8)

    timer = Timer(sampleRate=frequency, totalTime=simulationTime)
    
    print("Touch input ready. Waiting for touch input...")
    
    with (SensorsTrainer() as sensors, 
          SensorsDisplay() as lcd):
        
        while timer.check() and not KILL_THREAD:
            currentTime = timer.get_current_time()

            # Read sensor information
            sensors.read_outputs()
            new, touch = lcd.read_touch()

            if new and touch.num_fingers>0: 
                finger1 = touch.fingers[0]
                image[finger1.r:finger1.r+squareSize,
                        finger1.c:finger1.c+squareSize,:] = colorSquare1
                mask[finger1.r:finger1.r+squareSize,
                        finger1.c:finger1.c+squareSize,0] = 255

                if touch.num_fingers>1:
                    finger1 = touch.fingers[1]
                    image[finger1.r:finger1.r+squareSize,
                            finger1.c:finger1.c+squareSize,:] = colorSquare2
                    mask[finger1.r:finger1.r+squareSize,
                        finger1.c:finger1.c+squareSize,0] = 255
        
                if touch.num_fingers>2:
                    finger1 = touch.fingers[2]
                    image[finger1.r:finger1.r+squareSize,
                          finger1.c:finger1.c+squareSize,:] = colorSquare3
                    mask[finger1.r:finger1.r+squareSize,
                        finger1.c:finger1.c+squareSize,0] = 255

            # 10 times a second draw image and restart image and mask
            if np.mod(counterScope,frequency/10) == 0:
                lcd.draw_image_blend(image, mask)
                image  = np.zeros([490,810,3], dtype=np.uint8)
                mask  = np.zeros([490,810,1], dtype=np.uint8)

            # if plotTouch, update plot every 5 counts
            if np.mod(counterScope,5) == 0 and plotTouch:
                update_plot(currentTime, sensors, touch)
            
            if sensors.buttons[0]:
                lcd.clear()

            counterScope += 1

            timer.sleep()
# endregion


#region: Scope setup
def setupTouchScope():
    xyScope = XYScope(
        title="XYScope Touch",
        xLabel='Horizontal Location',
        yLabel='Vertical Location',
        xLim=(0, 800),
        yLim=(0, 480)
    )
    xyScope.attachSignal(color=[76,114,176], width=5, lineStyle=':', name = 'Touch 0')
    xyScope.attachSignal(color=[85,168,104], width=5, lineStyle=':', name = 'Touch 1')
    xyScope.attachSignal( color=[248,217,86], width=5, lineStyle=':', name = 'Touch 2')

    return xyScope

    
if plotTouch:
    xy_plot = setupTouchScope()
# endregion

#region: Threading setup

# Setup to enable killing the data generation thread using keyboard interrupts
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)

# Setup data generation thread and run until complete
thread = Thread(target=control_loop)
thread.start()

while thread.is_alive() and (not KILL_THREAD):

    # This must be called regularly or the scope windows will freeze
    # Must be called in the main thread.
    if plotTouch:
        MultiScope.refreshAll()
        XYScope.refreshAll()
    time.sleep(0.01)

# endregion
