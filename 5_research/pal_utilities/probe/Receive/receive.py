from pal.utilities.probe import Observer

# Image Parameters
imageWidth = 640
imageHeight = 480
imageChannels = 3

observer = Observer()
observer.add_display(imageSize = [imageHeight,imageWidth,imageChannels],
                     scalingFactor=2,
                     name='My Image 1')
observer.add_display(imageSize = [imageHeight,imageWidth,imageChannels],
                     scalingFactor=4,
                     name='My Image 2')
observer.add_plot(numMeasurements=1680,
                  frameSize=400,
                  pixelsPerMeter=50,
                  name='My Lidar 1')
observer.add_plot(numMeasurements=1680,
                  frameSize=300,
                  pixelsPerMeter=20,
                  name='My Lidar 2')
observer.add_scope(numSignals=2,
                   name='My Plot 1')
observer.add_scope(numSignals=2,
                   name='My Plot 2')

observer.launch()
