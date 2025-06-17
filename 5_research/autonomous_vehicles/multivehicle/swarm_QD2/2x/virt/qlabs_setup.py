# Note use this method to get your qvl libraries to ensure you're using the latest version
# in GitHub. It is inserted first in the list to take precedence over all other libraries
# in your python path.
import sys
import time
# sys.path.insert(0, "../")

from qvl.qlabs import QuanserInteractiveLabs
from qvl.free_camera import QLabsFreeCamera
from qvl.qdrone2 import QLabsQDrone2

import sys


########### Main program #################


def main():

    qlabs = QuanserInteractiveLabs()

    print("Connecting to QLabs...")
    if (not qlabs.open("localhost")):
        print("Unable to connect to QLabs")
        return    

    print("Connected")

    # Destroy any existing QLabs actors
    qlabs.destroy_all_spawned_actors()

    # destroy the previous QDrone2 and respawn it in a starting position

    hQDrone0 = QLabsQDrone2(qlabs, True)
    hQDrone0.spawn_id_degrees(actorNumber=0, location=[0.6, 0, 0], rotation=[0, 0, 0], scale=[1,1,1], configuration=0)
    hQDrone0.possess(hQDrone0.VIEWPOINT_TRAILING)

    hQDrone1 = QLabsQDrone2(qlabs, True)
    hQDrone1.spawn_id_degrees(actorNumber=1, location=[-0.6, 0, 0], rotation=[0, 0, 0], scale=[1,1,1], configuration=0)


    qlabs.close()
    print("Done!")

if __name__ == "__main__":
    main()
