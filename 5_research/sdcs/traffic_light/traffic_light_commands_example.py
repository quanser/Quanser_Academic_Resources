## Traffic light example
# This example initializes a Traffic Light and runs through the different
# commands to control it.  
# Modify the light_ip variable to have the correct IP of the Traffic light.
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# imports

from pal.products.traffic_light import TrafficLight
import time
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

# Provide the Traffic Light IP address
## -- -- -TRAFFIC LIGHT IP- -- -- 
light_ip = '192.168.2.3'
# -- -- -- -- -- -- -- -- -- -- --

# Initialize a Traffic Light with its corresponding IP
light = TrafficLight(light_ip)

# Check the status of the lights. 0 - No lights, 1 - Red LED, 
# 2 - Yellow LED, 3 - Green LED
status = light.status()
print("Traffic Light Status is: " + status)

print("Waiting...")
time.sleep(5)

# Set the Traffic Lights to automatic mode, the LEDs through 
# the red LED for 30s, the green LED for 30s and Yellow for 3s
automaticMode = light.auto()
print(automaticMode)

print('Running Lights in Auto Mode LEDs RED -> 30s, GREEN -> 30s, YELLOW -> 3s')
print("Waiting...")
time.sleep(65)

# IMPORTANT NOTE: IF USING THE FUNCTIONS AUTO OR TIMED MORE THAN ONCE 
# IN THE TRAFFIC LIGHT (E.G., EVERY TIME THE CODE STARTS) MAKE SURE TO 
# FIRST CALL LIGHT.OFF() AND DO A SLEEP FOR THE TOTAL AMOUNT OF TIME THE LIGHT 
# CYCLE WAS SUPPOSED TO LAST FOR. FOR AUTO THAT IS 30+30+3. THIS WILL ENSURE 
# THAT THE CYCLE PROPERLY STOPS, IF NOT, THE TRAFFIC LIGHT MIGHT START FLASHING 
# IN UNEXPECTED WAYS. ANOTHER OPTION IS TO JUST UNPLUG AND PLUG THE LIGHT.  

# Manually turn on of the traffic light LEDs - RED
redLED = light.red()
print(redLED)

# Check the status of the lights 
# ( 0 - all off, 1 - red, 2 -yellow, 3 - green).
status = light.status()
print("Traffic Light Status is: " + status)

print("Waiting...")
time.sleep(5)

# Manually turn on of the traffic light LEDs - YELLOW
yellowLED = light.yellow()
print(yellowLED)

# Check the status of the lights.
# ( 0 - all off, 1 - red, 2 -yellow, 3 - green).
status = light.status()
print("Traffic Light Status is: " + status)

print("Waiting...")
time.sleep(5)

# Manually turn on of the traffic light LEDs - GREEN
greenLED = light.green()
print(greenLED)

# Check the status of the lights.
# ( 0 - all off, 1 - red, 2 -yellow, 3 - green).
status = light.status()
print("Traffic Light Status is: " + status)

print("Waiting...")
time.sleep(5)

# Cycle through the LEDs
print("Cycle through LEDs RED -> YELLOW -> GREEN")
col = 0
while col < 6:
    response = light.color(1 + col % 3) # has 1+ since color(0) is off 
    # function needs  0-off; 1-red; 2-yellow; 3-green
    print(response)

    time.sleep(3)

    col = col + 1

print("Waiting...")
time.sleep(5)

# Set custom timed cycle for Traffic Lights LEDs 
print("Custom timed cycle. RED: 3s, YELLOW: 1s, GREEN: 5s")
customTime = light.timed(3, 1, 5)
print(customTime)

time.sleep(30)

# Turn off the traffic light with shutting down
turnOff = light.off()
print(turnOff)

# # Shutdown Traffic Light
# shutDown = light.shutdown()
# print(shutDown)