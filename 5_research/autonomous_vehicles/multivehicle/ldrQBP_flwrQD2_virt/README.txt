Instructions to run this example:

1. Open QLabs and then open the warehouse environment under QDrone2, QBotPlatform or Open World.

2. Run the setup_python.py script to spawn the virtual QDrone2 and virtual QBot Platform.

3. Open two MATLAB sessions, in one session, open the Mission Server Model,
depending on whether using JOYSTICK or not, run either the MS_QD2_QBP_joystick_R2023.slx or MS_QD2_QBP_manual_R2023.slx.

4. In the second MATLAB session, open and run the QD2_DroneStack_PID_virt_R2023.slx model. 

5. Follow the instructions in the mission server model. Use the Joystick (if available) or the manual switches 
in the mission server model to start the demo. 
After the drone is Armed and taken off, the Start_Follow switch is used to start the follow operation where
the QBot Platform is a leader and the QDrone2 is a follower.