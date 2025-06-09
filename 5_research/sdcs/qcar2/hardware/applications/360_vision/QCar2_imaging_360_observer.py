from pal.utilities.probe import Observer

observer = Observer()

imageWidth = 640
imageHeight = 480
observer.add_display(imageSize = [imageHeight + 40, 4*imageWidth + 120, 3],
                    scalingFactor=2,
                    name='360 CSI')

observer.launch()
