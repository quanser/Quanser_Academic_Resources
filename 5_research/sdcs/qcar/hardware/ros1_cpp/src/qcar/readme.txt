1. Put the files in C++ libraries under /opt/quanser/hil_sdk/include. If there is no hil_sdk/include directory open the terminal and run the following command: 
	sudo mkdir /opt/quanser/hil_sdk/include
The /opt/quaser directory does not allow for you to copy files manually, navigate to the location of the C++ libraries folder and copy the files using the following command: 
	sudo cp *.h /opt/quanser/hil_sdk/include

2. Modify the CMakelist in the qcar directory with the CMakelist provided here (noted that direct copy and replace might not work)

3. Replace the package.xml file in the ros1/src/qcar directory with the one provided here
