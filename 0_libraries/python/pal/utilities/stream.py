"""
stream.py: A module providing utility classes for using Quanser's stream API.

This module contains a collection of classes designed to simplify the process
of using the low-level stream API for network communication. These classes
handle tasks such as connecting to remote systems, sending and receiving data
over a network connection, and managing the connection's state.
"""
from quanser.communications import Stream, StreamError, PollFlag
try:
    from quanser.common import Timeout
except:
    from quanser.communications import Timeout
import numpy as np
import pickle
import io

class BaseStream:
    """Base class for StreamServer and StreamClient."""
    sendBufferSize = 1024
    receiveBufferSize = 1024
    defaultTimeout = 100 * 1e-6 # 100 microseconds

    def __init__(self):
        self._stream = Stream()
        self._status = 0

        self.timeoutDuration = BaseStream.defaultTimeout

    @property
    def timeoutDuration(self):
        """Returns the timeout duration in seconds"""
        return self._timeout.seconds + self._timeout.nanoseconds * 1e-9

    @timeoutDuration.setter
    def timeoutDuration(self, timeout_duration_seconds):
        """Sets the timeout as an instance of Timeout.

        Args:
            timeout_duration_seconds (float): The desired timeout duration
                in seconds.
        """
        seconds = int(timeout_duration_seconds)
        nanoseconds = int((timeout_duration_seconds - seconds) * 1e9)
        self._timeout = Timeout(seconds=seconds, nanoseconds=nanoseconds)

    def terminate(self):
        """Terminate the stream by shutting down and closing the connection."""
        if self._status == 1:
            self._stream.shutdown()
            self._stream.close()
            self._status = 2

    def _check_poll_flags(self, flags):
        """Check if the specified are set for self._stream.

        Flag options come from quanser.communications.PollFlags
        Note: this function will fail if self._stream is already closed.

        Args:
            flags (PollFlag): The poll flags to check.

        Returns:
            bool: True if the specified flags are set, False otherwise.
        """
        pollResult = self._stream.poll(self._timeout, flags)
        return (pollResult & flags) == flags

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()

class StreamServer(BaseStream):
    """Stream server class for accepting and managing client connections."""

    def __init__(self, uri, blocking=False):
        """Initialize the stream server.

        Args:
            uri (str): The URI to listen on.
            blocking (bool, optional): If True, the server operates in
                blocking mode. Defaults to False.
        """
        super().__init__()

        self._stream.listen(uri=uri, non_blocking=(not blocking))
        self._status = 1

    @property
    def status(self):
        """int: Get the status of the server (1: listening, 2: closed)."""
        return self._status

    def accept_clients(self):
        """Accept a client connection.

        Returns:
            StreamClient: A new StreamClient instance connected to the
                accepted client or None if no client was accepted.
        """
        if self._status < 2 and self._check_poll_flags(PollFlag.ACCEPT):
            client = self._stream.accept(
                BaseStream.sendBufferSize,
                BaseStream.receiveBufferSize
            )
            return StreamClient(client)
        return None

class StreamClient(BaseStream):
    """Stream client class for connecting to a stream server."""

    def __init__(self, uri, blocking=False):
        """Initialize the stream client.

        Args:
            uri (str): The URI to connect to.
            blocking (bool, optional): If True, the client operates in
                blocking mode. Defaults to False.
        """
        super().__init__()

        if isinstance(uri, Stream):
            # Not documented and not intended for end users. Used for
            # passing in a Stream object acquired by a server.
            self._status = 1
            self._stream = uri
        else:
            self._uri = uri
            self._blocking = blocking
            self._connect()

        self._buffer = bytearray(BaseStream.receiveBufferSize)


    def _connect(self):
            self._stream.connect(
                uri=self._uri,
                non_blocking=(not self._blocking),
                send_buffer_size=BaseStream.sendBufferSize,
                receive_buffer_size=BaseStream.receiveBufferSize
            )

    @property
    def status(self):
        """Returns the status of the client.

        Returns:
            0: waiting for connection
            1: connected
            2: closed
        """
        if self._status == 0:
            try:
                if self._check_poll_flags(PollFlag.CONNECT):
                    self._status = 1
            except StreamError as e:
                self._stream.close()
                self._connect()
        return self._status


    def receive(self):
        """Receive data from the stream.

        Returns:
            object: The received object or None if no data was received
                or the connection is closed.
        """
        if self.status == 1 and self._check_poll_flags(PollFlag.RECEIVE):
            bytesReceived = self._stream.receive(
                self._buffer,
                BaseStream.receiveBufferSize
            )
            if bytesReceived <= 0:
                self.terminate()
            elif bytesReceived > 0:
                header = self._buffer[0]
                payload = self._buffer[1:bytesReceived]

                if header == 1:
                    return payload.decode('utf-8')
                elif header == 2:
                    return np.load(io.BytesIO(payload))
                else:
                    return pickle.loads(payload)
        return None

    def send(self, obj):
        """Send data over the stream.

        Args:
            obj (object): The object to send.

        Returns:
            bool: True if the data was sent successfully, False otherwise.
        """
        if self.status == 1:
            try:
                if isinstance(obj, str):
                    byteArray = bytearray([1]) + obj.encode('utf-8')

                elif isinstance(obj, np.ndarray):
                    buffer = io.BytesIO()
                    np.save(buffer, obj)
                    byteArray = bytearray([2]) + buffer.getvalue()

                else:
                    byteArray = bytearray([0]) + pickle.dumps(obj)

                self._stream.send(
                    buffer=byteArray,
                    buffer_size=len(byteArray)
                )
                self._stream.flush()

                return True
            except StreamError as e:
                print(e.get_error_message()) # TODO: Check error code
                self.terminate()
        return False

class BasicStream:
    '''Class object consisting of basic stream server/client functionality'''
    def __init__(self, uri, agent='S', receiveBuffer=np.zeros(1, dtype=np.float64), sendBufferSize=2048, 
                 recvBufferSize=2048, nonBlocking=False, verbose=False, reshapeOrder = 'C'):
        '''
        This functions simplifies functionality of the quanser_stream module to provide a
        simple server or client. \n
         \n
        uri - IP server and port in one string, eg. 'tcpip://IP_ADDRESS:PORT' \n
        agent - 'S' or 'C' string representing server or client respectively \n
        receiveBuffer - numpy buffer that will be used to determine the shape and size of data received \n
        sendBufferSize - (optional) size of send buffer, default is 2048 \n
        recvBufferSize - (optional) size of recv buffer, default is 2048 \n
        nonBlocking - set to False for blocking, or True for non-blocking connections \n
         \n
        Stream Server as an example running at IP 192.168.2.4 which receives two doubles from the client: \n
        >>> myServer = BasicStream('tcpip://localhost:18925', 'S', receiveBuffer=np.zeros((2, 1), dtype=np.float64))
         \n
        Stream Client as an example running at IP 192.168.2.7 which receives a 480 x 640 color image from the server: \n
        >>> myClient = BasicStream('tcpip://192.168.2.4:18925', 'C', receiveBuffer=np.zeros((480, 640, 3), dtype=np.uint8))

        '''
        self.agent 			= agent
        self.sendBufferSize = sendBufferSize
        self.recvBufferSize = recvBufferSize
        self.uri 			= uri
        self.receiveBuffer  = receiveBuffer
        self.verbose        = verbose
        self.reshapeOrder   = reshapeOrder  
        # reshape order need to be specified as "F" when reading images streamed from a MATLAB server

        # If the agent is a Client, then Server isn't needed.
        # If the agent is a Server, a Client will also be needed. The server can start listening immediately.

        self.clientStream = Stream()
        if agent=='S':
            self.serverStream = Stream()

        # Set polling timeout to 10 milliseconds
        self.t_out = Timeout(seconds=0, nanoseconds=10000000)

        # connected flag initialized to False
        self.connected = False

        try:
            if agent == 'C':
                self.connected = self.clientStream.connect(uri, nonBlocking, self.sendBufferSize, self.recvBufferSize)
                if self.connected and self.verbose:
                    print('Connected to a Server successfully.')

            elif agent == 'S':
                if self.verbose:
                    print('Listening for incoming connections.')
                self.serverStream.listen(self.uri, nonBlocking)
            pass

        except StreamError as e:
            if self.agent == 'S' and self.verbose:
                print('Server initialization failed.')
            elif self.agent == 'C' and self.verbose:
                print('Client initialization failed.')
            print(e.get_error_message())

    def checkConnection(self, timeout=Timeout(seconds=0, nanoseconds=100)):
        '''When using non-blocking connections (nonBlocking set to True), the constructor method for this class does not block when
        listening (as a server) or connecting (as a client). In such cases, use the checkConnection method to attempt continuing to
        accept incoming connections (as a server) or connect to a server (as a client).  \n
         \n
        Stream Server as an example \n
        >>> while True:
        >>> 	if not myServer.connected:
        >>> 		myServer.checkConnection()
        >>>		if myServer.connected:
        >>> 		yourCodeGoesHere()
         \n
        Stream Client as an example \n
        >>> while True:
        >>> 	if not myClient.connected:
        >>> 		myClient.checkConnection()
        >>>		if myClient.connected:
        >>> 		yourCodeGoesHere()
         \n
        '''
        if self.agent == 'C' and not self.connected:
            try:
                pollResult = self.clientStream.poll(timeout, PollFlag.CONNECT)

                if (pollResult & PollFlag.CONNECT) == PollFlag.CONNECT:
                    self.connected = True
                    if self.verbose: print('Connected to a Server successfully.')

            except StreamError as e:
                if e.error_code == -33:
                    self.connected = self.clientStream.connect(self.uri, True, self.sendBufferSize, self.recvBufferSize)
                else:
                    if self.verbose: print('Client initialization failed.')
                    print(e.get_error_message())

        if self.agent == 'S' and not self.connected:
            try:
                pollResult = self.serverStream.poll(self.t_out, PollFlag.ACCEPT)
                if (pollResult & PollFlag.ACCEPT) == PollFlag.ACCEPT:
                    self.connected = True
                    if self.verbose: print('Found a Client successfully...')
                    self.clientStream = self.serverStream.accept(self.sendBufferSize, self.recvBufferSize)

            except StreamError as e:
                if self.verbose: print('Server initialization failed...')
                print(e.get_error_message())

    def terminate(self):
        '''Use this method to correctly shutdown and then close connections. This method automatically closes all streams involved (Server will shutdown server streams as well as client streams). \n
         \n
        Stream Server as an example \n
        >>> while True:
        >>> 	if not myServer.connected:
        >>> 		myServer.checkConnection()
        >>>		if myServer.connected:
        >>> 		yourCodeGoesHere()
        >>>			if breakCondition:
        >>>				break
        >>> myServer.terminate()
         \n
        Stream Client as an example	 \n
        >>> while True:
        >>> 	if not myClient.connected:
        >>> 		myClient.checkConnection()
        >>>		if myClient.connected:
        >>> 		yourCodeGoesHere()
        >>>			if breakCondition:
        >>>				break
        >>> myClient.terminate()

        '''

        if self.connected:
            self.clientStream.shutdown()
            self.clientStream.close()
            if self.verbose: print('Successfully terminated clients...')

        if self.agent == 'S':
            self.serverStream.shutdown()
            self.serverStream.close()
            if self.verbose: print('Successfully terminated servers...')

    def receive(self, iterations=1, timeout=Timeout(seconds=0, nanoseconds=10)):
        '''
        This functions populates the receiveBuffer with bytes if available. \n \n

        Accepts: \n
        iterations - (optional) number of times to poll for incoming data before terminating, default is 1 \n
         \n
        Returns: \n
        receiveFlag - flag indicating whether the number of bytes received matches the expectation. To check the actual number of bytes received, use the bytesReceived class object. \n
         \n
        Stream Server as an example \n
        >>> while True:
        >>> 	if not myServer.connected:
        >>> 		myServer.checkConnection()
        >>>		if myServer.connected:
        >>> 		flag = myServer.receive()
        >>>			if breakCondition or not flag:
        >>>				break
        >>> myServer.terminate()
         \n
        Stream Client as an example	 \n
        >>> while True:
        >>> 	if not myClient.connected:
        >>> 		myClient.checkConnection()
        >>>		if myClient.connected:
        >>> 		flag = myServer.receive()
        >>>			if breakCondition or not flag:
        >>>				break
        >>> myClient.terminate()

        '''

        self.t_out = timeout
        counter = 0
        dataShape = self.receiveBuffer.shape

        # Find number of bytes per array cell based on type
        numBytesBasedOnType = len(np.array([0], dtype=self.receiveBuffer.dtype).tobytes())

        # Calculate total dimensions
        dim = 1
        for i in range(len(dataShape)):
            dim = dim*dataShape[i]

        # Calculate total number of bytes needed and set up the bytearray to receive that
        totalNumBytes = dim*numBytesBasedOnType
        self.data = bytearray(totalNumBytes)
        self.bytesReceived = 0
        # print(totalNumBytes)
        # Poll to see if data is incoming, and if so, receive it. Poll a max of 'iteration' times
        try:
            while True:

                # See if data is available
                pollResult = self.clientStream.poll(self.t_out, PollFlag.RECEIVE)
                counter += 1
                if not (iterations == 'Inf'):
                    if counter > iterations:
                        break
                if not ((pollResult & PollFlag.RECEIVE) == PollFlag.RECEIVE):
                    continue # Data not available, skip receiving

                # Receive data
                self.bytesReceived = self.clientStream.receive_byte_array(self.data, totalNumBytes)

                # data received, so break this loop
                break

            #  convert byte array back into numpy array and reshape.
            self.receiveBuffer = np.reshape(np.frombuffer(self.data, dtype=self.receiveBuffer.dtype), dataShape, order = self.reshapeOrder)

        except StreamError as e:
            print(e.get_error_message())
        finally:
            receiveFlag = self.bytesReceived==1
            return receiveFlag, totalNumBytes*self.bytesReceived

    def send(self, buffer):
        """
        This functions sends the data in the numpy array buffer
        (server or client). \n \n

        INPUTS: \n
        buffer - numpy array of data to be sent \n

        OUTPUTS: \n
        bytesSent - number of bytes actually sent (-1 if send failed) \n
         \n
        Stream Server as an example \n
        >>> while True:
        >>> 	if not myServer.connected:
        >>> 		myServer.checkConnection()
        >>>		if myServer.connected:
        >>> 		sent = myServer.send()
        >>>			if breakCondition or sent == -1:
        >>>				break
        >>> myServer.terminate()
         \n
        Stream Client as an example	 \n
        >>> while True:
        >>> 	if not myClient.connected:
        >>> 		myClient.checkConnection()
        >>>		if myClient.connected:
        >>> 		sent = myServer.send()
        >>>			if breakCondition or sent == -1:
        >>>				break
        >>> myClient.terminate()

        """

        # Set up array to hold bytes to be sent
        byteArray = buffer.tobytes()
        self.bytesSent = 0

        # Send bytes and flush immediately after
        try:
            self.bytesSent = self.clientStream.send_byte_array(byteArray, len(byteArray))
            self.clientStream.flush()
        except StreamError as e:
            print(e.get_error_message())
            self.bytesSent = -1 # If an error occurs, set bytesSent to -1 for user to check
        finally:
            return self.bytesSent