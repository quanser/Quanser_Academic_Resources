from pal.utilities.timing import Timer
from pal.utilities.keyboard import QKeyboard
from src.visualization import VisualizePWM

totalTime = 300 # in seconds. run for 5 minutes

timer = Timer(sampleRate=60.0, totalTime=totalTime)
kbd = QKeyboard()
viz = VisualizePWM(kbd, 30)

while timer.check():
    kbd.update()
    viz.render()
    timer.sleep()
