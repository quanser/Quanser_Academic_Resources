# Observer to plot raw color sensor data

from pal.utilities.probe import Observer

observer = Observer()
observer.add_scope(numSignals=4,
                   name='Color Sensor',
                #    signalNames=['red','green','blue','clear'])
                   signalNames=['red','clear','green','blue'])                     
observer.launch()