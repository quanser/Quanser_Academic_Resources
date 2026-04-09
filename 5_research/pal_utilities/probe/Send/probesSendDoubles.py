#-----------------------------------------------------------------------------#
# probeSendDoubles.py
#-----------------------------------------------------------------------------#
# This example demonstrates how to stream, receive, and display time series data
# using the probe and observer module.

# To run this example, 
# 1) open receive.py and comment out the code that opens other displays and 
# plots. Keep the code to open the scopes named "My Scope 1" and "My Scope 2"
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

# Initialize probe
probe = Probe(ip=IP_HOST)
probe.add_scope(numSignals=2, name='scope 1')
probe.add_scope(numSignals=2, name='scope 2')

rng = np.random.default_rng()     # non-deterministic random number generator

try:
    connected = False
    time.sleep(0.1)
    while elapsed_time() < TEST_TIME:
        if not probe.connected:
            probe.check_connection()

        if probe.connected:
            # Generate data samples
            a = rng.integers(-3, 3)
            b = np.sin(5*elapsed_time())
            c = np.cos(4*elapsed_time())
            d = np.sign(b)
            data_1 = np.array([a, d])
            data_2 = np.array([b, c])

            # send data
            sent_1 = probe.send(name='scope 1', scopeData=(elapsed_time(), data_1))
            sent_2 = probe.send(name='scope 2', scopeData=(elapsed_time(), data_2))
            if not (sent_1 or sent_2):
                break

            time.sleep(0.01)

except KeyboardInterrupt:
    print('User Interrupted!')
    pass

finally:
    # Terminate all displays
    probe.terminate()
