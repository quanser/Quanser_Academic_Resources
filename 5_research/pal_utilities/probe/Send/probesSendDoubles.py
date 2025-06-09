from pal.utilities.probe import Probe
import time
import numpy as np
import cv2

start = time.time()
def elapsed_time():
    return time.time() - start

# Image Parameters
imageWidth = 640
imageHeight = 480
imageChannels = 3

ip_host = 'localhost'
displays = []

probe = Probe(ip=ip_host)
probe.add_scope(numSignals=4, name='my scope')

connectionSuccessful = False
t_prev = time.time()
try:
    connected = False
    time.sleep(0.1)
    while True:
        if not probe.connected:
            # print('Not connected')
            probe.check_connection()

        if probe.connected:
            a = np.random.randint(-3, 3)
            b = np.sin(5*elapsed_time())
            c = np.cos(4*elapsed_time())
            d = np.sign(b)
            data = np.array([a, b, c, d])
            sent = probe.send(name='my scope', scopeData=(elapsed_time(), data))
            if not sent:
                break

            time.sleep(0.1)

except KeyboardInterrupt:
    print('User Interrupted!')
    pass

finally:
    # Terminate all displays
    probe.terminate()
