from pal.utilities.probe import Observer

observer = Observer()

for i in range(4):
    observer.add_display(imageSize = [410,820,3],
                        scalingFactor=2,
                        name='CSI'+str(i))

observer.launch()
