'''hardware_test_gamepad.py

This example demonstrates how to read data from the Logitech F710 gamepad.
The data received from buttons independently might change depending on the OS
(windows vs. linux)
'''
from pal.utilities.gamepad import LogitechF710
import time
import os


# Timing and Initialization
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

simulationTime = 60
sampleRate = 100
sampleTime = 1/sampleRate
gpad = LogitechF710()

# Restart starTime just before Main Loop
startTime = time.time()

## Main Loop
try:
    while elapsed_time() < simulationTime:
        # Start timing this iteration
        start = elapsed_time()

        # Basic IO - write motor commands
        new = gpad.read()

        if new:
            # Clear the Screen for better readability
            os.system('cls')

            # Print out the gamepad IO read
            print("Left Laterial:\t\t{0:.2f}\nLeft Longitudonal:\t{1:.2f}\nTrigger:\t\t{2:.2f}\nRight Lateral:\t\t{3:.2f}\nRight Longitudonal:\t{4:.2f}"
                .format(gpad.leftJoystickX, gpad.leftJoystickY, gpad.trigger, gpad.rightJoystickX, gpad.rightJoystickY))
            print("Button A:\t\t{0:.0f}\nButton B:\t\t{1:.0f}\nButton X:\t\t{2:.0f}\nButton Y:\t\t{3:.0f}\nButton LB:\t\t{4:.0f}\nButton RB:\t\t{5:.0f}"
                .format(gpad.buttonA, gpad.buttonB, gpad.buttonX, gpad.buttonY, gpad.buttonLeft, gpad.buttonRight))
            print("Up:\t\t\t{0:.0f}\nRight:\t\t\t{1:.0f}\nDown:\t\t\t{2:.0f}\nLeft:\t\t\t{3:.0f}"
                .format(gpad.up, gpad.right, gpad.down, gpad.left))

        # End timing this iteration
        end = elapsed_time()

        # Calculate computation time, and the time that the thread should
        # pause/sleep for
        computation_time = end - start
        sleep_time = sampleTime - computation_time%sampleTime

        # Pause/sleep and print out the current timestamp
        time.sleep(sleep_time)

except KeyboardInterrupt:
    print("User interrupted!")

finally:
    # Terminate Joystick properly
    gpad.terminate()