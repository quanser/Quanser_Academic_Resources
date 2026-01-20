#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#-------------------------Observer to Plot Data-------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()
observer.add_scope(numSignals=3,
                   name='Gyroscope',
                   signalNames=['X (deg/s)', 'Y (deg/s)', 'Z (deg/s)'])
observer.add_scope(numSignals=3,
                   name='Accelerometer',
                   signalNames=['X (m/s^2)', 'Y (m/s^2)', 'Z (m/s^2)'])
observer.launch()