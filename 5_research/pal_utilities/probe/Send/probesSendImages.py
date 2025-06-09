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
probe.add_display(imageSize = [imageHeight,imageWidth,imageChannels],
                  scaling = True,
                  scalingFactor = 2,
                  name = 'my display')

img = cv2.imread('test.png')

connectionSuccessful = False
t_prev = time.time()
try:
    connected = False
    time.sleep(0.1)
    while True:
        if not probe.connected:
            probe.check_connection()

        if probe.connected:
            cv2.imshow('Window', img)
            cv2.waitKey(33)
            sent = probe.send(name='my display', imageData=img)
            if not sent:
                break

            # time.sleep(0.033)

except KeyboardInterrupt:
    print('User Interrupted!')
    pass

finally:
    # Terminate all displays
    probe.terminate()
