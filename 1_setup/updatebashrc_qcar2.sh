#!/bin/bash

BASHRC="$HOME/.bashrc"
LINE1='export PYTHONPATH=$HOME/Documents/Quanser/0_libraries/python'
LINE2='export QAL_DIR=$HOME/Documents/Quanser'

echo "Updating ~/.bashrc if needed..."

# Check if lines already exist in .bashrc, if not, add them
if ! grep -q 'Quanser/0_libraries/python' "$BASHRC"; then
    echo "$LINE1" >> "$BASHRC"
    echo "PYTHONPATH added to ~/.bashrc"
else
    echo "PYTHONPATH already exists in ~/.bashrc"
fi

if ! grep -qxF "$LINE2" "$BASHRC"; then
    echo "$LINE2" >> "$BASHRC"
    echo "QAL_DIR added to ~/.bashrc"
else
    echo "QAL_DIR already exists in ~/.bashrc"
fi


# Installing dependencies if there is an internet connection
if nc -zw1 google.com 443; then
    echo "internet connection identified"
    sudo apt update
    sudo apt install quanser-sdk -y
    sudo apt install python3-setuptools -y
    pip3 install transforms3d
    sudo apt-get install ros-humble-tf-transformations -y
    python3 -m pip install numpy==1.23 --upgrade
    echo "packages were attempted to be installed"
else
    echo "no internet connection found"
    echo "no packages were attempted to be installed"
fi

source $BASHRC
