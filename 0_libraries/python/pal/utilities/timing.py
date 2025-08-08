import time
from quanser.common import Timeout

# Timing class wrappers based on timing module & quanser.common Timeout
# Last updated: 5th May 2025
# Quanser Consulting Inc.

class Timer():
    """A class for timing your loops using sleep methods that account for both
    computation time as well as sleep overhead.

    Parameters
    ----------
    sampleRate : float
        Desired frequency (Hz) for your timer.
    totalTime : float
        Total simulation time you want to run your script for.

    Other Parameters
    ----------------
    performance : array_like
        includes the final end time, simulation counter iterations & achieved
        sample time

    Examples
    --------
    Time a loop at 50 Hz for 240 seconds.

    >>> from pal.utilities.timing import QTimer

    >>> # Create a 50.0 Hz timer for 240.0 seconds.
    >>> timer = Timer(sampleRate=50.0, totalTime=240.0)

    >>> while timer.check() # resets loop iteration, and checks validity
    >>>     computations_that_depend_on_current_time( timer.get_current_time() )
    >>>     computations_that_depend_on_sample_time( timer.get_sample_time() )
    >>>     timer.sleep()   # sleeps until next iteration must start


    """
    def __init__(self, sampleRate, totalTime, verbose=False):
        import os
        if os.name == 'nt':
            import ctypes
            winmm = ctypes.WinDLL('winmm')
            winmm.timeBeginPeriod(1)

        self._eps = 1/2500
        self._verbosity = verbose
        self._totalTime = totalTime
        self._sampleRate = sampleRate
        self._sampleTime = 1/sampleRate
        self._counter = 0
        self._sampleTimeAchieved = self._sampleTime
        self._restart()
        self._loopStart = self._startTime
        self._loopEnd = self._loopStart

    def _restart(self):
        '''Used to restart the simulation time from 0.'''
        self._startTime = time.time()

    def check(self):
        '''Resets internal parameters for next iteration. Use this method as
        a condition on your while loop.'''
        self._loopStart = time.time() - self._startTime
        self._sampleTimeAchieved = self._loopStart - self._loopEnd
        if (self._sampleTimeAchieved > (self._sampleTime + self._eps)) and (self._verbosity):
            print('Warning: desired sample time not achieved... consider slowing down.')
        flag = self._loopStart < self._totalTime
        if not flag:
            finalTime = self._loopStart
            finalCounts = self._counter
            finalSampleTime = finalTime/finalCounts
            self.performance = [finalTime, finalCounts, finalSampleTime]
        return flag

    def get_current_time(self):
        '''Returns the current time (absolute).'''
        return self._loopStart

    def get_sample_time(self):
        '''Returns the sample time (relative).'''
        return self._sampleTimeAchieved

    def sleep(self):
        '''Sleeps as required to catch up to an absolute clock.'''
        delta = min(self._loopStart - self._counter*self._sampleTime,
                    self._sampleTime)
        time.sleep(self._sampleTime - delta)
        self._counter = self._counter + 1
        self._loopEnd = self._loopStart
        if self._verbosity:
            print('Current Time:', f"{self._loopStart:.3f}",
                  'Simulation Time:', f"{self._counter*self._sampleTime:.3f}")

class QTimer():
    """A class for timing your loops using busy wait methods that account for
    both computation time as well as sleep overhead.

    Parameters
    ----------
    sampleRate : float
        Desired frequency (Hz) for your timer.
    totalTime : float
        Total simulation time you want to run your script for.

    Other Parameters
    ----------------
    performance : array_like
        Includes the final end time, simulation counter iterations & achieved
        sample time

    Examples
    --------
    Time a loop at 50 Hz for 240 seconds.

    >>> from pal.utilities.timing import QTimer

    >>> # Create a 50.0 Hz timer for 240.0 seconds.
    >>> timer = QTimer(sampleRate=50.0, totalTime=240.0)

    >>> while timer.check() # resets loop iteration, and checks validity
    >>>     computations_that_depend_on_current_time( timer.get_current_time() )
    >>>     computations_that_depend_on_sample_time( timer.get_sample_time() )
    >>>     timer.sleep()   # sleeps until next iteration must start

    """
    def __init__(self, sampleRate, totalTime):
        self._totalTime = totalTime
        self._sampleRate = sampleRate
        self._sampleTime = 1/sampleRate
        self._interval = Timeout.get_timeout(self._sampleTime)
        self._counter = 1
        self._restart()

    def _restart(self):
        '''Used to restart the simulation time from 0.'''
        self._start = Timeout.get_current_time()
        self._next = self._start + self._interval

    def check(self):
        '''Resets internal parameters for next iteration. Use this method as
        a condition on your while loop.'''
        if self.get_current_time() - self._sampleTime*self._counter > self._sampleTime:
            print('Warning: desired sample time not achieved... consider slowing down.')
        self._counter = self._counter + 1
        self._next = self._next + self._interval

        flag = self._counter < int(self._totalTime/self._sampleTime)
        if not flag:
            finalTime = self.get_current_time()
            finalCounts = self._counter
            finalSampleTime = finalTime/finalCounts
            self.performance = [finalTime, finalCounts, finalSampleTime]
        return flag

    def get_current_time(self):
        '''Returns the current time (absolute).'''
        _netTime = self._next.get_current_time() - self._start
        return _netTime.get_milliseconds()/1000

    def get_sample_time(self):
        '''Returns the sample time (relative).'''
        return self._sampleTime

    def sleep(self, verbose=False):
        '''Sleeps until the next Timeout expires.'''
        while not self._next.is_expired():
            pass
        if verbose:
            print('Current Time:', f"{self.get_current_time():.3f}", 'Simulation Time:', f"{self._counter*self._sampleTime:.3f}")
