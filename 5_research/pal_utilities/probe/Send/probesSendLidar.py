#-----------------------------------------------------------------------------#
# probeSendLidar.py
#-----------------------------------------------------------------------------#
# This example demonstrates how to stream, receive, and display randomly 
# generated LiDAR data in a polar plot

# To run this example, 
# 1) open receive.py and comment out the code to open other displays, plots, and
# scopes. Keep the code to open the plot named "My Lidar 1"
# 2) run receive.py  
# 3) run this script (use a separate terminal if running both scripts on the 
#   same machine)

from pal.utilities.probe import Probe
import time
import numpy as np

start = time.time()
def elapsed_time():
    return time.time() - start

IP_HOST = 'localhost'
TEST_TIME = 10 # seconds
displays = []

# Initialize probe
probe = Probe(ip=IP_HOST)
probe.add_plot(numMeasurements=1680, name='my plot')
ranges = np.ones((1680), dtype=np.float32)
angles = np.linspace(0, 2*np.pi-(2*np.pi/1680), 1680, endpoint=False, dtype=np.float32)

rng = np.random.default_rng()     # non-deterministic random number generator


try:
    time.sleep(0.1)
    while elapsed_time() < TEST_TIME:
        if not probe.connected:
            probe.check_connection()

        if probe.connected:
            
            mag = rng.integers(1, 3)
            ranges_s = (mag*ranges).astype(np.float32) # convert
            
            sent = probe.send(name='my plot', lidarData=(ranges_s, angles))
            if not sent:
                break

            time.sleep(0.1)

except KeyboardInterrupt:
    print('User Interrupted!')
    pass

finally:
    # Terminate all displays
    probe.terminate()
