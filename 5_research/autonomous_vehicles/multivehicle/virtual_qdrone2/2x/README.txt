Instructions for Running the Example with 2 virtual QDrones

Prerequisites:
    Ensure you have installed the Quanser Python API. The ideal way
    to install this is via the Research Resources zip which you should have received.
    If you have any problems, please reach out to tech@quanser.com.

1. Start Quanser Interactive Labs, and select the 'Warehouse' workspace under 'QDrone2'.

2. Open MATLAB/Simulink and set the current folder as your working directory.

3. Now open and Run the 'MControl.slx' simulink model. This will start the Mission Controller. Ensure that you have setup your
Radio Transmitter and Receiver correctly, ideally you need the transmitter to Arm/TakeOff.

4. Run the 'run_example_2x_QDrone2.bat' file.

5. Use the Radio Transmitter to Arm and Take Off the virtual QDrone2. You can then use the manual switches in the 'MControl.slx' for controlling
the Mission. When you land the drone, ensure to stop the 'MControl.slx' model.

6. When done, run the 'clean_all.bat' file to close any open consoles and stop the spawn models.

Note that for this example, the RT files for the stabilizer have been precompiled with HIL port numbers 18981 for the first drone
and 18991 for the second drone so that the Simulink stabilizer model files have the name convention "DStack_hilport.slx". So drone 0
has simulink file "DStack_18981.slx" and RT model file "DStack_18981.rt-win64".
