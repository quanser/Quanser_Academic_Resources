#-----------------------------------------------------------------------------#
#------------------Skills Progression 1 - Task Automation---------------------#
#-----------------------------------------------------------------------------#
#------------------------------Lab 3 - Observer-------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()
observer.add_display(imageSize = [200, 320, 1],
                    scalingFactor = 2,
                    name='Downward Facing Raw')
observer.add_display(imageSize = [50, 320, 1],
                    scalingFactor = 1,
                    name='Downward Facing Binary')
observer.launch()