#-----------------------------------------------------------------------------#
# probeSendMulti.py
#-----------------------------------------------------------------------------#
# This example demonstrates how to stream, receive, and display data using 
# probe and observer module that includes support for Displays (for video data), 
# Plots (standard polar plot as an image), Scope (standard time series plotter), 
# and XY Scope(Real-time display of 2D signals)  

# To run this example, 
# 1) open receive.py and make sure that all code to open displays, plots, 
# scopes, and an xy scope is uncommented
# 2) run receive.py  
# 3) go to the directory containing this script and run the script (use a 
#  separate terminal if running both scripts on the same machine)

from pal.utilities.probe import Probe
import time
import numpy as np
import cv2

start = time.time()
def elapsed_time():
    return time.time() - start

# Initialize data to be sent
IMAGE_WIDTH, IMAGE_HEIGHT, IMAGE_CHANNELS = 640, 480, 3
IP_HOST = 'localhost'
img = cv2.imread('test.png')
ranges = np.ones((1680), dtype=np.float32)
angles = np.linspace(0, 2*np.pi-(2*np.pi/1680), 1680, endpoint=False, dtype=np.float32)
a_prev, counter = elapsed_time(), 0
sending_0, sending_1, sending_2, sending_3, sending_4, sending_5, sending_6 = 1, 1, 1, 1, 1, 1, 1

# Initialize probes
TEST_TIME = 10 # seconds

probe = Probe(ip=IP_HOST)
probe.add_display(imageSize = [IMAGE_HEIGHT,IMAGE_WIDTH,IMAGE_CHANNELS],
                  scaling = True, scalingFactor = 2, name='large image')
probe.add_display(imageSize = [IMAGE_HEIGHT,IMAGE_WIDTH,IMAGE_CHANNELS],
                  scaling = True, scalingFactor = 4, name='small image')
probe.add_plot(numMeasurements=1680, name='big lidar')
probe.add_plot(numMeasurements=1680, name='small lidar')
probe.add_scope(numSignals=2, name='scope 1')
probe.add_scope(numSignals=2, name='scope 2')
probe.add_xy_scope(numSignals=2, name='XY scope')

try:
    time.sleep(0.1)
    while elapsed_time() < TEST_TIME:
        if not probe.connected:
            probe.check_connection()

        if probe.connected:

            # generate lidar data sample
            mag = elapsed_time()%2
            ranges_s = mag*ranges
            if counter%10 == 0:
                # send lidar data
                sending_0 = probe.send('big lidar', lidarData=(ranges_s, angles))
                sending_1 = probe.send('small lidar', lidarData=(ranges_s, angles))

            # generate scope data
            a = elapsed_time()%2
            b = np.sin(5*elapsed_time())
            c = np.cos(4*elapsed_time())
            d = np.sign(b)
            data_1 = np.array([a, d])
            data_2 = np.array([b, c])
            # send scope data
            sending_2 = probe.send('scope 1', scopeData=(elapsed_time(), data_1))
            sending_3 = probe.send('scope 2', scopeData=(elapsed_time(), data_2))

            # send image data
            if counter%3 == 0:
                sending_4 = probe.send('large image', imageData=img)
            if a < a_prev:
                img = np.flip(img, 0)
            if counter%3 == 0:
                sending_5 = probe.send('small image', imageData=img)

            # generate XY data sample
            t = elapsed_time()
            x = np.log(t+1) * np.cos(t*np.pi)
            y = np.log(t+1) * np.sin(t*np.pi)
            # send XY data
            sending_6 = probe.send('XY scope', xyData=(elapsed_time(), [[x+1, y+1],
                                                                        [y-1, x-1]]))

            # print(sending_0, sending_1, sending_2, sending_3, sending_4, sending_5, sending_6)
            if not (sending_0 or sending_1 or sending_2 or sending_3 or sending_4 or sending_5 or sending_6):
                break
            a_prev = a
            counter += 1
            time.sleep(0.01)

except KeyboardInterrupt:
    print('User Interrupted!')
    pass

finally:
    probe.terminate()
