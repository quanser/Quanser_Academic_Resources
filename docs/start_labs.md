<img src="images/quanser-resources-header.png" width="100%">
<p align="right"><a href="../README.md#getting-started-with-content"><sup>Back To Guide</sup></a>
<br/></p>

# Getting Started With Quanser Lab Products

This guide walks you through getting started with the following labs/products: 

- [Autonomous Vehicles Research Studio (AVRS)](#avrs): 
    - QDrone, QDrone 2, QBot 2, QBot 2e
- [Mobile Robotics Lab (MRL)](#mrl):
    - QBot Platform, QArm Mini
- [Self Driving Car Studio (SDCS)](#sdcs):
    - QCar, QCar 2

- [Quanser's Directory Structure](#directory-structure)

If  your product is not listed above, use the [Getting Started - Others](start_others.md) guide. 


## AVRS

The Autonomous Vehicle Research Studio (AVRS) is a research only lab that mainly uses MATLAB/Simulink as the development environment. The steps to get started after having set up your computer are as follows:

1. Go through the setup steps located in `1_setup/autonomous_vehicles_research_studio`.

2. Go through the user manual of the device you are using, located under `3_user_manuals`, for more detailed information on using the device. 
3. Find available examples under `5_research/autonomous_vehicles` for the device you are using. 

For a more detailed description of the provided file directory, go to the [Directory Structure](#directory-structure) section.

**Note:** If needed, use the [Simulink Onramp](https://matlabacademy.mathworks.com/details/simulink-onramp/simulink), for help getting started with Simulink, or the [QUARC Demos](https://docs.quanser.com/quarc/documentation/quarc_demos.html) for help getting started with Quanser's QUARC. 

[Back to Top](#)   |   [Back to Guide](../README.md#getting-started-with-content)


## MRL

The Mobile Robotics Lab (MRL) is a teaching and research lab for mobile robots. The steps to get started after having set up your computer are as follows:

1. Go through the welcome guide located in `1_setup/mobile_robotics`.

2. Run through the quick start guides of the products you have to make sure your hardware is functioning as expected. These files are located under `2_quick_start_guides/qbot_platform` and `2_quick_start_guides/qarm_mini` and are separated by hardware and virtual devices as well as by programming language (MATLAB/Python). Note that also individual IO tests are located in the product folder under `5_research`.
3. Review the User Manuals under `3_user_manuals/`, these will guide you through how to use your system, including interfacing of hardware and software. 
4. If you are using the systems for research, content is located under `5_research` under individual product folders. This content includes MATLAB, Python and ROS examples. 
5. If you are using the systems for teaching, content is located under `6_teaching/3_Robotics`. The content for each of the products is shown below as well as their corresponding skills progressions. 

    <img src="images/mrl_teaching.png" width="650">

For a more detailed description of the provided file directory, go to the [Directory Structure](#directory-structure) section.

**Note:** If needed, use the [Simulink Onramp](https://matlabacademy.mathworks.com/details/simulink-onramp/simulink), for help getting started with Simulink, or the [QUARC Demos](https://docs.quanser.com/quarc/documentation/quarc_demos.html) for help getting started with Quanser's QUARC. 

[Back to Top](#)   |   [Back to Guide](../README.md#getting-started-with-content)

## SDCS

The Self Driving Car Studio (SDCS) is a teaching and research lab for self driving using QCar. The steps to get started after having set up your computer are as follows:

1. Go through the welcome guide located in `1_setup/self_driving_car_studio`.

2. If you have QCar 2, run through the quick start guide  to make sure your hardware is functioning as expected. These files are located under `2_quick_start_guides/qcar2`. Note that also individual IO tests are located in the product folder under `5_research`.
3. Review the User Manuals under `3_user_manuals/`, read the user manuals for your QCar version (qcar or qcar2), as well as the user manual for the traffic light if you are going to be using it with your system. These will guide you through how to use your system, including interfacing of hardware and software. 
4. If you are using the systems for research, content is located under `5_research/sdcs`, it will have IO and research examples for all products of this lab. This content includes MATLAB, Python and ROS examples. Note that the full self driving examples are part of the teaching content.
5. If you are using the systems for teaching, content is located under `6_teaching/3_Robotics`. The self driving content available as part of skills progressions is shown below.

    <img src="images/sdcs_content.png" width="500">

For a more detailed description of the provided file directory, go to the [Directory Structure](#directory-structure) section.

**Note:** If needed, use the [Simulink Onramp](https://matlabacademy.mathworks.com/details/simulink-onramp/simulink), for help getting started with Simulink, or the [QUARC Demos](https://docs.quanser.com/quarc/documentation/quarc_demos.html) for help getting started with Quanser's QUARC. 

[Back to Top](#)   |   [Back to Guide](../README.md#getting-started-with-content)


## Directory Structure

Quanser content is subdivided into a series of directories to help you get started quickly. 

<img src="images/quanser_content.png" width="450">

- **0_libraries**: Source location for custom Python/Simulink libraries, as well as other useful files used in the libraries. Please review `libraries_guide` inside the libraries folder for more information.

- **1_setup**: Setup for different lab products. 
- **2_quick_start_guides**: Standalone Quick Start Guides for various products. 
- **3_user_manuals**: PDF files of user manuals for different Quanser products.
- **4_concept_reviews**: Consists of .docx/.pdf files for background concepts utilized in Quanser Curriculum.
- **5_research**: Research and IO examples and in either Simulink/Python/ROS for different solutions provided by Quanser. (previously "examples" folder) 
- **6_teaching**: Curriculum/lab content for various Quanser products for hardware or digital twins. 

[Back to Top](#)   |   [Back to Guide](../README.md#getting-started-with-content)
