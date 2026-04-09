#-----------------------------------------------------------------------------#
#------------------Skills Progression 1 - Task Automation---------------------#
#-----------------------------------------------------------------------------#
#------------------------------Lab 4 - Observer-------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()


observer.add_scope(numSignals=3,
                   name = 'Estimated Pose vs Time')
observer.add_xy_scope(numSignals=2, 
                    name = 'Estimated Pose XY')
observer.add_scope(numSignals=1,
                   name = 'Score')
observer.add_scope(numSignals=1, name = 'Loop Execution Time')
observer.launch()