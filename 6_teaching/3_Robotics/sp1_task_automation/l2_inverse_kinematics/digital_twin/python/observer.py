#-----------------------------------------------------------------------------#
#------------------Skills Progression 1 - Task Automation---------------------#
#-----------------------------------------------------------------------------#
#------------------------------Lab 2 - Observer-------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()
observer.add_display(imageSize = [200, 320, 1],
                    scalingFactor = 2,
                    name='Downward Facing Raw')
observer.add_scope(numSignals=4, 
                   name='Motor Speed Plot', 
                   signalNames=['Left Wheel Cmd', 'Right Wheel Cmd','Left Wheel Meas','Right Wheel Meas'])
observer.add_scope(numSignals=3, 
                   name='Body Speed Plot', 
                   signalNames=['Forward Speed', 'Turn Speed', 'Gyro Measurement'])
observer.launch()