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
probe.add_plot(numMeasurements=1680, name='my plot')
ranges = np.ones((1680), dtype=np.float32)
angles = np.linspace(0, 2*np.pi-(2*np.pi/1680), 1680, endpoint=False, dtype=np.float32)

connectionSuccessful = False
t_prev = time.time()
try:
    connected = False
    time.sleep(0.1)
    while True:
        if not probe.connected:
            probe.check_connection()

        if probe.connected:
            mag = np.random.randint(1, 3)
            ranges_s = mag*ranges
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
