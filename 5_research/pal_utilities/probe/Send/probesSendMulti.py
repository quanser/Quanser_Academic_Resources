from pal.utilities.probe import Probe
import time
import numpy as np
import cv2

start = time.time()
def elapsed_time():
    return time.time() - start

# Initialize data to be sent
imageWidth, imageHeight, imageChannels = 640, 480, 3
ip_host = 'localhost'
img = cv2.imread('test.png')
ranges = np.ones((1680), dtype=np.float32)
angles = np.linspace(0, 2*np.pi-(2*np.pi/1680), 1680, endpoint=False, dtype=np.float32)
a_prev, counter = elapsed_time(), 0
sending_0, sending_1, sending_2, sending_3, sending_4, sending_5 = 1, 1, 1, 1, 1, 1

# Initialize probes
probe = Probe(ip=ip_host)
probe.add_display(imageSize = [imageHeight,imageWidth,imageChannels],
                  scaling = True, scalingFactor = 2, name='large image')
probe.add_display(imageSize = [imageHeight,imageWidth,imageChannels],
                  scaling = True, scalingFactor = 4, name='small image')
probe.add_plot(numMeasurements=1680, name='big lidar')
probe.add_plot(numMeasurements=1680, name='small lidar')
probe.add_scope(numSignals=2, name='scope 1')
probe.add_scope(numSignals=2, name='scope 2')

try:
    time.sleep(0.1)
    while True:
        if not probe.connected:
            probe.check_connection()

        if probe.connected:
            # send lidar data
            mag = elapsed_time()%2
            ranges_s = mag*ranges
            if counter%10 == 0:
                sending_0 = probe.send('big lidar', lidarData=(ranges_s, angles))
                sending_1 = probe.send('small lidar', lidarData=(ranges_s, angles))

            # send scope data
            a = elapsed_time()%2
            b = np.sin(5*elapsed_time())
            c = np.cos(4*elapsed_time())
            d = np.sign(b)
            data_1 = np.array([a, d])
            data_2 = np.array([b, c])
            sending_2 = probe.send('scope 1', scopeData=(elapsed_time(), data_1))
            sending_3 = probe.send('scope 2', scopeData=(elapsed_time(), data_2))

            # send image data
            if counter%3 == 0:
                sending_4 = probe.send('large image', imageData=img)
            if a < a_prev:
                img = np.flip(img, 0)
            if counter%3 == 0:
                sending_5 = probe.send('small image', imageData=img)
            print(sending_0, sending_1, sending_2, sending_3, sending_4, sending_5)
            if not (sending_0 or sending_1 or sending_2 or sending_3 or sending_4 or sending_5):
                break
            a_prev = a
            counter += 1
            time.sleep(0.01)

except KeyboardInterrupt:
    print('User Interrupted!')
    pass

finally:
    probe.terminate()
