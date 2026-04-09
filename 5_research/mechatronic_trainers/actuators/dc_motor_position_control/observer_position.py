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
                   name='Motor Current',
                   signalNames=['Current'])
observer.add_scope(numSignals=2,
                   name='Motor Position',
                   signalNames=['Measured', 'Desired'])
observer.launch()