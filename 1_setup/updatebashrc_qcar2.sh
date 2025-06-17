#!/bin/bash

# Define the lines you want to add
line1="export PYTHONPATH=$PYTHONPATH:/home/nvidia/Documents/Quanser/0_libraries/python"
line2="export QAL_DIR=/home/nvidia/Documents/Quanser"

# Use sed to insert the lines at lines 6 and 7 of .bashrc
sed -i '6i\'"$line1" ~/.bashrc
sed -i '7i\'"$line2" ~/.bashrc

# Source the .bashrc to apply changes immediately
#source ~/.bashrc
python3 -m pip install numpy==1.23 --upgrade
echo "Lines added to .bashrc and changes applied."
