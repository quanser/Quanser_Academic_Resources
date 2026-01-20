#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#-------------------------Observer to Plot Data-------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()
observer.add_scope(numSignals=1,
                   name='Motor Voltage',
                   signalNames=['Voltage'])
observer.add_scope(numSignals=1,
                   name='Motor Encoder',
                   signalNames=['Encoder counts'])
observer.add_scope(numSignals=1,
                   name='Tachometer (Motor Speed)',
                   signalNames=['Tachometer speed'])
observer.add_scope(numSignals=2,
                   name='Motor Speed Modeling',
                   signalNames=['Measured', 'Modeled'])
observer.launch()