from quanser.communications import Stream, StreamError, PollFlag
from quanser.common import ErrorCode
try:
    from quanser.common import Timeout
except:
    from quanser.communications import Timeout

import struct
import os
import platform
import time


######################### MODULAR CONTAINER CLASS #########################

class CommModularContainer:

    """The CommModularContainer is a collection of data used to communicate with actors. Multiple containers can be packaged into a single packet."""

    # Define class-level variables
    containerSize = 0
    """The size of the packet in bytes. Container size (uint32: 4 bytes) + class ID (uint32: 4 bytes) + actor number (uint32: 4 bytes) + actor function (1 byte) + payload (varies per function)"""
    classID = 0
    """See the class ID variables in the respective library classes."""
    actorNumber = 0
    """An identifier that should be unique for each actor of a given class. """
    actorFunction = 0
    """See the FCN constants in the respective library classes."""
    payload = bytearray()
    """A variable sized payload depending on the actor function in use."""

    ID_GENERIC_ACTOR_SPAWNER = 135
    """The actor spawner is a special actor class that exists in open world environments that manages the spawning and destruction of dynamic actors."""
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_ID = 10
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_ID_ACK = 11
    FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ACTOR = 12
    FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ACTOR_ACK = 13
    FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_ACTORS_OF_CLASS = 24
    FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_ACTORS_OF_CLASS_ACK = 25
    FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_ACTORS = 14
    FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_ACTORS_ACK = 15
    FCN_GENERIC_ACTOR_SPAWNER_REGENERATE_CACHE_LIST = 16
    FCN_GENERIC_ACTOR_SPAWNER_REGENERATE_CACHE_LIST_ACK = 17
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN = 22
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_RESPONSE = 23
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_AND_PARENT_RELATIVE = 50
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_AND_PARENT_RELATIVE_ACK = 51
    FCN_GENERIC_ACTOR_SPAWNER_PARENT_CURRENT_WORLD = 52
    FCN_GENERIC_ACTOR_SPAWNER_PARENT_CURRENT_WORLD_ACK = 53
    FCN_GENERIC_ACTOR_SPAWNER_PARENT_RELATIVE = 54
    FCN_GENERIC_ACTOR_SPAWNER_PARENT_RELATIVE_ACK = 55
    FCN_GENERIC_ACTOR_SPAWNER_PARENT_BREAK_WITH_CURRENT_WORLD = 56
    FCN_GENERIC_ACTOR_SPAWNER_PARENT_BREAK_WITH_CURRENT_WORLD_ACK = 57

    ID_UNKNOWN = 0
    """Class ID 0 is reserved as an unknown class. QLabs may respond with a container with information it does not understand due to an unknown class, if data was improperly formatted, or if communication methods were executed in the wrong order."""

    BASE_CONTAINER_SIZE = 13
    """Container size variable (4 bytes) + class ID (4 bytes) + actor number (4 bytes) + actor function (1 byte). Does not include the payload size which is variable per function."""

    # Initialize class
    def __init__(self):

       return

######################### COMMUNICATIONS #########################

class QuanserInteractiveLabs:
    """This class establishes a server connection with QLabs and manages the communications."""
    _stream = None
    
    _BUFFER_SIZE = 100000

    _readBuffer = bytearray(_BUFFER_SIZE)
    _sendBuffer = bytearray()

    _receivePacketBuffer = bytearray()
    _receivePacketSize = 0
    _receivePacketContainerIndex = 0
    _wait_for_container_timeout = 5

    _send_queue = bytearray()


    # Initialize QLabs
    def __init__(self):
        """ Constructor Method """
        pass

    def open(self, address, timeout=10):
        """Open a connection to QLabs.

        :param address: The machine name or IP address of a local or remote copy of QLabs such as "localhost", or "192.168.1.123".
        :param timeout: (Optional) Period to attempt the connection for before aborting. Default 10s.
        :type address: string
        :type timeout: float
        :return: `True` if successful, `False` otherwise
        :rtype: boolean

        """

        address = "tcpip://" + address + ":18000"

        self._stream = Stream()

        result = self._stream.connect(address, True, self._BUFFER_SIZE, self._BUFFER_SIZE)
        if (result == False):
            # Connection was not immediate so poll the stream to determine what might be wrong
            pollResult = 0

            while (((pollResult & PollFlag.CONNECT) != PollFlag.CONNECT) and (timeout > 0)):
                try:
                    pollResult = self._stream.poll(Timeout(1), PollFlag.CONNECT)
                except StreamError as e:
                    if e.error_code == -33:
                        self._stream.close()
                        return False
                    
                timeout = timeout - 1

            if pollResult & PollFlag.CONNECT == PollFlag.CONNECT:
                #print("Connection accepted")
                pass
            else:
                if (timeout == 0):
                    print("Connection timeout")
                    
                self._stream.close()
                return False

        return True

    def close(self):
        """Shutdown and close a connection to QLabs. Always close a connection when communications are finished.

        :return: No return. If an existing connection cannot be found, the function will fail silently.
        :rtype: none

        """
        try:
            self._stream.shutdown()
            self._stream.close()
        except:
            pass

    def queue_add_container(self, container):
        """Queue a single container into a buffer for future transmission

        :param container: CommModularContainer populated with the actor information.
        :type container: CommModularContainer object

        """

        self._send_queue = self._send_queue + bytearray(struct.pack(">iiiB", container.containerSize, container.classID, container.actorNumber, container.actorFunction)) + container.payload

    def queue_send(self):
        """Package the containers in the queue and transmit immediately

        :param container: CommModularContainer populated with the actor information.
        :type container: CommModularContainer object
        :return: `True` if successful and the queue will be emptied, `False` otherwise and the queue will remain intact.
        :rtype: boolean

        """

        try:
            data = bytearray(struct.pack("<iB", 1+len(self._send_queue))) + self._send_queue
            numBytes = len(data)
            bytesWritten = self._stream.send(data, numBytes)
            self._stream.flush()
            self._send_queue = bytearray()
            return True
        except:
            return False

    def queue_destroy(self):
        """The container queue is emptied of all data.

        """
        self._send_queue = bytearray()

    # Pack data and send immediately
    def send_container (self, container):
        """Package a single container into a packet and transmit immediately

        :param container: CommModularContainer populated with the actor information.
        :type container: CommModularContainer object
        :return: `True` if successful, `False` otherwise
        :rtype: boolean

        """
        result = False
        try:
            data = bytearray(struct.pack("<i", 1+container.containerSize)) + bytearray(struct.pack(">BiiiB", 123, container.containerSize, container.classID, container.actorNumber, container.actorFunction)) + container.payload
            numBytes = len(data)
            bytesWritten = self._stream.send_byte_array(data, numBytes)
            if bytesWritten > 0:
                self._stream.flush()
                result = True
        except:
            pass

        return result

    # Check if new data is available.  Returns true if a complete packet has been received.
    def receive_new_data(self):
        """Poll for new data received from QLabs through the communications framework. If you are expecting large amounts of data such as video, this should be executed frequently to avoid overflowing internal buffers. Data split over multiple packets will be automatically reassembled before returning true. This method is non-blocking.

        :return: `True` if at least one complete container has been received, `False` otherwise
        :rtype: boolean

        """
        bytesRead = self._stream.receive(self._readBuffer, self._BUFFER_SIZE) # returns -ErrorCode.WOULD_BLOCK if it would block
        newData = False

        while bytesRead > 0:
            self._receivePacketBuffer += bytearray(self._readBuffer[0:(bytesRead)])

            #while we're here, check if there are any more bytes in the receive buffer
            bytesRead = self._stream.receive(self._readBuffer, self._BUFFER_SIZE) # returns -ErrorCode.WOULD_BLOCK if it would block

        # check if we already have data in the receive buffer that was unprocessed (multiple packets in a single receive)
        if len(self._receivePacketBuffer) > 5:
            if (self._receivePacketBuffer[4] == 123):

                # packet size
                self._receivePacketSize, = struct.unpack("<I", self._receivePacketBuffer[0:4])
                # add the 4 bytes for the size to the packet size
                self._receivePacketSize = self._receivePacketSize + 4

                if len(self._receivePacketBuffer) >= self._receivePacketSize:

                    self._receivePacketContainerIndex = 5
                    newData = True

            else:
                print("Error parsing multiple packets in receive buffer.  Clearing internal buffers.")
                _receivePacketBuffer = bytearray()

        return newData

    # Parse out received containers
    def get_next_container(self):
        """If receive_new_data has returned true, use this method to receive the next container in the queue.

        :return: The data will be returned in a CommModularContainer object along with a flag to indicate if additional complete containers remain in the queue for extraction. If this method was used without checking for new data first and the queue is empty, the container will contain the default values with a class ID of ID_UNKNOWN.
        :rtype: CommModularContainer object, boolean

        """

        c = CommModularContainer()
        isMoreContainers = False

        if (self._receivePacketContainerIndex > 0):
            c.containerSize, = struct.unpack(">I", self._receivePacketBuffer[self._receivePacketContainerIndex:(self._receivePacketContainerIndex+4)])
            c.classID, = struct.unpack(">I", self._receivePacketBuffer[(self._receivePacketContainerIndex+4):(self._receivePacketContainerIndex+8)])
            c.actorNumber, = struct.unpack(">I", self._receivePacketBuffer[(self._receivePacketContainerIndex+8):(self._receivePacketContainerIndex+12)])
            c.actorFunction = self._receivePacketBuffer[self._receivePacketContainerIndex+12]
            c.payload = bytearray(self._receivePacketBuffer[(self._receivePacketContainerIndex+c.BASE_CONTAINER_SIZE):(self._receivePacketContainerIndex+c.containerSize)])

            self._receivePacketContainerIndex = self._receivePacketContainerIndex + c.containerSize

            if (self._receivePacketContainerIndex >= self._receivePacketSize):

                isMoreContainers = False

                if len(self._receivePacketBuffer) == self._receivePacketSize:
                    # The data buffer contains only the one packet.  Clear the buffer.
                    self._receivePacketBuffer = bytearray()
                else:
                    # Remove the packet from the data buffer.  There is another packet in the buffer already.
                    self._receivePacketBuffer = self._receivePacketBuffer[(self._receivePacketContainerIndex):(len(self._receivePacketBuffer))]

                self._receivePacketContainerIndex = 0

            else:
                isMoreContainers = True


        return c, isMoreContainers

    def set_wait_for_container_timeout(self, timeout):
        """By default, a method using the wait_for_container method (typically represented with the waitForComfirmation flag) will abort waiting for an acknowledgment after 5 seconds
        at which time the method will return a failed response. This time period can be adjusted with this function. Values
        less than or equal to zero will cause the methods to wait indefinitely until the expected acknowledgment is received.

        :param timeout: Timeout period in seconds
        :type timeout: float

        """


        if (timeout < 0):
            timeout = 0

        self._wait_for_container_timeout = timeout

    def wait_for_container(self, classID, actorNumber, functionNumber):
        """Continually poll and parse incoming containers until a response from specific actor with a specific function response is received.
        Containers that do not match the class, actor number, and function number are discarded. This function blocks until the appropriate packet
        is received or the timeout is reached.

        :return: The data will be returned in a CommModularContainer object.
        :rtype: CommModularContainer object

        """

        startTime = time.time()

        while(True):
            while (self.receive_new_data() == False):
                if self._wait_for_container_timeout > 0:
                    currentTime = time.time()
                    if (currentTime - startTime >= self._wait_for_container_timeout):
                        return None
                pass

            moreContainers = True

            while (moreContainers):
                c, moreContainers = self.get_next_container()

                if c.classID == classID:
                    if c.actorNumber == actorNumber:
                        if c.actorFunction == functionNumber:
                            return c

    def flush_receive(self):
        """Flush receive buffers removing all unread data. This can be used to clear receive buffers after fault conditions to ensure it contains only new data.

        :return: None
        :rtype: None

        """
        bytesRead = self._stream.receive(self._readBuffer, self._BUFFER_SIZE) # returns -ErrorCode.WOULD_BLOCK if it would block
        self._receivePacketBuffer = bytearray()
        self._receivePacketContainerIndex = 0

    def regenerate_cache_list(self):
        """Advanced function for actor indexing.

        :return: `True` if successful, `False` otherwise
        :rtype: boolean

        .. danger::

            TODO: Improve this description.
        """
        c = CommModularContainer()
        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_REGENERATE_CACHE_LIST
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if (self.send_container(c)):
            c = self.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, c.actorNumber, CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_REGENERATE_CACHE_LIST_ACK)
            if (c == None):
                return False
            else:
                return True

        else:
            return False

    def ping(self):
        """QLabs will automatically disconnect a non-responsive client connection. The ping method can be used to keep the connection alive if operations are infrequent.

        :return: `True` if successful, `False` otherwise
        :rtype: boolean
        """

        FCN_REQUEST_PING = 1
        FCN_RESPONSE_PING = 2


        c = CommModularContainer()
        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = FCN_REQUEST_PING
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self.flush_receive()

        if (self.send_container(c)):

            c = self.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, 0, FCN_RESPONSE_PING)
            if (c == None):
                return False
            elif c.payload[0] > 0:
                return True
            else:
                return False
        else:
            return False

    def destroy_all_spawned_actors(self):
        """Find and destroy all spawned actors and widgets. This is a blocking operation.

        :return: The number of actors deleted. -1 if failed.
        :rtype: int32

        """
        actorNumber = 0
        c = CommModularContainer()

        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = actorNumber
        c.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_ACTORS
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if (self.send_container(c)):
            c = self.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, actorNumber, CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_ACTORS_ACK)
            if (c == None):
                return -1

            if len(c.payload) == 4:
                num_actors_destroyed, = struct.unpack(">I", c.payload[0:4])
                return num_actors_destroyed
            else:
                return -1

        else:
            return -1

    def __del__(self):
        """ Destructor Method """
        self.close()