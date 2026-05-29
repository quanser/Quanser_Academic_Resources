<img src="../docs/images/quanser-resources-header.png" width="100%">
<p align="right" style="font-size: 1.2em;"><a href="../README.md#getting-started-with-content"><sup>Back To Guide</sup></a>
<br/></p>

<a name="top"></a>

# 1_setup folder

The 1_setup folder serves two purposes:
1. It contains setup guides for various Quanser Labs.
2. It contains the files required to configure a computer for use with the Quanser Resources (this repository).

This guide covers the files described in point 2 above.

The following three files are used during computer setup:
1. [step_1_check_requirements.bat](#reqs)

The following files are used depending on the configuration required:

2. [configure_matlab.bat](#matlab)
3. [configure_python.bat](#python)


<a id="reqs"></a>

## step_1_check_requirements.bat

This script checks which Quanser software is installed on your system and determines which of the four supported configurations your machine can run. It must be run before `configure_matlab.bat` or `configure_python.bat`.

It opens the [PC Setup Guide](../docs/pc_setup.md#downloading-resources) in a browser, then does the following:

1. **Checks for installed software** -- detects whether QUARC, Quanser SDK (QSDK), Quanser Interactive Labs (QLabs), MATLAB/Simulink (R2018a through R2026a), Visual Studio (2015 through 2022), and Python (3.11 through 3.14) are present on the machine.

2. **Displays a requirements table and a system state table** -- shows which software is required for each supported configuration, then shows what is currently installed on your machine.

3. **Reports which configurations your system supports** -- lists which of the four configurations (MATLAB Hardware, MATLAB Virtual, Python Hardware, Python Virtual) are available based on what was detected.

4. **Logs the system state to `software_requirements.log`** -- the configure scripts read this file as a reference during setup. If any software is installed or removed after this check, re-running this script is recommended to update the log.

The four supported configurations and their software requirements are:

| | QUARC | QSDK | QLabs | MATLAB/Simulink | Python |
|---|:---:|:---:|:---:|:---:|:---:|
| MATLAB Hardware | 1 | - | - | 1 | - |
| MATLAB Virtual | 0 | - | 1 | 1 | - |
| Python Hardware | - | 1 | - | - | 1 |
| Python Virtual | - | 1 | 1 | - | 1 |

Note that if you are using both MATLAB/Simulink and Python with Quanser's hardware, you only need the QUARC software -- it installs Quanser SDK (QSDK) which supports Python.


<a id="matlab"></a>

## configure_matlab.bat

This file reads the `software_requirements.log` produced by `step_1_check_requirements.bat` and configures your system for MATLAB/Simulink usage. It must be run after step 1.

It checks that MATLAB is installed (required) and warns if QUARC or Quanser Interactive Labs are missing, then does the following to your system:

1. **Sets two persistent Windows environment variables** (via `setx`, so they survive reboots):
    - `QAL_DIR` -- points to `%USERPROFILE%\Documents\Quanser`, the root of the Quanser resources folder.
    - `RTMODELS_DIR` -- points to `%USERPROFILE%\Documents\Quanser\0_libraries\resources\rt_models`, used to locate real-time models.

2. **Adds the Quanser MATLAB library to MATLAB's persistent path** -- it scans `C:\Program Files\MATLAB` for all installed MATLAB versions (R2019a through R2026a) and, for each one found, launches MATLAB in batch mode to run `addpath` and `savepath`, so the `0_libraries/matlab` folder is available in every future MATLAB session without manual path setup.

A machine restart is required for the environment variable changes to take effect.


<a id="python"></a>

## configure_python.bat

This file reads the `software_requirements.log` produced by `step_1_check_requirements.bat` and configures your system for Python usage. It must be run after step 1.

It checks that Python and QUARC or Quanser SDK are installed and warns if Quanser Interactive Labs is missing, then does the following to your system:

1. **Installs the Quanser Python API** -- locates the `quanser_api` wheel file in the SDK directory and installs it (plus upgrades pip) using the detected Python version. The detected Python version will always be the latest one installed in your system up to Python 3.14.

2. **Installs additional Python packages** -- runs `pip install -r requirements.txt` to install all other packages needed by the Quanser resources. The list of requirements is located in `requirements.txt` in this folder.

3. **Sets persistent Windows environment variables** (via `setx`):
    - `QAL_DIR` -- points to `%USERPROFILE%\Documents\Quanser`, the root of the Quanser resources folder.
    - `RTMODELS_DIR` -- points to `%USERPROFILE%\Documents\Quanser\0_libraries\resources\rt_models`, used to locate real-time models.
    - `PYTHONPATH` -- adds `%USERPROFILE%\Documents\Quanser\0_libraries\python` so the Quanser Python libraries are importable from any project without manual path setup. If `PYTHONPATH` already exists, the path is appended rather than replaced.

A machine restart is required for the environment variable changes to take effect.



<p align="left" style="font-size: 1.3em;"><a href="#"><sup>Back to Top</sup></a>
<br/></p>
