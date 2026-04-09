#-----------------------------------------------------------------------------#
# probeSendXY.py
#-----------------------------------------------------------------------------#
# This example demonstrates how to stream, receive, and display real-time XY 
# data using probe/observer module 

# To run this example, 
# 1) run receive.py 
# 2) run this script (use a separate terminal if running both scripts on the 
#   same machine)


from pal.utilities.probe import Probe
import time
import numpy as np

start = time.time()
def elapsed_time():
    return time.time() - start

IP_HOST = 'localhost'
TEST_TIME = 10 # seconds

# Initialize probes
probe = Probe(ip=IP_HOST)
probe.add_xy_scope(numSignals=2, name='XY scope')

try:
    time.sleep(0.1)
    while elapsed_time() < TEST_TIME:
        if not probe.connected:
            probe.check_connection()

        if probe.connected:

            t = elapsed_time()
            # Generate data sample
            x = np.log(t+1) * np.cos(t*np.pi)
            y = np.log(t+1) * np.sin(t*np.pi)

            # send data 
            sent = probe.send('XY scope', xyData=(elapsed_time(), [[x-1, y-1],
                                                                   [y+1, x+1]]))

            if not (sent):
                break
            
            time.sleep(0.01)

except KeyboardInterrupt:
    print('User Interrupted!')
    pass

finally:
    probe.terminate()