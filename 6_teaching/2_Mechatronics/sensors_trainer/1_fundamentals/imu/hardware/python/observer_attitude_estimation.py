#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#-------------------------Observer to Plot Data-------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()
observer.add_scope(numSignals=5,
                   name='Attitude',
                   signalNames=['Roll Acc (deg)',
                                 'Pitch Acc (deg)',
                                 'Roll Gyro (deg)',
                                 'Pitch Gyro (deg)',
                                 'Yaw Gyro (deg)'])
observer.launch()