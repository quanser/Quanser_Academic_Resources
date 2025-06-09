#-----------------------------------------------------------------------------#
#------------------Skills Progression 1 - Task Automation---------------------#
#-----------------------------------------------------------------------------#
#------------------------------Lab 4 - Observer-------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()

# observer.add_display(imageSize = [200, 320, 1],
#                     scalingFactor = 2,
#                     name='Downward Facing Binary')
observer.add_plot(numMeasurements=1680,
                  frameSize=400,
                  pixelsPerMeter=50,
                  scalingFactor=4,
                  name='Leishen M10P Lidar')
observer.add_plot(numMeasurements=410,
                  frameSize=400,
                  pixelsPerMeter=50,
                  scalingFactor=1,
                  name='Plotting')
observer.launch()