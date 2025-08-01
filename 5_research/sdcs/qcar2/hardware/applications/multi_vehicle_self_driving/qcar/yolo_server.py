import numpy as np
import time
import cv2
from pit.YOLO.nets import YOLOv8
from pit.YOLO.utils import QCar2DepthAligned
from pal.utilities.probe import Probe

from utils import YOLOPublisher
import argparse

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Collect command line arguments
parser = argparse.ArgumentParser(prog='Vehicle control')
parser.add_argument('-i','--ip_host', default='192.168.2.10')
parser.add_argument('-p','--probing', default="False")
parser.add_argument('-w','--width', default=320, help="wide of to image to be displayed in the observer")
parser.add_argument('-ht','--height', default=200, help="height of to image to be displayed in the observer")
args = parser.parse_args()
ipHost = args.ip_host
probing = args.probing=="True"
width = int(args.width)
height = int(args.height)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Instantiate YOLOv8 model
imageWidth  = 640
imageHeight = 480
myYolo  = YOLOv8(
                 # modelPath = 'path/to/model', 
                 imageHeight= imageHeight,
                 imageWidth = imageWidth,
                )

# Initialize Depth/RGB alignment RT model, YOLO server, and probe
QCarImg = QCar2DepthAligned(port='18777')
YOLOserver = YOLOPublisher(port='18666')
if probing:
    probe = Probe(ip = ipHost)
    probe.add_display(imageSize = [height, width, 3], name='YOLO Image',scalingFactor =1)
probe_count = 0

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Main loop for YOLO server
try:
    while True:
        # Instantiate YOLO prediction send buffers
        stopSignBuffers = np.zeros((7),dtype=np.float64)
        trafficBuffers = np.zeros((7),dtype=np.float64)
        carBuffer = np.zeros((7),dtype=np.float64)
        yieldBuffer = np.zeros((7),dtype=np.float64)
        personBuffer = np.zeros((7),dtype=np.float64)
        
        # Get aligned RGB and Depth images
        QCarImg.read()
            
        # Get YOLO predictions and post-process results
        rgbProcessed = myYolo.pre_process(QCarImg.rgb)
        predecion = myYolo.predict(inputImg = rgbProcessed,
                                   classes = [0,2,9,11,33],
                                   confidence = 0.4,
                                   half = True,
                                   verbose = False
                                   )
        processedResults=myYolo.post_processing(alignedDepth = QCarImg.depth,
                                                clippingDistance = 10)
        annotatedImg=myYolo.post_process_render(showFPS = True)
        
        # Resize the annotated image and send to observer if probing is enabled
        if probing and probe_count%2 == 0:
            probe.check_connection()
            if probe.connected:
                resizedImg = cv2.resize(annotatedImg, (width, height))
                probe.send(name='YOLO Image', imageData=resizedImg)
        probe_count += 1

        # process the prediction results and send to vehicle control server
        stopSignCount=0
        trafficCount=0
        carCount=0
        yieldCount=0
        personCount = 0
        if len(processedResults)>0:
            for i in processedResults:
                # print(i.name)
                if 'car' in i.name:
                    carBuffer[carCount+1]=i.distance
                    carCount+=1
                elif 'stop sign' in i.name:
                    stopSignBuffers[stopSignCount+1]=i.distance
                    stopSignCount+=1
                elif 'red' in i.name:
                    trafficBuffers[trafficCount+1]=i.distance
                    trafficCount+=1
                elif 'yield' in i.name:
                    yieldBuffer[yieldCount+1]=i.distance
                    yieldCount+=1
                elif 'person' in i.name:
                    if personCount <= 5:
                        personBuffer[personCount+1]=i.distance
                    personCount+=1
        carBuffer[0] = carCount
        trafficBuffers[0] = trafficCount
        stopSignBuffers[0] = stopSignCount
        yieldBuffer[0] = yieldCount
        personBuffer[0] = personCount
        sendPacket = np.vstack((stopSignBuffers,trafficBuffers,carBuffer,yieldBuffer,personBuffer))
        YOLOserver.send(sendPacket)

except KeyboardInterrupt:
    print("User interrupted!")
    
finally:
    QCarImg.terminate()
    if probing:
        probe.terminate()

