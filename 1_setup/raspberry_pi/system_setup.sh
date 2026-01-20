#!/usr/bin/env bash
# ============================================================
# System setup script for Raspberry Pi
# - Updates system packages
# - Adds environment variables to ~/.bashrc
# - Installs Quanser SDK and Python APIs
# ============================================================

set -e  # Exit immediately if any command fails

echo "=== Starting system setup ==="

# Ensure script runs relative to the user's home directory
cd "$HOME"

# ------------------------------------------------------------
# 1. Add required lines to ~/.bashrc (safe to run multiple times)
# ------------------------------------------------------------

BASHRC="$HOME/.bashrc"

LINE1='export PYTHONPATH=$PYTHONPATH:$HOME/Documents/Quanser/0_libraries/python'
LINE2='export QAL_DIR=$HOME/Documents/Quanser'

echo "Updating ~/.bashrc if needed..."

# Only add if not already present
if ! grep -qxF "$LINE2" "$BASHRC"; then
    sed -i "1i$LINE2" "$BASHRC"
fi
if ! grep -qxF "$LINE1" "$BASHRC"; then
    sed -i "1i$LINE1" "$BASHRC"
fi

# Apply changes for this script execution
# (new terminals will pick this up automatically)
source "$BASHRC"

# ------------------------------------------------------------
# 2. Update system and install base dependencies
# ------------------------------------------------------------

echo "Updating system package lists..."
sudo apt update

echo "Installing base dependencies..."
sudo apt install -y \
    wget \
    ca-certificates \
    gnupg \
    python3-venv \
    python3-numpy \
    python3-bitarray \
    dkms \
    python3-pip

# ------------------------------------------------------------
# 3. Configure Quanser SDK repository and install the SDK
# ------------------------------------------------------------

echo "Configuring Quanser SDK repository..."


CONFIG_SCRIPT="configure_raspbian64_repo_prerelease.sh"
# once released
#CONFIG_SCRIPT="configure_raspbian64_repo_release.sh" 
MARKER_FILE="$HOME/.quanser_repo_configured"

if [ ! -f "$MARKER_FILE" ]; then
    # public release
    # wget --no-cache https://repo.quanser.com/debian/release/config/configure_raspbian64_repo_release.sh
    # public prerelease
    wget --no-cache https://repo.quanser.com/debian/prerelease/config/configure_raspbian64_repo_prerelease.sh

    chmod u+x "$CONFIG_SCRIPT"
    ./"$CONFIG_SCRIPT"

    # mark as done
    touch "$MARKER_FILE"

    rm -f "$CONFIG_SCRIPT"
fi

echo "Updating package lists after repo configuration..."
sudo apt update

echo "Installing Quanser SDK and Python APIs..."
sudo apt install -y quanser-sdk python3-quanser-apis

# update the xpad kernel driver to use sensors as a gamepad
echo "Updating xpad..."

if dkms status | grep -q "xpad/0.4"; then
    echo "xpad 0.4 already installed, skipping."
else
    sudo git clone https://github.com/drmadill/xpad.git /usr/src/xpad-0.4 -b add-quanser-controllers
    sudo dkms install -m xpad -v 0.4
fi

echo "Installing additional libraries..."
sudo apt update
sudo apt install -y \
    libportaudio2 \
    python3-opencv \
    python3-pyqt6 \
    python3-pyqtgraph \
    qt6-wayland \
    python3-scipy \
    python3-matplotlib \
    python3-pandas \
    joystick \
    code


# ------------------------------------------------------------
# 4. Add PyQt6 environment fixes to ~/.profile (for GUI apps)
# ------------------------------------------------------------
PROFILE="$HOME/.profile"

PYQT_LINES=(
    'export QT_QPA_PLATFORM=xcb'
    'unset QT_QPA_PLATFORMTHEME'
    'export QT_STYLE_OVERRIDE=fusion'
)

# echo "Updating ~/.profile with PyQt6 settings if needed..."
# for LINE in "${PYQT_LINES[@]}"; do
#     if ! grep -qxF "$LINE" "$PROFILE"; then
#         echo "$LINE" >> "$PROFILE"
#     fi
    
#     # Apply immediately for the current shell
#     # Remove leading 'export' for eval if necessary
#     if [[ "$LINE" == export* ]]; then
#         eval "$LINE"
#     else
#         # For 'unset' lines
#         eval "$LINE"
#     fi

# done

XSESSIONRC="$HOME/.xsessionrc"

echo "Updating ~/.xsessionrc with PyQt6 settings if needed..."
for LINE in "${PYQT_LINES[@]}"; do
    if ! grep -qxF "$LINE" "$XSESSIONRC" 2>/dev/null; then
        echo "$LINE" >> "$XSESSIONRC"
    fi
done

echo "NOTE: PyQt GUI changes take effect on next VNC/desktop login."

# ------------------------------------------------------------
# 5. Opening VS Code and Finalizing Setup
# ------------------------------------------------------------


echo "Opening VS Code"
code

sudo chmod 0700 /run/user/1000


echo "=== System setup complete ==="
echo "You may want to open a new terminal before continuing."
