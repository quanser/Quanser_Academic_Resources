#!/bin/bash

# Line to add to .bashrc
line="export PYTHONPATH=/home/nvidia/Documents/Quanser/0_libraries/python"

# Check if the line is already in the file to avoid duplicates
if ! grep -q "export PYTHONPATH=/home/nvidia/Documents/Quanser/0_libraries/python" ~/.bashrc
then
    # If the line is not in the file, append it
    echo "$line" >> ~/.bashrc
    echo "PYTHONPATH added to ~/.bashrc"
    
    # Source the .bashrc to apply changes immediately
    source ~/.bashrc
else
    echo "PYTHONPATH already exists in ~/.bashrc"
fi


# place any packages that need to be updated here
# check for an internet connection before attempting to install packages
if nc -zw1 google.com 443; then
    echo "internet connection identified"
else
    echo "no internet connection found"
    echo "no packages were attempted to be installed"
fi
