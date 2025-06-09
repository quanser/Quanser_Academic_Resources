#!/bin/bash

ls -l /dev |grep ttyTHS2
sudo chmod 666 /dev/ttyTHS2
source /opt/ros/melodic/setup.bash
source ~/ros1/devel/setup.bash
roslaunch qcar slam.launch
