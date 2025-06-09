#-----------------------------------------------------------------------------#
#------------------Skills Progression 1 - Task Automation---------------------#
#-----------------------------------------------------------------------------#
#------------------------------Lab 1 - Observer-------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()
observer.add_scope(numSignals=4,
                   name='Motor Speed Plot',
                   signalNames=['Left Motor Cmd', 'Right Motor Cmd', 'Left Motor Meas', 'Right Motor Meas'])
observer.add_scope(numSignals=3,
                   name='Body Speed Plot',
                   signalNames=['Foward Speed', 'Turn Speed', 'Gyro Measurement'])
observer.add_display(imageSize = [200, 320, 1],
                    scalingFactor = 2,
                    name='Downward Facing Raw')
observer.launch()