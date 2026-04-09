from .q_misc import Utilities
import numpy as np 

saturate = Utilities.saturate

def turn_speed_handling(speed_cmd, steering, enable=1):
    ''' This function implements a steering based speed reduction algorithm, to slow down the car when turning. \n
    
    INPUTS:
    speed_cmd - desired speed from user (m/s)
    steering - steering cmd (rad)
    enable - high (1) for enabled state, low (0) to disable. You can use this to programmatically disable speed reduction when at low speeds already.

    OUTPUTS:
    desired_speed - turn-based speed command (m/s)'''   

    gain = 1
    if enable:
        gain = saturate(np.cos(steering), 1, 0.5)

    return gain * speed_cmd