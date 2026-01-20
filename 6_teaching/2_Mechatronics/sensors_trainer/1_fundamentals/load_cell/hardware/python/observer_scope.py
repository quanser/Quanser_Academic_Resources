# Observer to plot load cell raw data#

from pal.utilities.probe import Observer

observer = Observer()
observer.add_scope(numSignals=1,
                   name='Load Cell',
                   signalNames=['Load Cell (V)'],)
observer.launch()