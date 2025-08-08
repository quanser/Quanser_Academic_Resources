import time
from pal.products.qarm_mini import QArmMini
from pal.utilities.keyboard import KeyBoardDriver
from hal.products.qarm_mini import QArmMiniKeyboardNavigator

kbd         = KeyBoardDriver(rate=30.0)
<<<<<<< HEAD
myMiniArm   = QArmMini(hardware=1, id=6)
=======
myMiniArm   = QArmMini(hardware=1, id=8)
>>>>>>> feature-qarm_mini
kbdNav      = QArmMiniKeyboardNavigator(kbd, initialPose=myMiniArm.HOME_POSE)

simulationTime  = 300 # will run for 10 seconds
startTime       = time.time()
end             = startTime

def elapsed_time():
    return time.time() - startTime

try:
    while elapsed_time() < simulationTime:
        if not kbd.connected:
            kbd.checkConnection()
        else:
            new = kbd.update()
            if new:
                start = elapsed_time()

                # To move one joint at a time w/ 1 2 3 4
                # myMiniArm.read_write_std(
                #     kbdNav.move_joints_with_keyboard(start - end))

                # To move one cartesian axis or gamma at a time w/ x, y, z, g
                myMiniArm.read_write_std(
                    kbdNav.move_ee_with_keyboard(start - end))

                end = start

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:
    myMiniArm.terminate()
    kbd.terminate()

