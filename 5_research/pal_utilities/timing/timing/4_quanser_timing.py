#-----------------------------------------------------------------------------#
# Example 4: Characterize two timers provided in pal.utilities.timing module.
#-----------------------------------------------------------------------------#

# Computation task takes approximately 7 to 9 ms
def computation():
    num = 0
    for val in range(400000):
        num = num + val

# This first method (Timer) is based on the absolute approach, but implemented
# via a class for ease of use. You should see similar performance as the
# absolute example #3. This does not use any timing functions from Quanser.

from pal.utilities.timing import Timer

timer = Timer (sampleRate=100.0, totalTime=10.0)
counter = 0
while timer.check():
    computation()
    timer.sleep()
print("Timer - stop Time:", f"{timer.performance[0]:.4f}", "sec with",
      f"{timer.performance[1]:.4f}", "iterations at a sample rate of",
      f"{timer.performance[2]:.4f}", ".")

# This second method (QTimer) is similar to the absolute approach, but uses the
# Timeout classes available in quanser.common, implemented as a class for ease
# of use. This class provides the best performance.

from pal.utilities.timing import QTimer

timer = QTimer(sampleRate=100.0, totalTime=10.0)
while timer.check():
    computation()
    timer.sleep()
print("QTimer- stop Time:", f"{timer.performance[0]:.4f}", "sec with",
      f"{timer.performance[1]:.4f}", "iterations at a sample rate of",
      f"{timer.performance[2]:.4f}", ".")
