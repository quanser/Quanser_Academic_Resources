from pal.utilities.stream import BasicStream
from threading import Thread
try:
    from quanser.common import Timeout
except:
    from quanser.communications import Timeout
import cv2
import numpy as np
import sys
from pal.utilities.scope import Scope, MultiScope, XYScope

class Probe():
    '''Class object to send data to a remote Observer.
    Includes support for Displays (for video data), Plots (standard polar
    plot as an image) and Scope (standard time series plotter).'''

    def __init__(self,
                 ip = 'localhost'):

        self.remoteHostIP = ip
        self.agents = dict()
        self.agentType = []
        # agentType =>  0 Video Display
        #               1 Polar Plot
        #               2 Scope
        self.numDisplays = 0
        self.numPlots = 0
        self.numScopes = 0
        self.connected = False

    def add_display(self,
            imageSize = [480,640,3],
            scaling = True,
            scalingFactor = 2,
            name = 'display'
        ):

        self.numDisplays += 1
        _display = RemoteDisplay(ip = self.remoteHostIP,
            id = self.numDisplays,
            imageSize = imageSize,
            scaling = scaling,
            scalingFactor = scalingFactor
            )

        if name == 'display':
            name = 'display_'+str(self.numDisplays)
        # agent type => 0
        self.agents[name] = (_display, 0)

        return True

    def add_plot(self,
            numMeasurements = 1680,
            scaling = True,
            scalingFactor = 2,
            name = 'plot'
        ):
        self.numPlots += 1
        _plot = RemotePlot(ip = self.remoteHostIP,
                           numMeasurements=numMeasurements,
                           id=self.numPlots,
                           scaling = scaling,
                           scalingFactor = scalingFactor)

        if name == 'plot':
            name = 'plot_'+str(self.numDisplays)
        # agent type => 1
        self.agents[name] = (_plot, 1)

        return True

    def add_scope(self,
            numSignals = 1,
            name = 'scope'
        ):
        self.numScopes += 1

        _scope = RemoteScope(numSignals=numSignals, id=self.numScopes, ip=self.remoteHostIP)

        if name == 'scope':
            name = 'scope_'+str(self.numDisplays)
        # agent type => 2
        self.agents[name] = (_scope, 2)

        return True

    def check_connection(self):
        '''Attempts to connect every unconnected probe in the agentList.
        Returns True if every probe is successfully connected.'''
        self.connected = True

        for key in self.agents:
            if not self.agents[key][0].connected:
                self.agents[key][0].check_connection()
            self.connected = self.connected and self.agents[key][0].connected
        return self.connected

    def send(self, name,
             imageData=None,
             lidarData=None,
             scopeData=None):
        '''Ensure that at least one of imageData, lidarData, scopeData is provided,
        and that the type of data provided matches the expected name, otherwise an
        error message is printed and the method returns False.

        imageData => numpy array conforming to imageSize used in display definition \n
        lidarData => (ranges, angles) tuple, where ranges and angles are numpy arrays conforming to numMeasurements used in plot definition \n
        scopeData => (time, data) tuple, with data being a numpy array conforming to numSignals used in scope definition and time is the timestamp \n
        '''

        flag = False
        agentType = self.agents[name][1]
        if agentType == 0:
            if imageData is None:
                print("Image data not provided for a display agent.")
            else:
                flag = self.agents[name][0].send(imageData)
        elif agentType == 1:
            if lidarData is None:
                print("Lidar data not provided for a plot agent.")
            else:
                flag = self.agents[name][0].send(distances=lidarData[0], angles=lidarData[1])
        elif agentType == 2:
            if scopeData is None:
                print("Scope data not provided for a scope agent")
            else:
                flag = self.agents[name][0].send(scopeData[0], data=scopeData[1])

        return flag

    def terminate(self):
        for key in self.agents:
            self.agents[key][0].terminate()

class ObserverAgent():
    def __init__(self, uriAddress, id, bufferSize, buffer, agentType, properties):

        self.server = BasicStream(uriAddress, agent='S',
                                  recvBufferSize=bufferSize,
                                  receiveBuffer=buffer,
                                  nonBlocking=False)
        self.id = id
        self.buffer = buffer
        self.bufferSize = bufferSize
        self.agentType = agentType
        # agentType =>  0 Video Display
        #               1 Polar Plot
        #               2 Scope
        self.properties = properties
        self.connected = self.server.connected
        self.timeout = Timeout(seconds=0, nanoseconds=1000000)
        self.counter = 0

        self.name = properties['name']
        if self.agentType == 0:
            self.imageSize = self.properties['imageSize']
            self.scalingFactor = self.properties['scalingFactor']
            # return True
        elif self.agentType == 1:
            self.numMeasurements = self.properties['numMeasurements']
            self.frameSize = self.properties['frameSize']
            self.pixelsPerMeter = self.properties['pixelsPerMeter']
            self.distances = np.zeros((self.numMeasurements,1), dtype=np.float32)
            self.angles = np.zeros((self.numMeasurements,1), dtype=np.float32)
            # return True
        elif self.agentType == 2:
            self.numSignals=self.properties['numSignals']
            self.signalNames=self.properties['signalNames']
            self.timeWindow = 10
            self.refreshWindow = self.timeWindow
            self.timer_bias = 0
            self.scope = Scope(
                title=self.name,
                timeWindow=self.timeWindow,
                xLabel='Time (s)',
                yLabel='Data'
            )
            if self.signalNames is None:
                for i in range(self.numSignals):
                    self.scope.attachSignal(name='signal_'+str(i+1))
            else:
                for i in range(self.numSignals):
                    self.scope.attachSignal(name=self.signalNames[i])
            # return True
        # else:
            # return False

    def receive(self):
        recvFlag = False
        exitCondition = False
        if self.server.connected:
            recvFlag, bytesReceived = self.server.receive(
                iterations=2, timeout=self.timeout)
            # add some sort of compression
            if recvFlag:
                self.counter = 1
            if not recvFlag:
                self.counter += 1
            if self.counter >= 1000:
                exitCondition = True
        return recvFlag, exitCondition

    def process(self):
        if self.agentType == 0:
            cv2.imshow(self.name, self.server.receiveBuffer)
            return True
        elif self.agentType == 1:
            self.distances = self.server.receiveBuffer[:,0]
            self.angles = self.server.receiveBuffer[:,1]
            image_lidar = np.zeros((self.frameSize, self.frameSize), dtype=np.uint8)
            offset = np.int16(self.frameSize/2)
            x = np.int16(np.clip(offset - self.pixelsPerMeter * self.distances * np.cos(self.angles), 0, self.frameSize-1))
            y = np.int16(np.clip(offset - self.pixelsPerMeter * self.distances * np.sin(self.angles), 0, self.frameSize-1))
            image_lidar[x, y] = np.uint8(255)
            cv2.imshow(self.name, image_lidar)
            return True
        elif self.agentType == 2:
            self.data = self.server.receiveBuffer[1:]
            self.scope.sample(self.server.receiveBuffer[0], list(self.data))
            return True
        else:
            return False

    def check_connection(self):
        '''Checks if the sendCamera object is connected to its server. returns True or False.'''

        # First check if the server was connected.
        self.server.checkConnection(timeout=self.timeout)
        self.connected = self.server.connected

    def terminate(self):
        '''Terminates the connection.'''
        self.server.terminate()

class Observer():
    '''Class object to send data to a remote Observer.
    Includes support for Displays (for video data), Plots (standard polar
    plot as an image) and Scope (standard time series plotter).'''

    def __init__(self):

        self.agentList = []
        self.numDisplays = 0
        self.numPlots = 0
        self.numScopes = 0
        self.agentThreads = []

    def add_display(self, imageSize = [480,640,3], scalingFactor = 2, name = None):

        if scalingFactor < 1:
            scalingFactor == 1
        scaling = scalingFactor > 1

        if (scaling and
            (imageSize[0] % scalingFactor != 0 or
            imageSize[1] % scalingFactor != 0)):
            sys.exit('Select a scaling factor that is a factor of both width and height of image')

        if scaling:
            imageSize[0] = int(imageSize[0]/scalingFactor)
            imageSize[1] = int(imageSize[1]/scalingFactor)

        self.counter = 0
        bufferSize = np.prod(imageSize)
        self.numDisplays += 1
        port = 18800+self.numDisplays
        uriAddress  = 'tcpip://localhost:' + str(port)

        if name == None:
            name = 'Display '+str(self.numDisplays)

        properties = dict()
        properties['imageSize'] = [imageSize[0],imageSize[1],imageSize[2]]
        properties['scalingFactor'] = scalingFactor
        properties['name'] = name

        display = ObserverAgent(uriAddress=uriAddress,
                                id=self.numDisplays,
                                bufferSize=bufferSize,
                                buffer=np.zeros((imageSize[0], imageSize[1], imageSize[2]), dtype=np.uint8),
                                agentType=0,
                                properties=properties)

        self.agentList.append(display)

        return True

    def add_plot(self, numMeasurements, frameSize = 400, pixelsPerMeter = 40, scalingFactor = 4, name = None):

        if scalingFactor < 1:
            scalingFactor == 1
        scaling = scalingFactor > 1

        self.numPlots += 1
        port = 18600+self.numPlots
        uriAddress  = 'tcpip://localhost:'+str(port)
        if name == None:
            name = 'Plot '+str(self.numPlots)

        properties = dict()
        properties['frameSize'] = frameSize
        properties['pixelsPerMeter'] = pixelsPerMeter
        properties['numMeasurements'] = int(numMeasurements/scalingFactor)
        properties['name'] = name

        plot = ObserverAgent(uriAddress=uriAddress,
                                id=self.numPlots,
                                bufferSize=int(numMeasurements * 2 * 4 / scalingFactor),
                                buffer=np.zeros((int(numMeasurements / scalingFactor),2), dtype=np.float32),
                                agentType=1,
                                properties=properties)

        self.agentList.append(plot)

        return True

    def add_scope(self, numSignals = 1, name = None, signalNames=None):

        self.numScopes += 1

        if name == None:
            name = 'Scope '+str(self.numScopes)

        properties = dict()
        properties['numSignals'] = numSignals
        properties['name'] = name
        properties['signalNames'] = signalNames

        port = 18700+self.numScopes
        uriAddress  = 'tcpip://localhost:'+str(port)
        scope = ObserverAgent(uriAddress=uriAddress,
                                id=self.numPlots,
                                bufferSize=(numSignals + 1) * 8,
                                buffer=np.zeros((numSignals + 1, 1), dtype=np.float64),
                                agentType=2,
                                properties=properties)

        self.agentList.append(scope)

        return True

    def thread_function(self, index):
        agent = self.agentList[index]
        print('Launching thread ', index)
        while True:
            if not agent.connected:
                agent.check_connection()

            if agent.connected:
                flag, exit = agent.receive()
                if exit:
                    break
                if flag:
                    agent.process()
                    if agent.agentType == 0 or agent.agentType == 1:
                        cv2.waitKey(1)

    def launch(self):
        refreshFlag = False

        for index, agent in enumerate(self.agentList):
            if agent.agentType == 2:
                refreshFlag = True
                scopeIdx = index
            self.agentThreads.append(Thread(target=self.thread_function, args=[index]))
            self.agentThreads[-1].start()

        if refreshFlag:
            while self.agentThreads[scopeIdx].is_alive():
                MultiScope.refreshAll()

    def terminate(self):
        for probe in self.agentList:
            probe.terminate()

class RemoteDisplay: # works as a client
    '''Class object to send camera feed to a device. Works as a client.'''
    def __init__(
            self,
            ip = 'localhost',
            id = 0,
            imageSize = [480,640,3],
            scaling = True,
            scalingFactor = 2
        ):

        '''
        ip - IP address of the device receiving the data as a string, eg. '192.168.2.4' \n
        id - unique identifier for sending and receiving data. Needs to match the ID in the receiveCamera object. \n
        imageSize - list defining image size. eg. [height, width, # of channels] \n
        scaling - Boolean describing if image will be scaled when sending data. This will decrease its size by the factor in scalingFactor.Default is True \n
        scalingFactor - Factor by which the image will be decreased by. Default is 2. If original image is 480x640, sent image will be 240x320\n
         \n
        Consideration: values for id, imageSize, scaling and scalingFactor need to be the same on the SendCamera and ReceiveCamera objects.
        '''
        if scaling and scalingFactor < 1:
            scalingFactor == 1

        if (scaling and
            (imageSize[0] % scalingFactor != 0 or
            imageSize[1] % scalingFactor != 0)):
            sys.exit('Select a scaling factor that is a factor of both width and height of image')

        if scaling:
            imageSize[0] = int(imageSize[0]/scalingFactor)
            imageSize[1] = int(imageSize[1]/scalingFactor)
            self.newSize = (imageSize[1], imageSize[0])

        bufferSize = np.prod(imageSize)
        # if scaling:
        #     print('Remote Display will stream an image of dimension', self.newSize, 'for', bufferSize, 'bytes.')
        # else:
        #     print('Remote Display will stream an image of dimension', imageSize, 'for', bufferSize, 'bytes.')

        id = np.clip(id,0,80)
        port = 18800+id
        uriAddress  = 'tcpip://' + str(ip) + ':' + str(port)

        self.client = BasicStream(uriAddress, agent='C',
                                  sendBufferSize=bufferSize,
                                  nonBlocking=True)
        self.scaling = scaling
        self.scalingFactor = scalingFactor
        self.connected = self.client.connected

        self.timeout = Timeout(seconds=0, nanoseconds=10000000)

    def check_connection(self):
        '''Checks if the sendCamera object is connected to its server. returns True or False.'''
        # First check if the server was connected.
        self.client.checkConnection(timeout=self.timeout)
        self.connected = self.client.connected

    def send(self,image):
        '''Resizes the image if needed and sends the image added as the input.
         \n
        image - image to send, needs to match imageSize defined while initializing the object'''
        if self.client.connected:
            # add some sort of compression
            if self.scaling:
                image2 = cv2.resize(image, self.newSize)

                sent = self.client.send(image2)
            else:
                sent = self.client.send(image)
            if sent == -1:
                return False
            else:
                return True

    def terminate(self):
        '''Terminates the connection.'''
        self.client.terminate()

class RemotePlot: # works as a client

    def __init__(
            self,
            ip = 'localhost',
            id = 1,
            numMeasurements = 1680,
            scaling = True,
            scalingFactor = 4
        ):
        self.scalingFactor = scalingFactor
        self.scaling = scaling
        self.numMeasurements = numMeasurements
        if scaling:
            self.numMeasurements = int(numMeasurements/self.scalingFactor)
        bufferSize = self.numMeasurements * 2 * 4 # 4 bytes per float and 2 for distances + angles
        port = 18600+id
        uriAddress  = 'tcpip://' + ip + ':'+ str(port)
        self.client = BasicStream(uriAddress, agent='C',
                                  sendBufferSize=bufferSize,
                                  nonBlocking=True)
        self.connected = self.client.connected
        self.timeout = Timeout(seconds=0, nanoseconds=1)

    def check_connection(self):
        '''Checks if the sendCamera object is connected to its server. returns True or False.'''
        # First check if the server was connected.
        self.client.checkConnection(timeout=self.timeout)
        self.connected = self.client.connected

    def send(self, distances = None, angles = None):
        if distances is None or angles is None:
            return False

        if self.client.connected:
            if self.scaling:
                data = np.concatenate((np.reshape(distances[0:-1:self.scalingFactor], (-1, 1)), np.reshape(angles[0:-1:self.scalingFactor], (-1, 1))), axis=1)
            else:
                data = np.concatenate((np.reshape(distances, (-1, 1)), np.reshape(angles, (-1, 1))), axis=1)
            result = self.client.send(data)
            if result == -1:
                return False
            else:
                return True

    def terminate(self):
        '''Terminates the connection.'''
        self.client.terminate()

class RemoteScope():
    def __init__(
            self,
            numSignals = 1,
            id = 1,
            ip = 'localhost'
        ):

        self.numMeasurements = numSignals
        bufferSize = (self.numMeasurements+1) * 8 # 8 bytes per double
        port = 18700+id
        uriAddress  = 'tcpip://' + ip + ':'+ str(port)
        self.client = BasicStream(uriAddress, agent='C',
                                  sendBufferSize=bufferSize,
                                  nonBlocking=True)
        self.connected = self.client.connected
        self.timeout = Timeout(seconds=0, nanoseconds=1000000)

    def check_connection(self):
        '''Checks if the sendCamera object is connected to its server. returns True or False.'''
        # First check if the server was connected.
        self.client.checkConnection(timeout=self.timeout)
        self.connected = self.client.connected

    def send(self, time, data = None):
        if data is None:
            return False

        if self.client.connected:
            timestamp = np.array([time], dtype=np.float64)
            flag = self.client.send(np.concatenate((timestamp, data)))
            if flag == -1:
                return False
            else:
                return True

    def terminate(self):
        '''Terminates the connection.'''
        self.client.terminate()
