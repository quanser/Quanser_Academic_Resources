# ---------------------- #
#			 #
# Quanser Infrastructure #
#			 #
# ---------------------- #

For the STEM_Experience, there are three infrastructure servers, namely "STEM_Infrastructure_Main",
"STEM_Infrastructure_V2V", and "STEM_Infrastructure_NN". They had been pre-loaded to the QUARC Run-Time Manager 
Spool running on the STEM windows machine. 

To verify that the traffic light servers are running on the windows machine, open monitor and ensure the target is 
"Local Windows". Once connected, hover the mouse over the monitor icon in the system tray area, and verify that the 
three infrastructure servers are running. If not, batch scripts are provided for different functionalities as 
described below.


To launch the QUARC Server models, run the following batch file: 

	run_infrastructure_models.bat


Similarly, run the following batch files to stop the QUARC Sever models:

	stop_infrastructure_models.bat


To configure the QUARC servers to run automatically on boot/power up, first download the server to the QUARC Manager, 
then enable the QUARC Servers to run on boot, by running the following batch scripts:

	download_infrastructure_models.bat
	enable_run_on_boot_infrastructure_models.bat

In addition, the initial time delay for running server after the complete startup of the windows machine can 
be configured in config.txt in the parent folder.
 

To disable the QUARC Sever model from running on boot, run the following batch script:

	disable_run_on_boot_infrastructure_models.bat

