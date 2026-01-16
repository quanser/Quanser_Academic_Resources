#!/usr/bin/env bash
# ============================================================
# Python virtual environment setup
# - Creates a venv with access to system site packages
# - Installs required Python packages
#
# User-configurable section is at the top
# ============================================================

set -e  # Exit immediately if any command fails

# Ensure script runs relative to the user's home directory
cd "$HOME"

# ------------------------------------------------------------
# USER CONFIGURATION
# ------------------------------------------------------------

# Base directory where the venv will live
VENV_BASE_DIR="$HOME"

# Name of the virtual environment
VENV_NAME="trainers"

# Full path to the virtual environment
VENV_PATH="$VENV_BASE_DIR/$VENV_NAME"

# ------------------------------------------------------------
# 1. Create directory for virtual environments
# ------------------------------------------------------------

echo "Creating venv base directory if it does not exist..."
mkdir -p "$VENV_BASE_DIR"

# ------------------------------------------------------------
# 2. Create the virtual environment
#    --system-site-packages allows access to apt-installed
#    Python packages (e.g., python3-quanser-apis)
# ------------------------------------------------------------

if [ -d "$VENV_PATH" ]; then
    echo "Virtual environment already exists at:"
    echo "  $VENV_PATH"
else
    echo "Creating virtual environment at:"
    echo "  $VENV_PATH"
    python3 -m venv --system-site-packages "$VENV_PATH"
fi

# ------------------------------------------------------------
# 3. Activate the virtual environment
# ------------------------------------------------------------

echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# ------------------------------------------------------------
# 4. Upgrade pip and install Python packages
# ------------------------------------------------------------

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing Python dependencies..."
pip install \
    sounddevice \
    soundfile \
    #pygit 


# If you later add a requirements.txt, you can replace the
# above with:
# pip install -r requirements.txt

echo "=== Virtual environment setup complete ==="
echo "To activate this venv in the future, run:"
echo "  source $VENV_PATH/bin/activate"