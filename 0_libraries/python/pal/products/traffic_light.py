# Traffic Light Client
"""
This script provides a user-friendly library to interact with traffic lights. 
It establishes a connection to a Raspberry Pi Zero W running a micro-controller that controls the traffic light LEDs. 
The library offers functionalities to control the traffic lights manually (setting them to red, yellow, or green) or switch them to an automatic timed mode. 
It also allows for turning off the lights and starting or stopping a stream.

"""

import urllib.request, sys
from urllib.error import HTTPError, URLError
from socket import timeout
import time

class TrafficLight():
    
    def __init__(self, ip):
        """ 
        Connection to the lights
        
        Args:
            ip (string): 192.168.2.xxx when connected to Quanser_UVS network
        """
        self.url = "http://" + ip + ":5000/"

    def status(self):
        """
        Check and return the status of LEDs in use

        Args:
            None
        
        Returns (str):
            0 -> No lit LEDs, 1 -> Red LED lit, 2 -> Yellow LED lit, 3 -> Green LED lit
        """ 
        request = 'status'
        response = self._sendreq(self.url + request)
        return response
    
    def shutdown(self):
        """
        Shutdown the Traffic Light
        
        Args:
            None
        """
        request = 'shutdown'
        response = self._sendreq(self.url + request)
        print('Shutting Down Traffic Light ' + self.url)
        return response
    
    def auto(self):
        """
        Set the Traffic lights to automatic mode

        Args:
            None

        Automatic mode: The traffic lights cycle through the following sequence:
        Red light illuminated for 30 seconds.
        Green light illuminated for 30 seconds.
        Yellow light illuminated for 3 seconds.
        The cycle then repeats.
        """
        response = self.timed(0,0,0) # the r/y/g flags are set to 0s to trigger automatic mode
        return response
        
    def red(self):
        """
        Set Traffic Light to Red 
        
        Args:
            None

        Two LEDs cannot be turned on at the same time
        """
        request = 'immediate/red'
        response = self._sendreq(self.url + request)
        return response
     
    def yellow(self):
        """
        Set Traffic Light to Yellow 
        
        Args:
            None

        Two LEDs cannot be turned on at the same time
        """
        request = 'immediate/yellow'
        response = self._sendreq(self.url + request)
        return response
        
    def green(self):
        """
        Set Traffic Light to Green 
        
        Args:
            None

        Two LEDs cannot be turned on at the same time
        """
        request = 'immediate/green'
        response = self._sendreq(self.url + request)
        return response
     
    def color(self, color):
        """
        Function to set one of the traffic light LEDs on.
        Can only have one color ON at a time. 
        
        Args:
            color(int): 0-off; 1-red; 2-yellow; 3-green
        """
        if int(color) == 0:
            response = self.off()
        elif int(color) == 1:
            response = self.red()
        elif int(color) == 2:
            response = self.yellow()
        elif int(color) == 3:
            response = self.green()
        else:
            response = self.off()
        return response
 
    def timed(self, red = 30, yellow = 3, green = 30):
        """
        Set custom timed cycle for the Traffic Lights LEDs 
        
        Args:
            red (int): x seconds where red will be on
            yellow (int): x seconds where yellow will be on
            green (int): x seconds where green will be on

        Two LEDs cannot be turned on at the same time. 
        Default mode, The timed lights cycle set red -> 30s, yellow -> 3s & green -> 30s 
        """
        self.off()
        time.sleep(0.25)
        request = "timed/" + str(red) + "/" + str(yellow) + "/" + str(green)
        response = self._sendreq(self.url + request)
        return response
    
    def off(self):
        """
        Turn the LEDs off without shutting down
        
        Args:
            None
        """
        request = 'immediate/off'
        response = self._sendreq(self.url + request)
        return response
    
    def start_stream(self):
        """
        Connect to Matlab/Simulink using QUARC Streaming API
        
        Args:
            None

        Closes the serial port in python so it can be accessed 
        by Matlab/Simulink to connect/communicate with the lights
        """
        self.off()
        request = 'start_stream'
        response = self._sendreq(self.url + request)
        return response
    
    def stop_stream(self):
        """
        Reconnects back to Python to use TrafficLight functions
        
        Args:
            None

        Reopens the serial port in python so all the methods 
        in TrafficLight can resume communicating with the lights 
        """
        request = 'close_stream'
        response = self._sendreq(self.url + request)
        return response
    
    def isStreaming(self):
        """
        Check if the Streaming connection is Open
        
        Args:
            None
        
        Return:
            (string): Returns the status of streaming connection

        Check if the streaming connection is already open. 
        If you want to use the methods in TrafficLight, 
        the stream connection needs to be closed first.
        """
        request = 'check_stream'
        streaming = self._sendreq(self.url + request)
        if(streaming == '1' or streaming == '0'):
            return 'Streaming connection is open' if streaming == '1' else 'Streaming connection is NOT open'
        else:
            return streaming
        
    #Send the formatted request
    def _sendreq(self, url):
        #Format the HTTP get request with a timeout 
        # of 1s to account for async tasks that will not return
        response = "Call complete!"
        try:
            if url.find("stream") == -1:
                timeoutURL=1
            else:
                timeoutURL=4
            response = urllib.request.urlopen(url, timeout=timeoutURL).read().decode('utf-8')
        #If the URL is not correct
        except (HTTPError, URLError) as error:
            if(self.isStreaming() == '1'):
                response = "Streaming is open, Close the stream to use TrafficLight() functions"
            else:
                response = "Error endpoint not found at " + url
        #If the request was not expected to return the call it complete, otherwise flag a timeout
        except timeout:
            if url.find("timed") == -1:
                if(self.isStreaming() == '1'):
                    response = "Streaming is open, Close the stream to use TrafficLight() functions"
                else:
                    response = "Call timed out"
            else:
                response = "Async call complete"

        return response