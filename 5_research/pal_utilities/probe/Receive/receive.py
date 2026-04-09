#-----------------------------------------------------------------------------#
# receive.py
#-----------------------------------------------------------------------------#
# This script is used in several examples that show how to stream, receive, and 
# display data using probe and observer module that includes support for 
# Displays (for video data), Plots (standard polar plot as an image), Scope 
# (standard time series plotter), and XY Scope(Real-time display of 2D signals)  

# Follow the steps in each example to run them
from pal.utilities.probe import Observer

'''
TEST NUMBER corresponds to the example you want to run.
1) probeSendImages.py  
2) probeSendLidar.py
3) probeSendDoubles.py  
4) probeSendXY.py
5) probeSendMulti.py 

NOTE: Make sure the last test case is always the probeSendMulti.py example, which includes all the different types of displays, plots, and scopes. 
This will allow you to test all the different implementations at once. Update the last test case with new implementations as they are added to the probe and observer module.

Add different test cases for new implementations to test inside the Observer class. 
Make sure to add the corresponding case in the match statement below and to open the correct display, plot, or scope in the receive.py script.
'''
TEST_NUMBER = 5 
observer = Observer()
# Image Parameters
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
IMAGE_CHANNELS = 3

match TEST_NUMBER:
    case 1:
        observer.add_display(imageSize = [IMAGE_HEIGHT,IMAGE_WIDTH,IMAGE_CHANNELS],
                scalingFactor=2,
                name='My Image 1') # for probeSendImages.py
        
        print("Test case for probeSendImages.py example")
    
    case 2:

        observer.add_plot(numMeasurements=1680,
                    frameSize=400,
                    pixelsPerMeter=50,
                    name='My Lidar 1') # for probeSendLidar.py 

        print("Test case for probeSendLidar.py example")
    
    case 3:

        observer.add_scope(numSignals=2,
                    name='My Scope 1') # for probeSendDoubles.py
        observer.add_scope(numSignals=2,
                    name='My Scope 2') # for probeSendDoubles.py

        print("Test case for probeSendDoubles.py example")
    
    case 4:
        observer.add_xy_scope(numSignals=2,
                            name='My XY Scope', 
                            xLabel='x label', 
                            yLabel = 'y data',
                            xLim = (-3,3),
                            yLim = (-3,3)) # for probeSendXY.py
        print("Test case for probeSendXY.py example")
    
    case 5:
        
        observer.add_display(imageSize = [IMAGE_HEIGHT,IMAGE_WIDTH,IMAGE_CHANNELS],
        scalingFactor=2,
        name='large image')
        
        observer.add_display(imageSize = [IMAGE_HEIGHT,IMAGE_WIDTH,IMAGE_CHANNELS],
        scalingFactor=2,
        name='small image')

        observer.add_plot(numMeasurements=1680,
                    frameSize=400,
                    pixelsPerMeter=50,
                    name='My Lidar 1')
        
        observer.add_plot(numMeasurements=1680,
                    frameSize=400,
                    pixelsPerMeter=50,
                    name='big lidar')
        
        observer.add_plot(numMeasurements=1680,
                    frameSize=400,
                    pixelsPerMeter=50,
                    name='small lidar')
        
        observer.add_scope(numSignals=2,
            name='My Scope 1') 
        
        observer.add_scope(numSignals=2,
            name='My Scope 2') 

        observer.add_xy_scope(numSignals=2,
                            name='My XY Scope', 
                            xLabel='x label', 
                            yLabel = 'y data',
                            xLim = (-3,3),
                            yLim = (-3,3))

observer.launch()
