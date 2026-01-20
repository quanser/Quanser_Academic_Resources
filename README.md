<img src="docs/images/quanser-resources-header.png" width="100%">


# Quanser_Academic_Resources
The [Quanser](https://www.quanser.com/) Academic Resources includes the research and teaching content for using Quanser products, including libraries, research examples, teaching content, user manuals, guides and more.

This repository includes content for the following products: `Aero 2, Mechatronic Actuators Trainer, Mechatronic Sensors Trainer, QArm, QArm Mini, QBot Platform and older QBots, QCar, QCar 2, QDrone, QDrone 2, Qube-Servo 3`, and looking for resources on these solutions from [Quanser's website](https://www.quanser.com/) will redirect here. If you are looking for resources to other products, skip these instructions and refer to the section [Resources For Older Products](#resources-for-older-products).

### Table of Contents
- [Downloading Resources](#downloading-resources)
- [Setting Up Your Computer](#setting-up-your-computer)
- [Getting Started With Content](#getting-started-with-content)
- [Resources For Older Products](#resources-for-older-products)
- [Changelog](changelog.txt)


## Downloading Resources

**Note:** If you are trying to set up a Raspberry Pi (4 or 5) to use with the Mechatronic Actuators Trainer and/or the Mechatronic Sensors Trainer, skip this guide and see [Raspberry Pi Setup](1_setup/raspberry_pi/pi_setup.pdf). These devices work both in Windows computers and Raspberry Pis.

Before getting started with these resources, the first step is to download them into your computer. There is two ways to do this, using Git, or downloading the files simply as a .zip file. We recommend having our resources in a `C:/Users/user/Documents/Quanser` folder.

### With Git

<details open>
<summary>Installation using Git</summary>

1. Install [Git](https://git-scm.com/downloads) in your system.
2. Open your Documents folder and open a windows terminal in that folder.
3. Run the following command to create the Quanser directory and copy the contents of this repo in there.
    ```
    git clone https://github.com/quanser/Quanser_Academic_Resources.git Quanser
    ```

</details>

### Without Git

<details>
<summary>Installation without Git</summary>

1. On your system, create a folder called _Quanser_ under _Documents_. This should look like `C:/Users/user/Documents/Quanser`.
2. Click the green Code button at the top of this GitHub page, click _Download ZIP_ at the bottom of the menu that pops up.
3. Unzip the folder in your system.
4. Go into _Quanser_Academic_Resources-main_ (you see the folders 0_libraries, 1_setup ...). Copy all the contents of that folder into your newly created Documents/Quanser folder.
</details>

## Setting Up Your Computer

To begin using these resources, you will need to install the necessary software to your computer based on your intended method of interfacing with Quanser devices. This may involve working with either virtual and/or hardware systems, and utilizing Python and/or MATLAB/Simulink.

- Follow the setup guide: [Computer Setup](docs/pc_setup.md).

- Note that if a router was provided as part of your system: please DO NOT connect an internet cable to the router, this may cause unexpected behavior due to automatic router firmware updates.

## Getting Started With Content

For a comprehensive guide to getting started with these resources and using your Quanser products, follow [Getting Started With Content](docs/getting_started.md). 


# Resources For Older Products

 **_For any other product not listed above, please visit the Quanser Website for [resources](https://www.quanser.com/resources/)._**
