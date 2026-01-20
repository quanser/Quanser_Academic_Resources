#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#
#-------------------------Observer to Plot Data-------------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

from pal.utilities.probe import Observer

observer = Observer()

observer.add_scope(numSignals=1, 
                   name='Potentiometer Angle', 
                   signalNames=['Estimated Angle'])

observer.add_scope(numSignals=4,
                   name='Joystick',
                   signalNames=['Potentiometer', 
                                'Joystick X', 
                                'Joystick Y', 
                                'Joystick Button'])



observer.launch()