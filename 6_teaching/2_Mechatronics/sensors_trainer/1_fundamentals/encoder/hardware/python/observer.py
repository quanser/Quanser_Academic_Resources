#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#-------------------------Observer to Plot Data-------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()
observer.add_scope(numSignals=2,
                   name='Encoder Pulses',
                   signalNames=['A Pulse', 'B Pulse'])
observer.add_scope(numSignals=1,
                   name='Encoder Counts',
                   signalNames=['Encoder Counts'])
observer.launch()