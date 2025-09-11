<img src="docs/images/BannerQCar.png" width="100%">


# Quanser_Academic_Resources
The [Quanser](https://www.quanser.com/) Academic Resources includes the research and teaching content for using Quanser products, including libraries, research examples, teaching content, user manuals, guides and more.

This branch was created so you could download all files that are related to the Self Driving Car Studio which includes the `QCar and QCar 2` and that you can add to your QCar to start developing on the car itself.  If you are looking for resources for your PC, please refer to the [dev-windows](https://github.com/quanser/Quanser_Academic_Resources/tree/dev-windows) branch.

### Table of Contents
- [Downloading Resources](#downloading-resources)
- [Setting Up Your QCar](#setting-up-your-qcar)
- [Getting Started With Content](#getting-started-with-content)
- [Changelog](changelog.txt)


## Downloading Resources

Before getting started with these resources, the first step is to download them, this could be to your PC and then transferring to the QCar or directly to the QCar itself. 

### Downloading directly on the QCar

<details open>
<summary>Downloading to QCar</summary>

1. Connect to a QCar by HDMI cable or remote desktop (see [User Manual Connectivity](3_user_manuals/qcar2/user_manual_connectivity.pdf) for more help). 
2. Make sure to connect your QCar to a network with internet connectivity. You can change the WiFi connection or connect a network cable using the QCar's port.
3. In your QCar, navigate to `home/nvidia/Documents`/`~/Documents`, if you have an existing Quanser folder, either delete it or rename it something else, for example `Quanser_old`.
4. Open your `Documents` directory in terminal and run the following command as shown in the picture below:

    ```
    git clone -b dev-qcar --single-branch https://github.com/quanser/Quanser_Academic_Resources.git Quanser
    ```

    It will create a folder called `Quanser` and download all the necessary files into that folder. 

    <img src="docs/images/git_to_qcar.png" width="500">

5. Continue by following the steps in the next section, [Setting Up Your QCar](#setting-up-your-qcar). 

</details>


### Downloading to your PC first

<details>
<summary>Download to PC</summary>

1. Click the green Code button at the top of this GitHub page, click _Download ZIP_ at the bottom of the menu that pops up. 
2. Unzip the folder in your system. 
3. Go into _Quanser_Academic_Resources-dev-qcar_ (you see the folders 0_libraries, 1_setup ...). 
4. Make sure you can ping your QCar using the IP it shows on its display. 
4. Download or open [WinSCP](https://winscp.net/eng/download.php)
5. Connect and move files using WinSCP to the QCar as follows:
    
    <img src="docs/images/winSCPLogin.png" width="500">

    Where the host name is the IP of the QCar, username and password are `nvidia`.

    Double click the address bar on the left of window to open the directory where your downloaded resources are. 

    <img src="docs/images/winSCPstep2.png" width="500">

    On the right side (the QCar directory side), go to `home/nvidia/Documents` and create a folder called `Quanser`. Copy the files from _Quanser_Academic_Resources-dev-qcar_ into this new folder by dragging and dropping from the left to the right window. 

    <img src="docs/images/winSCPstep3.png" width="650">

    You can now close WinSCP.

</details>


## Setting Up Your QCar

Your QCar comes equipped with the necessary libraries that you might use as part of the existing examples, however, there is one step that you need to complete before starting to use your QCar. 

Connect to a QCar by HDMI cable or remote desktop (see [User Manual Connectivity](3_user_manuals/qcar2/user_manual_connectivity.pdf) for more help). Go into your documents in the QCar into your newly created Documents/Quanser folder from the steps above and go to `1_setup`. Run the  `updatebashrc_qcar2.sh` file located in that folder. It will make sure your QCar is ready for usage. 

## Getting Started With Content

For a comprehensive guide to getting started with these resources for the QCar 2, please refer to the [Getting Started - Labs](docs/start_labs.md) guide.
    
    - Self Driving Car Studio (SDCS):
        - QCar, QCar 2
        - Traffic Light

For information on setup for other products, please refer to the guide in the [dev-windows](https://github.com/quanser/Quanser_Academic_Resources/tree/dev-windows) branch.

