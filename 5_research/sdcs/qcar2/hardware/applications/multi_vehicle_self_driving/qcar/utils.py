import numpy as np
from quanser.common import Timeout
from pal.utilities.stream import BasicStream

class YOLOReceiver():
    def __init__(self,ip='localhost',nonBlocking=True,port="18666"):
        self.stopSign = np.zeros((7),dtype=np.float64)
        self.trafficlight = np.zeros((7),dtype=np.float64)
        self.cars = np.zeros((7),dtype=np.float64)
        self.yieldSign = np.zeros((7),dtype=np.float64)
        self.person = np.zeros((7),dtype=np.float64)

        self.uri='tcpip://'+ip+':'+port
        self._timeout = Timeout(seconds=0, nanoseconds=100000)
        self._handle = BasicStream(uri=self.uri,
                                    agent='C',
                                    receiveBuffer=np.zeros((5,7),
                                                           dtype=np.float64),
                                    recvBufferSize=7*5*8,
                                    nonBlocking=nonBlocking,
                                    reshapeOrder='C')
        self.status_check('', iterations=20)

    def status_check(self, message, iterations=10):
        # blocking method to establish connection to the server stream.
        self._timeout = Timeout(seconds=0, nanoseconds=10000) #1000000
        counter = 0
        while not self._handle.connected:
            self._handle.checkConnection(timeout=self._timeout)
            counter += 1
            if self._handle.connected:
                print(message)
                break
            elif counter >= iterations:
                print('YOLO Server error: status check failed.')
                break

    def read(self):
        new = False
        self._timeout = Timeout(seconds=0, nanoseconds=10)
        if self._handle.connected:
            new, bytesReceived = self._handle.receive(timeout=self._timeout, iterations=5)
            # print('read:',new, bytesReceived)
            # if new is True, full packet was received
            if new:
                self.stopSign[:] = self._handle.receiveBuffer[0,:]
                self.trafficlight[:] = self._handle.receiveBuffer[1,:]
                self.cars[:] = self._handle.receiveBuffer[2,:]
                self.yieldSign[:]= self._handle.receiveBuffer[3,:]
                self.person[:]= self._handle.receiveBuffer[4,:]
        else:
            self.status_check('Reconnected to yolo Server',iterations=1)
        return new

    def terminate(self):
        self._handle.terminate()
    
    def __enter__(self):
        """ Used for with statement. """
        return self
    
    def __exit__(self, type, value, traceback):
        """ Used for with statement. Terminates the YOLO receiver. """
        self.terminate()

class YOLOPublisher():
    def __init__(self,ip='localhost',nonBlocking=False,port="18666"):

        self.uri='tcpip://'+ip+':'+port
        self._timeout = Timeout(seconds=0, nanoseconds=100000)
        self._handle = BasicStream(uri=self.uri,
                                    agent='S',
                                    sendBufferSize=7*5*8,
                                    nonBlocking=nonBlocking,
                                    reshapeOrder='F')
        self.status_check('', iterations=20)

    def status_check(self, message, iterations=10):
        # blocking method to establish connection to the server stream.
        self._timeout = Timeout(seconds=0, nanoseconds=100000) #1000000
        counter = 0
        while not self._handle.connected:
            self._handle.checkConnection(timeout=self._timeout)
            counter += 1
            if self._handle.connected:
                print(message)
                break
            elif counter >= iterations:
                print('YOLO client error: status check failed.')
                break

    def send(self,yolodata):

        # data received flag
        new = False
        # 1 us timeout parameter
        self._timeout = Timeout(seconds=0, nanoseconds=100000)
        # set remaining packet to send
        self._sendPacket = yolodata
        # if connected to driver, send/receive
        if self._handle.connected:
            new = True
            self._handle.send(self._sendPacket)

        else:
            self.status_check('Reconnected to yolo client.')

        # if new is False, data is stale, else all is good
        return new

    def terminate(self):
        self._handle.terminate()

    def __enter__(self):
        """ Used for with statement. """
        return self
    
    def __exit__(self, type, value, traceback):
        """ Used for with statement. Terminates the YOLO publisher. """
        self.terminate()

class YOLODriveLogic():
    """
    YOLODriveLogic class implements the logic for processing YOLO predictions
    and determining the vehicle's velocity gain based on detected objects.
    
    Arguments:
        stopSignThreshold (float): Distance threshold for stop sign detection.
        trafficThreshold (float): Distance threshold for traffic light detection.
        carThreshold (float): Distance threshold for car detection.
        yieldThreshold (float): Distance threshold for yield sign detection.
        personThreshold (float): Distance threshold for person detection.
        pulseLength (int): Lengh of the pulse generated after detecting an object in number of frames.
    
    Methods:
        check_yolo(stopSign, trafficLight, QCar, yieldSign, person):
            Processes YOLO predictions and returns the velocity gain.
        stopSignPulse(stopSign):
            Handles stop sign detection logic.
        trafficPulse(trafficLight):
            Handles traffic light detection logic.
        yieldPulse(yieldSign):
            Handles yield sign detection logic.
        carPulse(car):
            Handles car detection logic.
        personPulse(person):
            Handles person detection logic.
    """
    def __init__(self,
                 stopSignThreshold = 0.6,
                 trafficThreshold = 1.7,
                 carThreshold = 0.3,
                 yieldThreshold = 1,
                 personThreshold = 0.6,
                 pulseLength = 300
                 ):
        self.counter = 0
        self.counter_yield = 0
        self.counter_traffic = 0
        self.counterStart_traffic = False
        self.counterStart = False
        self.counterStart_yield = False
        self.stopSignTrigger = 0
        self.carTrigger = 0
        self.trafficTrigger = 0
        self.yieldTrigger = 0
        self.personTrigger = 0
        self.vGain_person = 1
        self.vGain_yield = 1 
        self.vGain_stop = 1 
        self.vGain_car = 1 
        self.vGain = 1 
        self.stopSignThreshold = stopSignThreshold
        self.trafficThreshold = trafficThreshold
        self.carThreshold = carThreshold
        self.yieldThreshold = yieldThreshold
        self.personThreshold = personThreshold
        self.pulseLength = pulseLength

        self.carDist=100
        self.stopSignDist=100
        self.trafficLightDist=100
        self.yieldDist=100
        self.personDist=100


    def check_yolo(self,stopSign,trafficLight,QCar,yieldSign,person):
        ''' processes the YOLO predictions and returns the velocity gain.'''

        self.stopSignPulse(stopSign)
        self.trafficPulse(trafficLight)

        if self.stopSignTrigger == 1 or self.trafficTrigger == 1:
            self.vGain_stop = 0
            # return self.vGain

        self.carPulse(QCar)
        self.personPulse(person)
        # if self.carTrigger ==1 or self.personTrigger == 1:
        #     return self.vGain

        self.yieldPulse(yieldSign)
        if self.yieldTrigger ==1:
            self.vGain_yield = 0.5
            # return self.vGain
        
        self.vGain = min([self.vGain_yield,self.vGain_stop,self.vGain_car,self.vGain_person])
        self.vGain_yield = 1
        self.vGain_stop = 1
        self.vGain_car = 1
        self.vGain_person = 1
        return self.vGain
    
    def stopSignPulse(self,stopSign):
        ''' If a stop sign is closer than the threshold, a pulse with the length
        of self.pulseLength is generated, reducing the velocity gain to 0 for the 
        during of the pulse. After the pulse, the detection for stop sign is paused 
        for half the pulse time.'''

        stopSignCount = stopSign[0]
        stopSign[np.isnan(stopSign)]=10
        if stopSignCount>0:
            self.stopSignDist = stopSign[1:][stopSign[1:]!=0].min()
        else:
            self.stopSignDist=100
        if not self.counterStart:
            if stopSignCount>0 \
                and self.stopSignDist<self.stopSignThreshold:
                self.counterStart=True
                self.stopSignTrigger=1
            else:
                self.counterStart=False
                self.stopSignTrigger=0
        else:
            self.counter+=1
            if self.counter < self.pulseLength:
                self.stopSignTrigger = 1
            elif self.counter < self.pulseLength+int(self.pulseLength/2):
                self.stopSignTrigger = 0
            else:
                self.counter = 0
                self.counterStart = False
                self.stopSignTrigger = 0

    
    def trafficPulse(self,trafficLight):
        ''' If a red traffic light is closer than the threshold, a pulse with the length
        of self.pulseLength/6 is generated, reducing the velocity gain to 0 for the 
        during of the pulse. '''

        trafficLightCount = trafficLight[0]
        trafficLight[np.isnan(trafficLight)]=10

        if trafficLightCount>0:
            self.trafficLightDist = trafficLight[1:][trafficLight[1:]!=0].min()
        else:
            self.trafficLightDist=100
            self.trafficTrigger=0

        if not self.counterStart_traffic:
            if trafficLightCount>0 \
                and self.trafficLightDist<self.trafficThreshold \
                    and self.trafficLightDist> self.trafficThreshold - 0.6:
                self.trafficTrigger=1
                self.counterStart_traffic=True
            else:
                self.counterStart_traffic=False
                self.trafficTrigger=0
        else:
            self.counter_traffic+=1
            if self.counter_traffic < int(self.pulseLength/6):
                self.trafficTrigger = 1
            else:
                self.counter_traffic = 0
                self.counterStart_traffic = False
    
    def yieldPulse(self,yieldSign):
        ''' If a yeild sign is closer than the threshold, a pulse with the length
        of self.pulseLength is generated, reducing the velocity gain to 0.5 for the 
        during of the pulse. '''

        yieldSignCount = yieldSign[0]
        yieldSign[np.isnan(yieldSign)]=10
        if yieldSignCount>0:
            self.yieldDist = yieldSign[1:][yieldSign[1:]!=0].min()
        else:
            self.yieldDist=100
            self.yieldTrigger=0
        
        if not self.counterStart_yield:
            if yieldSignCount>0 \
                and self.yieldDist<self.yieldThreshold:
                self.counterStart_yield=True
                self.yieldTrigger=1
            else:
                self.counterStart_yield=False
                self.yieldTrigger=0
        else:
            self.counter_yield+=1
            if self.counter_yield < self.pulseLength:
                self.yieldTrigger = 1
            else:
                self.counter_yield = 0
                self.counterStart_yield = False

    def carPulse(self, car):
        ''' If a car is closer than the threshold, the velocity gain will be
        reduced to a value between 0 and 1, depending on the distance to the car.
        The speed will start decresing at the distance of 1.2, and will be 0
        at the distance of se;f.carThreshold.'''

        carCount = car[0]
        detect_threshold = 1.2
        car[np.isnan(car)]=10
        if carCount>0:
            self.carDist = car[1:][car[1:]!=0].min()
        else:
            self.carDist=100
            self.carTrigger=0
        if carCount>0 \
            and self.carDist<detect_threshold:
            self.carTrigger=1
            m=1/(detect_threshold-self.carThreshold)
            b=-m*self.carThreshold
            self.vGain_car = np.clip(m*self.carDist+b,0,1)
        else:
            self.carTrigger=0
    
    def personPulse(self, person):
        ''' If a person is closer than the threshold, the velocity gain will be
        reduced to a value between 0 and 1, depending on the distance to the car.
        The speed will start decresing at the distance of 1.5, and will be 0
        at the distance of self.personThreshold.'''

        personCount = person[0]
        detect_threshold = 1.5
        person[np.isnan(person)]=10
        if personCount>0:
            self.personDist = person[1:][person[1:]!=0].min()
        else:
            self.personDist=100
            self.personTrigger=0
        if personCount>0 \
            and self.personDist<detect_threshold:
            self.personTrigger=1
            m=1/(detect_threshold-self.personThreshold)
            b=-m*self.personThreshold
            self.vGain_person = np.clip(m*self.personDist+b,0,1)
        else:
            self.personTrigger=0
