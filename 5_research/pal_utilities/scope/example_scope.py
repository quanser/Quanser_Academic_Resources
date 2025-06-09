#region General Setup, unrelated to scope
# General package imports.
from threading import Thread
import numpy as np
import signal
import time
# Setup to enable killing the data generation thread using keyboard interrupts
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)
#endregion

# Import required for using one or more of the three scope classes
from pal.utilities.scope import Scope, XYScope, MultiScope

#region MultiScope Example
multiScope = MultiScope(
    rows=2,
    cols=2,
    title="MultiScope Example",
    fps=30
)

multiScope.addAxis(row=0, col=0, timeWindow=5, yLabel='X Position (m)')
multiScope.axes[0].attachSignal(name='s1')
multiScope.axes[0].attachSignal(name='s2')

multiScope.addAxis(
    row=1,
    col=0,
    timeWindow=5,
    xLabel='Time (s)',
    yLabel='Y Position (m)'
)
multiScope.axes[1].attachSignal()
multiScope.axes[1].attachSignal(color=[85,168,104])

multiScope.addXYAxis(
    row=0,
    col=1,
    rowSpan=2,
    xLabel='X (m)',
    yLabel='Y (m)',
    xLim=(-4, 4),
    yLim=(-4, 4)
)
multiScope.axes[2].attachSignal(color=[76,114,176], width=5, lineStyle=':')

multiScope.axes[2].attachImage(
    scale=(8/5, -8/5),
    offset=(-2.5, -2.5),
    rotation=0, # rotation angle in degrees
    levels=(0, 2) # (blackValue, whiteValue)
)
im = np.eye(5)
im[0,0] = 0
im[0,1] = 1.5
multiScope.axes[2].images[0].setImage(im)
#endregion

#region Scope Example
scope = Scope(
    title='Scope Example',
    timeWindow=5,
    xLabel='Time (s)',
    yLabel='X Position (m)'
)
scope.attachSignal(name='s1')
scope.attachSignal(name='s2')
#endregion

#region XYScope Example
xyScope = XYScope(
    title="XYScope Example",
    xLabel='X (m)',
    yLabel='Y (m)',
    xLim=(-4, 4),
    yLim=(-4, 4)
)
xyScope.attachSignal(color=[76,114,176], width=5, lineStyle=':')

xyScope.attachImage(
    scale=(8/5, -8/5),
    offset=(-2.5, -2.5),
    rotation=0, # rotation angle in degrees
    levels=(0, 2) # (blackValue, whiteValue)
)
im = np.eye(5)
im[0,0] = 0
im[0,1] = 1.5
xyScope.images[0].setImage(im)
#endregion


def control_loop():
    #region setup for control_loop, unrelated to scope
    n = 2
    w = 2*np.pi /2
    t0 = time.time()
    t = 0
    tf = 20
    i = 0
    n=2
    #endregion

    while (t <= tf) and (not KILL_THREAD):
        #region Generate data samples, unrelated to scope
        t = time.time() - t0
        i += 1
        data = []
        for j in range(n):
            data.append(np.sin(t*w + j/n*np.pi))
        x = np.log(t+1) * np.cos(t*w)
        y = np.log(t+1) * np.sin(t*w)
        #endregion

        #region Add data samples to multiScope
        multiScope.axes[0].sample(t, [data[0], data[0]-0.2])

        if np.mod(i,20) == 0:
            multiScope.axes[1].sample(t, [data[0], data[0]-0.2])

        multiScope.axes[2].sample(t, [[x,y]])
        #endregion

        # Add samples to scope
        scope.sample(t, [data[0], data[0]-0.2])

        # Add samples to xyScope
        xyScope.sample(t, [[x,y]])

        time.sleep(0.01)


# Setup data generation thread and run until complete
thread = Thread(target=control_loop)
thread.start()

while thread.is_alive() and (not KILL_THREAD):

    # This must be called regularly or the scope windows will freeze
    # Must be called in the main thread.
    MultiScope.refreshAll()
    # Can also use Scope.refreshAll() or XYScope.refreshAll() instead.
    # All perform the same function. Only one needs to be called.

    time.sleep(0.01)

input('Press the enter key to exit.')