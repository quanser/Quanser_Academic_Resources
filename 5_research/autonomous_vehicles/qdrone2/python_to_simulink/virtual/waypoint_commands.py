# This example script is used to send discrete waypoint commands or a smooth trajectory
# to a Mission Server for QDrone2. The mission server is running as an RT model.
import sys
sys.path.insert(0, "../")

from commander import WaypointTrajectory
import time
import numpy as np
import qlabs_setup


########### Main program #################

# discrete waypoint commands/positions in the form x, y, z, yaw. You can modify.
WAYPOINTS = np.array([[-1, -0.5, 0.75, 0.0],
                        [ -1, -0.5, 0.75, np.pi/6],
                        [ -1, 0.5, 0.75, 0.0],
                        [ -1, 0.5, 0.75, -np.pi/6],
                        [ -1, -0.5, 0.75, 0.0],
                        [ -1, 0.5, 0.75, -np.pi/6],
                        [ -1, 0.5, 0.75, 0.0],
                        [ -1, -0.5, 0.75, np.pi/6],
                        [ -1, -0.5, 0.75, 0.0],
                        [ 0, 0.0, 0.75, 0.0]], dtype=np.float64)

#  This integer value determines the amount of time between sending waypoints.
#  Since the waypoints are discrete, it is important that there is adequate time
#  to allow the drone go to the desired position before a new waypoint command
#  is issued. The higher this value, the longer the delay between waypoints.
WAYPOINT_DELAY = 3000

# This flag determines whether discrete waypoints are sent or a smooth trajectory
# is sent. In this example, a circle trajectory is sent using the circle_trajectory()
# method. The default is 0 which is to send discrete waypoints. Set to 1 to send
# a circle (default) or your custom trajectory.
TRAJECTORY = 0


def circle_trajectory(radius, angle):
    """ This method generates the x, y values for a circle trajectory.\n
        as an example on sending smooth trajectories.\n

        params: \n
            radius - float, the circle radius \n
            angle - float, angle of inclination \n

        returns: \n
            a generator of x, y values for each time instant. \n

        usage: \n
        Start the generator:\n
            >>> c = circle_trajectory(radius=1.5, angle=0.15)
            >>> next(c)

        Generate values in your while loop: \n
            >>> x, y = c.send(time.time())

    """
    x, y = [0 for i in range(2)]
    while True:
        timestamp = yield x, y
        x = radius * np.cos(angle * timestamp)
        y = radius * np.sin(angle * timestamp)


def main():
    """ This method sends trajectories to the URI defined in the WaypointTrjector() class"""

    # connect to mission server rt model
    uri = "tcpip://localhost:{}".format(qlabs_setup.PORTS["traj"])
    myqdrone = WaypointTrajectory(uri=uri)

    # initialize generator for sending circle trajectory
    if TRAJECTORY:
        c = circle_trajectory(radius=1, angle=0.15)
        next(c)

    # counters used when sending discrete waypoints
    wait, idx = [0 for i in range(2)]

    print("\nUse Ctrl+C to ABORT at anytime...")

    while True:
        try:
            # check connection
            if not myqdrone.connected:
                myqdrone.check_connection()
            else:
                d_ = myqdrone.receive_data()

                if myqdrone.mode:
                    match TRAJECTORY:
                        case 0:
                            # This section is an example of sending discrete waypoints
                            wait += 1
                            if wait == WAYPOINT_DELAY:
                                print("Sending waypoint {} of {}...".format((idx + 1), WAYPOINTS.shape[0]))
                                myqdrone.send_trajectory(traj=WAYPOINTS[idx])
                                if (idx + 1) == WAYPOINTS.shape[0]:
                                    idx = -1

                                idx += 1
                                wait = 0

                        case 1:
                            # This section is an example of sending a (continuous) circle trajectory
                            x, y = c.send(time.time())
                            myqdrone.send_trajectory(traj=np.array([x, y, 0.75, 0.05]))
                else:
                    pass

        except KeyboardInterrupt:
            # if ctrl+c is pressed and drone is in the air
            print("Mission ABORTED.")
            myqdrone.send_trajectory(traj=WAYPOINTS[-1])
            time.sleep(5)
            myqdrone.terminate()
            break


if __name__ == "__main__":
    main()
