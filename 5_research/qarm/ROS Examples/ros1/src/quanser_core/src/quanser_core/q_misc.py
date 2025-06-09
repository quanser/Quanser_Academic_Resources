from quanser.communications import Stream, StreamError, PollFlag, Timeout
import struct
import numpy as np

class BasicStream:
    '''Class object consisting of basic stream server/client functionality'''
    def __init__(self, uri, agent='s', send_buffer_size=2048, recv_buffer_size=2048):
        """
        This functions simplifies functionality of the quanser_stream module to provide a 
        simple blocking server or client. \n \n

        INPUTS: \n
        uri - IP server and port in one string, eg. 'tcpip://IP_ADDRESS:PORT' \n
        agent - 's' or 'c' string representing server or client respectively
        send_buffer_size - (optional) size of send buffer, default is 2048 \n
        recv_buffer_size - (optional) size of recv buffer, default is 2048 \n

        """
        self.agent = agent
        self.send_buffer_size = send_buffer_size
        self.recv_buffer_size = recv_buffer_size
        self.uri = uri
        
        # If the agent is a Client, then Server isn't needed. 
        # If the agent is a Server, a Client will also be needed. The server can start listening immediately.
        
        self.clientStream = Stream()
        if agent=='s':
            self.serverStream = Stream()
            
        # Set polling timeout to 1 second, and initialize counter for polling connections         
        self.t_out = Timeout(seconds=0, nanoseconds=1000000)
        # counter = 0

        # connected flag initialized to False
        self.connected = False
        non_blocking = False

        try:
            if agent == 'c':
                self.connected = self.clientStream.connect(uri, non_blocking, self.send_buffer_size, self.recv_buffer_size)
       
            elif agent == 's':
                self.serverStream.listen(self.uri, non_blocking)
            pass

        except StreamError as e:
            if self.agent == 's':
                print('Server initialization failed.')
            elif self.agent == 'c':
                print('Client initialization failed.')
            print(e.get_error_message())

    def checkConnection(self):

        if self.agent == 'c' and not self.connected:
            try:
                poll_result = self.clientStream.poll(self.t_out, PollFlag.CONNECT)
                                
                if (poll_result & PollFlag.CONNECT) == PollFlag.CONNECT:
                    self.connected = True
                    print('Connected to the Server successfully.')            

            except StreamError as e:
                if e.error_code == -33:
                    self.connected = self.clientStream.connect(self.uri, True, self.send_buffer_size, self.recv_buffer_size)
                else:
                    print('Client initialization failed.')
                    print(e.get_error_message())

        if self.agent == 's' and not self.connected:
            try:
                poll_result = self.serverStream.poll(self.t_out, PollFlag.ACCEPT)
                if (poll_result & PollFlag.ACCEPT) == PollFlag.ACCEPT:
                    self.connected = True
                    print('Found a Client successfully.')
                    self.clientStream = self.serverStream.accept(self.send_buffer_size, self.recv_buffer_size)

            except StreamError as e:
                print('Server initialization failed.')
                print(e.get_error_message())

    def terminate(self):
        if self.connected:
            self.clientStream.shutdown()
            self.clientStream.close()
            print('Successfully terminated clients.')

        if self.agent == 's':
            self.serverStream.shutdown()
            self.serverStream.close()
            print('Successfully terminated servers.')

    def receive(self, buffer, iterations=1000):
        """
        This functions receives a numpy buffer object that it will fill with bytes if available. \n \n

        INPUTS: \n
        buffer -  numpy float32 array  \n
        iterations - (optional) number of times to poll for incoming data before terminating, default is 1000 \n 

        OUTPUTS: \n
        buffer - data received \n
        bytes_received - number of bytes received \n
        """
        
        self.t_out = Timeout(1)
        counter = 0
        dataShape = buffer.shape

        # Find number of bytes per array cell based on type
        numBytesBasedOnType = len(np.array([0], dtype=buffer.dtype).tobytes())

        # Calculate total dimensions
        dim = 1
        for i in range(len(dataShape)):
            dim = dim*dataShape[i]
        
        # Calculate total number of bytes needed and set up the bytearray to receive that
        totalNumBytes = dim*numBytesBasedOnType
        self.data = bytearray(totalNumBytes)
        self.bytes_received = 0        

        # Poll to see if data is incoming, and if so, receive it. Poll a max of 'iteration' times
        try:
            while True:

                # See if data is available
                poll_result = self.clientStream.poll(self.t_out, PollFlag.RECEIVE)
                counter += 1
                if not (iterations == 'Inf'):
                    if counter >= iterations:
                        break        
                if not ((poll_result & PollFlag.RECEIVE) == PollFlag.RECEIVE):
                    continue # Data not available, skip receiving

                # Receive data
                self.bytes_received = self.clientStream.receive(self.data, totalNumBytes)
                
                # data received, so break this loop
                break 

            #  convert byte array back into numpy array and reshape.
            buffer = np.reshape(np.frombuffer(self.data, dtype=buffer.dtype), dataShape) 

        except StreamError as e:
            print(e.get_error_message())
        finally:
            return buffer, self.bytes_received

    def send(self, buffer):
        """
        This functions sends the data in the numpy array buffer
        (server or client). \n \n

        INPUTS: \n
        buffer - numpy array of data to be sent \n

        OUTPUTS: \n
        bytesSent - number of bytes actually sent (-1 if send failed) \n
        """

        # Set up array to hold bytes to be sent
        byteArray = buffer.tobytes()
        self.bytesSent = 0
        
        # Send bytes and flush immediately after
        try:
            self.bytesSent = self.clientStream.send(byteArray, len(byteArray))
            self.clientStream.flush()
        except StreamError as e:
            print(e.get_error_message())
            self.bytesSent = -1 # If an error occurs, set bytesSent to -1 for user to check
        finally:
            return self.bytesSent

class Utilities:
    '''Class object consisting of common utilities such as saturation methods'''
    @staticmethod
    def saturate(value, upper, lower):
        '''Saturate the input value based on the upper and lower thresholds provided.
            
            For example, 
            >>> saturate(0.1, 0.2, -0.2) # will yeild 0.1
            >>> saturate(0.3, 0.2, -0.2) # will yeild 0.2
            >>> saturate(-0.3, 0.2, -0.2) # will yeild -0.2
            '''

        value_sat = value
        if value > upper:
            value_sat = upper
        if value < lower:
            value_sat = lower   

        return value_sat

class Calculus:
    '''Class object consisting of basic differentiation and integration functions'''

    def differentiator(self, dt, x_prev=0):
        '''Standard derivative. Provide the sample time (s), and use the .send(value) method to differentiate.
        
        For example, 
        >>> diff_1 = Calculus().differentiator(0.01) 
        >>> while True:
        >>>     value = some_random_function()
        >>>     value_derivative = diff_1.send(value)

        Multiple differentiators can be defined for different signals. Do not use the same handle to differentiate different value signals.
        '''
        derivative = 0
        while True:
            x = yield derivative
            derivative = (x - x_prev)/dt
            x_prev = x
    
    def differentiator_variable(self, dt, x_prev=0):
        '''Standard derivative. Provide the sample time (s), and use the .send(value) method to differentiate.
        
        For example, 
        >>> diff_1 = Calculus().differentiator_variable(0.01) 
        >>> while True:
        >>>     value = some_random_function()
        >>>     time_step = some_time_taken
        >>>     value_derivative = diff_1.send((value, time_step))

        Multiple differentiators can be defined for different signals. Do not use the same handle to differentiate different value signals.
        '''
        derivative = 0
        while True:
            x, dt = yield derivative
            derivative = (x - x_prev)/dt
            x_prev = x
    
    def integrator(self, dt, integrand=0):
        '''Standard integral. Provide the sample time (s), and use the .send(value) method to integrate.
        
        For example, 
        >>> intg_1 = Calculus().integrator(0.01)
        >>> while True:
        >>>     value = some_random_function()
        >>>     value_integral = intg_1.send(value)

        Multiple integrators can be defined for different signals. Do not use the same handle to integrate different value signals.
        '''
        while True:
            x = yield integrand
            integrand = integrand + x * dt

    def integrator_variable(self, dt, integrand=0):
        '''Standard integral. Provide the sample time (s), and use the .send(value) method to integrate.
        
        For example, 
        >>> intg_1 = Calculus().integrator_variable(0.01)
        >>> while True:
        >>>     value = some_random_function()
        >>>     time_step = some_time_taken
        >>>     value_integral = intg_1.send((value, time_step)))

        Multiple integrators can be defined for different signals. Do not use the same handle to integrate different value signals.
        '''
        while True:
            x, dt = yield integrand
            integrand = integrand + x * dt

class Filter:
    '''Class object consisting of different filter functions'''

    def low_pass_first_order(self, wn, dt, x0=0):
        '''Standard first order low pass filter. Provide the filter frequency (rad/s), sample time (s), and use the .send(value) method to filter.
        
        For example, 
        >>> filter_1 = filter().low_pass_first_order(20, 0.01)
        >>> value_filtered = next(filter_1)
        >>> while True:
        >>>     value = some_random_function()
        >>>     value_filtered = filter_1.send(value)

        Multiple filters can be defined for different signals. Do not use the same handle to filter different signals.'''

        output = 0
        integrator_1 = Calculus().integrator(dt, integrand=x0)
        next(integrator_1)
        while True:
            x = yield output
            output = integrator_1.send(wn * (x - output))

    def low_pass_first_order_variable(self, wn, dt, x0=0):
        '''Standard first order low pass filter. Provide the filter frequency (rad/s), sample time (s), and use the .send(value) method to filter.
        
        For example, 
        >>> filter_1 = filter().low_pass_first_order(20, 0.01)
        >>> value_filtered = next(filter_1)
        >>> while True:
        >>>     value = some_random_function()
        >>>     value_filtered = filter_1.send(value)

        Multiple filters can be defined for different signals. Do not use the same handle to filter different signals.'''

        output = 0
        integrator_1 = Calculus().integrator_variable(dt, integrand=x0)
        next(integrator_1)
        while True:
            x, dt = yield output
            output = integrator_1.send((wn * (x - output), dt))

    def low_pass_second_order(self, wn, dt, zeta=1, x0=0):
        '''Standard second order low pass filter. Provide the filter frequency (rad/s), sample time (s), and use the .send(value) method to filter.
        
        For example, 
        >>> filter_2 = filter().low_pass_second_order(20, 0.01)
        >>> value_filtered = next(filter_2)
        >>> while True:
        >>>     value = some_random_function()
        >>>     value_filtered = filter_2.send(value)

        Multiple filters can be defined for different signals. Do not use the same handle to filter different signals.'''
        output = 0
        temp = 0        
        integrator_1 = Calculus().integrator(dt, integrand=0)
        integrator_2 = Calculus().integrator(dt, integrand=x0)
        next(integrator_1)
        next(integrator_2)
        while True:
            x = yield output
            temp = integrator_1.send(wn * ( x - output - 2*zeta*temp ) )
            output = integrator_2.send(wn * temp)

    def moving_average(self, samples, x_0=0):
        '''Standard moving average filter. Provide the number of samples to average, and use the .send(value) method to filter.
        
        For example, 
        >>> filter_3 = filter().moving_average(20)
        >>> value_filtered = next(filter_3)
        >>> while True:
        >>>     value = some_random_function()
        >>>     value_filtered = filter_3.send(value)

        Multiple filters can be defined for different signals. Do not use the same handle to filter different signals.'''
        window = x_0*np.ones(samples)
        average = x_0
        while True:
            new_value = yield average
            window = np.append(new_value, window[0:samples-1])
            average = window.mean()

class Signal_Generator:
    '''Class object consisting of common signal generators'''
    def sine(self, amplitude, ang_freq, phase=0, mean=0):
        '''This function outputs a sinusoid wave based on the provided timestamp. 
        
        For example:
        >>> generator_sine = Signal_Generator().sine(2, pi/2)
        >>> initial_output = next(generator_sine)
        >>> while True:
        >>>     timestamp = your_timing_function()
        >>>     output = generator_sine.send(timestamp) '''

        output = amplitude*np.sin(phase) + mean
        while True:
            timestamp = yield output
            output = amplitude*np.sin(ang_freq*timestamp + phase) + mean

    def cosine(self, amplitude, ang_freq, phase=0, mean=0):
        '''This function outputs a cosinusoid wave based on the provided timestamp. 
        
        For example:
        >>> generator_cosine = Signal_Generator().cosine(2, pi/2)
        >>> initial_output = next(generator_sine)
        >>> while True:
        >>>     timestamp = your_timing_function()
        >>>     output = generator_cosine.send(timestamp) '''

        output = amplitude*np.sin(phase + np.pi/2) + mean
        while True:
            timestamp = yield output
            output = amplitude*np.sin(ang_freq*timestamp + phase + np.pi/2) + mean

    def PWM(self, freq, width, phase=0):
        '''This function outputs a PWM wave based on the provided timestamp. 
        
        For example:
        >>> generator_PWM = Signal_Generator().PWM(2, 0.5)
        >>> initial_output = next(generator_PWM)
        >>> while True:
        >>>     timestamp = your_timing_function()
        >>>     output = generator_PWM.send(timestamp) '''

        period = 1/freq
        if phase%1 >= width:
            output = 0
        else:
            output = 1
        while True:
            timestamp = yield output
            marker = ( ( (timestamp % period) / period ) + phase ) % 1
            if marker > width:
                output = 0
            else:
                output = 1
