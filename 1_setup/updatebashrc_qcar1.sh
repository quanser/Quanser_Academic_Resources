#!/bin/bash

# Lines to add to .bashrc
BASHRC="$HOME/.bashrc"
LINE1='export PYTHONPATH="$HOME/Documents/Quanser/0_libraries/python"'
LINE2='export QAL_DIR="$HOME/Documents/Quanser"'

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

# place any packages that need to be updated here
# check for an internet connection before attempting to install packages
if nc -zw1 google.com 443; then
    echo "internet connection identified"
    #echo "packages were attempted to be installed"
else
    echo "no internet connection found"
    #echo "no packages were attempted to be installed"
fi

source $BASHRC