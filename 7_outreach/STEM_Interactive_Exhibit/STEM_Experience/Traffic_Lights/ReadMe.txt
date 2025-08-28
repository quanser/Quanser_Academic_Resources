# --------------------- #
#			#
# Quanser Traffic Light #
#			#
# --------------------- #

For the STEM_Experience, there are two traffic lights, pre-assigned as "20" or "21", based on its pre-assigned IP 
address of 192.168.X.20 or 192.168.X.21, where X is based on the IP gateway of your router. Ensure the IP_GATEWAY 
variable is defined correctly in the config.txt in the parent folder. 

The traffic lights are configured to automatically connect to wireless network with SSID of 'Quanser_UVS'. Ensure
your router is broadcasting the correct SSID, modify if necessary. If changing the SSID of your router is not possible,
please contact Quanser support (tech@quanser.com).

For each traffic light, the corresponding QUARC server model (either "traffic_light_target_20" or traffic_light_target_21") 
had been pre-loaded to the QUARC Run-Time Manager Spool running on the Raspberry Pi Zero. To verify that the traffic light 
servers are running on the Raspberry Pi, open monitor and change target to the IP of the traffic light. Once connected, 
hover the mouse over the monitor icon in the system tray area, and verify that the server is running. If not, batch 
scripts are provided for different functionalities as described below.


To launch the QUARC Server, run the following batch file: 

	run_all_traffic_light.bat


Similarly, run the following batch files to stop the QUARC Sever model:

	stop_all_traffic_light.bat


To configure the QUARC server to run automatically on boot/power up, first download the server to
the Raspberry Pi Zero, then enable the QUARC Server to run on boot, by running the following batch scripts:

	download_traffic_light_servers.bat
	enable_run_on_boot.bat

In addition, the initial time delay for running server after the complete startup of the Raspberry Pi can 
be configured in config.txt in the parent folder.
 

To disable the QUARC Sever model from running on boot, run the following batch script:

	disable_run_on_boot.bat

