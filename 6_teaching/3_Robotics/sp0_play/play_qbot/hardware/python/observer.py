#-----------------------------------------------------------------------------#
#-----------------------Skills Progression 0 - Play---------------------------#
#-----------------------------------------------------------------------------#
#------------------------------Lab 1 - Observer-------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()
# observer.add_display(imageSize = [400,640,1],
#                      scalingFactor=2,
#                      name='Downward Facing Image')
observer.add_display(imageSize = [480,640,3],
                     scalingFactor=2,
                     name='RealSense RGB Image')
# observer.add_display(imageSize = [480,640,1],
#                      scalingFactor=2,
#                      name='RealSense Depth Image')
# observer.add_plot(numMeasurements=1680,
#                   frameSize=400,
#                   pixelsPerMeter=50,
#                   scalingFactor=8,
#                   name='Leishen M10P Lidar')
observer.launch()
