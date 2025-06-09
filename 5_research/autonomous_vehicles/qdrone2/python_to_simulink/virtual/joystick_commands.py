# This example script is used to emulate and send joystick commands to a
# Mission Server for QDrone2. The mission server is running as an RT model.
import sys
sys.path.insert(0, "../")

from commander import JoystickCommands
import os
import time
import qlabs_setup

########### Main program #################

def main():

    qlabs_setup.main()

    sleep_for = 0.5 # seconds

    # connect to Mission server rt model
    uri = "tcpip://localhost:{}".format(qlabs_setup.PORTS["joystick"])
    myqdrone = JoystickCommands(uri=uri)

    # start mission server
    if qlabs_setup.USE_VRPN:
        os.system("quarc_run -D -r -t tcpip://localhost:17000 rtmodels/MissionServerVRPN.rt-win64 \
            -uri tcpip://localhost:17002 -URI_Host tcpip://localhost:{}".format(qlabs_setup.PORTS["host"]))
        time.sleep(sleep_for)
    else:
        os.system("quarc_run -D -r -t tcpip://localhost:17000 rtmodels/MissionServerLegacy.rt-win64 \
            -uri tcpip://localhost:17002 -URI_Host tcpip://localhost:{} \
            -uri_pose tcpip://localhost:{}".format(qlabs_setup.PORTS["host"], qlabs_setup.PORTS["pose"]))
        time.sleep(sleep_for)

    # start stabilizer
    os.system("quarc_run -D -r -t tcpip://localhost:17000 rtmodels/DroneStack.rt-win64 \
            -uri tcpip://localhost:17003 -URI_Host tcpip://localhost:{}".format(qlabs_setup.PORTS["host"]))
    time.sleep(sleep_for)

    while True:
        try:
            # check connection
            if not myqdrone.connected:
                myqdrone.check_connection()
            else:
                # arm case
                if not myqdrone.armed:
                    if input("Ready to Arm (y/N)? ").lower() == 'y':
                        myqdrone.arm()
                        myqdrone.armed = 1

                # takeoff case
                if myqdrone.armed and not myqdrone.takenoff:
                    if input("Ready to TakeOff (y/N)? ").lower() == 'y':
                        myqdrone.takeoff()
                        myqdrone.takenoff = 1

                # check whether to land or send waypoints/trajectories
                if myqdrone.takenoff:
                    l_in = input("Land or send waypoints (l/w)? ")
                    if l_in.lower() == 'l':
                        myqdrone.land()
                        time.sleep(5)
                        myqdrone.terminate()
                        qlabs_setup.clean_up()
                        break

                    elif l_in.lower() == 'w':
                        myqdrone.activate_waypoint_mode()
                        print("IN WAYPOINT MODE! --> In a separate terminal, run the 'waypoint_commands.py' script")
                        while myqdrone.mode:
                            if input("Press Enter to return to Hover Mode...") == "":
                                print("IN HOVER MODE!")
                                myqdrone.activate_hover_mode()
                                break

        except KeyboardInterrupt:
            # if ctrl+c is pressed and drone is in the air
            print("Mission ABORTED.")
            myqdrone.land() if myqdrone.takenoff else None
            time.sleep(6)
            myqdrone.terminate()
            qlabs_setup.clean_up()
            break


if __name__ == "__main__":
    main()