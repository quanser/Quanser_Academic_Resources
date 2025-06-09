from pal.utilities.probe import Observer

observer = Observer()

imageWidth  = 1640
imageHeight = 820
observer.add_display(imageSize = [imageHeight, imageWidth, 3],
						scalingFactor= 4, name="Detection Overlay")
observer.launch()
