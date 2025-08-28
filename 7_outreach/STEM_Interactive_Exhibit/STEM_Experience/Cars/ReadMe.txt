# -------------- #
#       	 #
#  Quanser QCar  #
#		 #
# -------------- #

For the STEM_Experience, there can be up to 5 cars. Ensure their pre-assigned IP addresses are within the range of
192.168.X.11 and 192.168.X.15, where X is based on the IP gateway of your router. Ensure the IP_GATEWAY variable is 
defined correctly in the config.txt in the parent folder. In addition, ensure the correct CAR_TYPE (QCar1 or QCar2, 
case sensitive) is defined in config.txt.

Batch scripts are provided for running STEM the rt models on the QCars, stopping the models, and enable the model to
run on boot. To verify that the models are running on the QCar, open monitor and change target to the IP of the Car. 
Once connected, hover the mouse over the monitor icon in the system tray area, and verify that the model is running.

Before running the models on the cars, reference scans needs to downloaded to the cars. Instruction for this process
can be found in the child folder "reference scan". This process only needs to be done once, before running the STEM
Experience for the very first time.


To launch the models on all cars, run the following batch file: 

	run_car_model.bat


Similarly, run the following batch files to stop the models:

	stop_car_model.bat


To configure the models to run automatically on boot/power up, first download the model to the car, then enable the mode 
to run on boot, by running the following batch scripts:

	download_car_model.bat
	enable_run_on_boot_car_model.bat

In addition, the initial time delay for running server after the complete startup of the QCar can 
be configured in config.txt in the parent folder.
 

To disable the model from running on boot, run the following batch script:

	disable_run_on_boot_car_model.bat

