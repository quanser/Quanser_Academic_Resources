# Servo

# Exploring how to drive a servo

# region: Python level imports
from pal.products.actuators import ActuatorsTrainer
from pal.utilities.keyboard import QKeyboard
from pal.utilities.timing import Timer
# endregion 

# region: Experiment constants
simulationTime = 120 # Simulation run time (seconds)
frequency = 50       # Simulation frequency (Hz)
# endregion

kbd = QKeyboard()


# region: Main Loop

# Initialize Actuators Block #2 
# servoMode is
#   0 for 0.5 to 2.5 ms command range
#   1 for 1.0 to 2.0 ms command range
with ActuatorsTrainer(block = 2, servoMode = 0) as actuators: 
    timer = Timer(sampleRate=frequency, totalTime=simulationTime)
    # Minimum incremental servo command
    delta = 0.0
    # Zero position bias
    bias  = 0.0

    servoCmd = 0.5 # Initial servo command

    actuators.enable_motors()

    while timer.check():
        # Read Keyboard states and increment servoCmd
        kbd.update()
        if kbd.states[kbd.K_UP]:
            servoCmd = servoCmd + delta
            if servoCmd > 1.0: servoCmd = 1.0 # upper saturation
        if kbd.states[kbd.K_DOWN]:
            servoCmd = servoCmd - delta
            if servoCmd < 0.0: servoCmd = 0.0 # lower saturation

        print(f'Servo Command: {servoCmd:.4f}')

        actuators.update_servo(servoCmd + bias) # Update servoCmd in buffer
        actuators.write_motors()         # Write servoCmd to the motor

        timer.sleep()
# endregion