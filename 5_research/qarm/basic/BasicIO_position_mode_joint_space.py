from pal.products.qarm import QArm
from hal.products.qarm import QArmUtilities
import time
import numpy as np

#region: Setup
# Timing Parameters and methods
startTime = 0
def elapsed_time():
    return time.time() - startTime

# Reset startTime before Main Loop
startTime = time.time()
#endregion

with QArm(hardware=1) as myArm:
#region: Main Loop
    myArmUtilities = QArmUtilities()
    ledCmd = np.array([0, 1, 0], dtype=np.float64)
    np.set_printoptions(precision=2, suppress=True)

    while myArm.status:
        result = myArmUtilities.take_user_input_joint_space()
        start = elapsed_time()
        phiCmd = result[0:4]
        gripCmd = result[4]

        location, rotation = myArmUtilities.qarm_forward_kinematics(phiCmd)
        print(f"Arm going to: {location} in x, y, z")

        myArm.read_write_std(phiCMD=phiCmd, gprCMD=gripCmd, baseLED=ledCmd)
        
        print(f"Total time elapsed: {int(elapsed_time())} seconds.")

        # Wait 0.5 seconds before next command
        time.sleep(.5)


    myArm.terminate()

#endregion
