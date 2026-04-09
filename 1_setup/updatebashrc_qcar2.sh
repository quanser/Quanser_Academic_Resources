#!/bin/bash

# Define the lines you want to add
line1="export PYTHONPATH=$PYTHONPATH:/home/nvidia/Documents/Quanser/0_libraries/python"
line2="export QAL_DIR=/home/nvidia/Documents/Quanser"

# Add a newline first (in case file doesn't end with one), then append
printf "\n%s\n%s\n" "$line1" "$line2" >> ~/.bashrc

# TODO: remove when the bug fix is released
# Patch quanserSDK scan match
FILE="/usr/lib/python3/dist-packages/quanser/image_processing/lidar_match_scans.py"
# Patch line 109: add "self"
sudo sed -i '109s/def open(resolution, max_range):/def open(self, resolution, max_range):/' "$FILE"
# Patch line 248: fix "pose"
sudo sed -i '248s/                                                                     ffi.from_buffer(_SINGLE_ARRAY3, pose) if pos is not None else ffi.NULL, ffi.from_buffer(_SINGLE_ARRAY, score) if score is not None else ffi.NULL, ffi.from_buffer(_SINGLE_ARRAY9, covariance) if covariance is not None else ffi.NULL)/                                                                     ffi.from_buffer(_SINGLE_ARRAY3, pose) if pose is not None else ffi.NULL, ffi.from_buffer(_SINGLE_ARRAY, score) if score is not None else ffi.NULL, ffi.from_buffer(_SINGLE_ARRAY9, covariance) if covariance is not None else ffi.NULL)/' "$FILE"

# Installing dependencies
sudo apt install python3-setuptools -y
pip3 install transforms3d
sudo apt-get install ros-humble-tf-transformations -y
python3 -m pip install numpy==1.23 --upgrade
echo "Lines added to .bashrc and changes applied."
# Source the .bashrc to apply changes immediately
source ~/.bashrc