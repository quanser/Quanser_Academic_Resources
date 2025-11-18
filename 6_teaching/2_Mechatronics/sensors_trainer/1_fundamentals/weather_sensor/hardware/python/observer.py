#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#-------------------------Observer to Plot Data-------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()
observer.add_scope(numSignals=1,
                   name='Temperature',
                   signalNames=['Temperature (°C)'])
observer.add_scope(numSignals=1,
                   name='Pressure',
                   signalNames=['Pressure (Pa)'])
observer.add_scope(numSignals=1,
                   name='Humidity',
                   signalNames=['Humidity (%)'])
observer.add_scope(numSignals=1,
                   name='Altitude Above Sea Level',
                   signalNames=['Altitude (m)'])
observer.launch()