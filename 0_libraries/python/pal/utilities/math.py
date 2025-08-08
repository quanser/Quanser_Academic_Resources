"""math.py: A module providing handy functions for common mathematical tasks.

This module contains a collection of utility functions for completing various
mathematical operations, such as wrapping angles, filtering signals, and
performing numerical differentiation. These functions are designed to simplify
and streamline the process of working with mathematical operations in a variety
of applications, including data processing, analysis, and control systems.
"""
import numpy as np


TWO_PI = 2 * np.pi
"""A constant representing the value of two times pi, for convenience."""


def wrap_to_2pi(th: float) -> float:
    """Wrap an angle in radians to the interval [0, 2*pi).

    Args:
        th (float): The angle to be wrapped in radians.

    Returns:
        float: The wrapped angle in radians.
    """
    return np.mod(np.mod(th, TWO_PI) + TWO_PI, TWO_PI)


def wrap_to_pi(th: float) -> float:
    """Wrap an angle in radians to the interval [-pi, pi).

    Args:
        th (float): The angle to be wrapped in radians.

    Returns:
        float: The wrapped angle in radians.
    """
    th = th % TWO_PI
    th = (th + TWO_PI) % TWO_PI
    if th > np.pi:
        th -= TWO_PI
    return th


def angle(v1: np.ndarray, v2: np.ndarray) -> float:
    """Compute the angle in radians between two vectors.

    Args:
        v1 (numpy.ndarray): A 2-dimensional input vector.
        v2 (numpy.ndarray): A 2-dimensional input vector.

    Returns:
        float: The angle between the two input vectors in radians.
    """
    num = np.dot(v1, v2)
    den = np.linalg.norm(v1) * np.linalg.norm(v2)
    try:
        th = np.arccos(num / den)
    except:
        th = 0
    return th


def signed_angle(v1: np.ndarray, v2: np.ndarray = None) -> float:
    """Find the signed angle between two vectors

    Compute the signed angle in radians between two vectors or the angle of
    a single vector with respect to the x-axis if v2 is None.

    Args:
        v1 (numpy.ndarray): A 2-dimensional input vector.
        v2 (numpy.ndarray, optional): A 2-dimensional input vector.
            Defaults to None.

    Returns:
        float: The signed angle between the two input vectors in radians, or
            the angle of v1 in radians with respect to the x-axis.

    Notes:
        - If v2 is None, then the function computes the angle of v1 with
            respect to the x-axis.
        - The function uses the `wrap_to_pi` function to ensure that the signed
            angle is in the range [-pi, pi).
    """
    if v2 is None:
        return np.arctan2(np.arctan2(v1[1], v1[0]))
    return wrap_to_pi(np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0]))



def get_mag_and_angle(v):
    mag = np.linalg.norm(v)
    alpha = np.arctan2(v[1], v[0])
    return mag, alpha


def find_overlap(a: np.ndarray, b: np.ndarray, i: int, j: int) -> tuple:
    """Finds slices that correspond to overlapping cells of two 2D numpy arrays

    Args:
        a (numpy.ndarray): First input array of shape (m, n).
        b (numpy.ndarray): Second input array of shape (p, q).
        i (int): Row index in a's index-space where b[0,0] is located.
        j (int): Column index in a's index-space where b[0,0] is located.

    Returns:
        Tuple of two slices: aSlice and bSlice.
        aSlice (tuple): Slice of a corresponding to the overlapping cells.
        bSlice (tuple): Slice of b corresponding to the overlapping cells.

    Notes:
        - The function assumes that the first element of b is located at
            position (i, j) in a's index-space.
        - The function clips the indices of a and b to ensure that they are
            within bounds.
    """

    ma,na = a.shape
    mb,nb = b.shape

    ia = np.int_(np.array([np.clip(i,0,ma),np.clip(i+mb,0,ma)]))
    ja = np.int_(np.array([np.clip(j,0,na),np.clip(j+nb,0,na)]))
    ib = np.int_(ia - i)
    jb = np.int_(ja - j)

    aSlice = (slice(ia[0],ia[1]),slice(ja[0],ja[1]))
    bSlice = (slice(ib[0],ib[1]),slice(jb[0],jb[1]))

    return aSlice, bSlice


def ddt_filter(u, state, A, Ts):
    # d/dt with filtering:
    # y = As*u/(s+A)
    #
    # Z-domain with Tustin transform:
    # y = (2AZ - 2A)/((2+AT)z + (AT-2))
    #
    # Divide through by z to get z^-1 terms the convert to time domain
    # y_k1(AT-2) + y_k(AT+2) = 2Au_k - 2Au_k1
    # y_k = 1/(AT+2) * ( 2Au_k - 2Au_k1 - y_k1(AT-2) )
    #
    # y - output
    # u - input
    # state - previous state returned by this function -- initialize to np.array([0,0], dtype=np.float64)
    # Ts - sample time in seconds
    # A - filter bandwidth in rad/s

    y = 1/(A*Ts+2)*(2*A*u - 2*A*state[0] - state[1]*(A*Ts - 2))

    state[0] = u
    state[1] = y

    return y, state

def lp_filter(u, state, A, Ts):
    # y = A*u/(s+A)
    #
    # y - output
    # u - input
    # state - previous state returned by this function -- initialize to np.array([0,0], dtype=np.float64)
    # Ts - sample time in seconds
    # A - filter bandwidth in rad/s

    y = (u*Ts*A + state[0]*Ts*A - state[1]*(Ts*A - 2) ) / (2 + Ts*A)

    state[0] = u
    state[1] = y

    return y, state


class SignalGenerator:
    """Class object consisting of common signal generators"""

    def sine(self, amplitude, angularFrequency, phase=0, mean=0):
        """
        This function outputs a sinusoid wave based on the provided timestamp.

        For example:

        .. code-block:: python

            generatorSine = Signal_Generator().sine(2, pi/2)
            initialOutput = next(generatorSine)
            while True:
                timestamp = your_timing_function()
                output = generatorSine.send(timestamp)
        """

        output = amplitude*np.sin(phase) + mean
        while True:
            timestamp = yield output
            output = amplitude*np.sin(
                angularFrequency*timestamp + phase) + mean

    def cosine(self, amplitude, angularFrequency, phase=0, mean=0):
        """Outputs a cosinusoid wave based on the provided timestamp.

        For example:

        .. code-block:: python

            generatorCosine = Signal_Generator().cosine(2, pi/2)
            initialOutput = next(generatorCosine)
            while True:
                timestamp = your_timing_function()
                output = generatorCosine.send(timestamp)
        """

        output = amplitude*np.sin(phase + np.pi/2) + mean
        while True:
            timestamp = yield output
            output = amplitude*np.sin(
                angularFrequency*timestamp + phase + np.pi/2) + mean

    def PWM(self, frequency, width, phase=0):
        """This function outputs a PWM wave based on the provided timestamp.

        For example:

        .. code-block:: python

            generatorPWM = Signal_Generator().PWM(2, 0.5)
            initialOutput = next(generatorPWM)
            while True:
                timestamp = your_timing_function()
                output = generatorPWM.send(timestamp)
        """

        period = 1/frequency
        if phase%1 >= width:
            output = 0
        else:
            output = 1
        while True:
            timestamp = yield output
            marker = ( ( (timestamp % period) / period ) + phase ) % 1
            if marker > width:
                output = 0
            else:
                output = 1

    def square(self, amplitude, period):
        """Outputs a square wave based on the provided timestamp."""
        val = 0
        while True:
            timestamp = yield val
            if timestamp % period < period/2.0:
                val = amplitude
            else:
                val = -amplitude

class Calculus:
    """Class object consisting of basic derivative and integration functions"""

    def differentiator(self, dt, x0=0):
        """Finite-difference-based numerical derivative.

        Provide the sample time (s), and use the .send(value) method
        to differentiate.

        For example:

        .. code-block:: python

            diff_1 = Calculus().differentiator(0.01)
            while True:
                value = some_random_function()
                value_derivative = diff_1.send(value)

        Multiple differentiators can be defined for different signals.
        Do not use the same handle to differentiate different value signals.
        """
        derivative = 0
        while True:
            x = yield derivative
            derivative = (x - x0)/dt
            x0 = x

    def differentiator_variable(self, dt, x0=0):
        """Finite-difference-based numerical derivative.

        Provide the sample time (s), and use the .send(value) method
        to differentiate.

        For example:

        .. code-block:: python

            diff_1 = Calculus().differentiator_variable(0.01)
            while True:
                value = some_random_function()
                time_step = some_time_taken
                value_derivative = diff_1.send((value, time_step))

        Multiple differentiators can be defined for different signals.
        Do not use the same handle to differentiate different value signals.
        """
        derivative = 0
        while True:
            x, dt = yield derivative
            derivative = (x - x0)/dt
            x0 = x

    def integrator(self, dt, integrand=0, saturation=None):
        """Iterative numerical integrator.

        Provide the sample time (s), and use the .send(value) method
        to integrate.

        For example:

        .. code-block:: python

            intg_1 = Calculus().integrator(0.01)
            while True:
                value = some_random_function()
                value_integral = intg_1.send(value)

        Multiple integrators can be defined for different signals.
        Do not use the same handle to integrate different value signals.
        """
        self.saturation = saturation
        while True:
            x = yield integrand
            if self.saturation is None:
                integrand = integrand + x * dt
            else:
                temp = integrand + x * dt
                if temp < saturation and temp > -saturation:
                    integrand = temp

    def integrator_variable(self, dt, integrand=0, minSaturation=-np.inf, maxSaturation=np.inf):
        """Iterative numerical integrator.

        Provide the sample time (s), and use the .send(value) method
        to integrate.

        For example:

        .. code-block:: python

            intg_1 = Calculus().integrator_variable(0.01)
            while True:
                value = some_random_function()
                time_step = some_time_taken
                value_integral = intg_1.send((value, time_step)))

        Multiple integrators can be defined for different signals.
        Do not use the same handle to integrate different value signals.
        """
        while True:
            x, dt = yield integrand
            temp = integrand + x * dt
            if temp < maxSaturation and temp > minSaturation:
                integrand = temp

class Integrator:
    def __init__(self, integrand=0, minSaturation=-np.inf, maxSaturation=np.inf):
        self.maxSaturation = maxSaturation
        self.minSaturation = minSaturation
        self.integrand = integrand

    def integrate(self, rate, timestep):
        temp = self.integrand + rate * timestep
        if temp < self.maxSaturation and temp > self.minSaturation:
            self.integrand = temp
        return self.integrand

    def reset(self, resetValue):
        self.integrand = resetValue

class Filter:
    """Class object consisting of different filter functions"""

    def low_pass_first_order(self, wn, dt, x0=0):
        """Standard first order low pass filter.

        Provide the filter frequency (rad/s), sample time (s), and
        use the .send(value) method to filter.

        For example:

        .. code-block:: python

            myFilter = filter().low_pass_first_order(20, 0.01)
            valueFiltered = next(myFilter)
            while True:
                value = some_random_function()
                valueFiltered = myFilter.send(value)

        Multiple filters can be defined for different signals.
        Do not use the same handle to filter different signals.
        """
        output = 0
        myIntegrator = Calculus().integrator(dt, integrand=x0)
        next(myIntegrator)
        while True:
            x = yield output
            output = myIntegrator.send(wn * (x - output))

    def low_pass_first_order_variable(self, wn, dt, x0=0):
        """Standard first order low pass filter.

        Provide the filter frequency (rad/s), sample time (s), and
        use the .send(value) method to filter.

        For example:

        .. code-block:: python

            myFilter = filter().low_pass_first_order(20, 0.01)
            valueFiltered = next(myFilter)
            while True:
                value = some_random_function()
                valueFiltered = myFilter.send(value)

        Multiple filters can be defined for different signals.
        Do not use the same handle to filter different signals.
        """
        output = x0
        myIntegrator = Calculus().integrator_variable(dt, integrand=x0)
        next(myIntegrator)
        while True:
            x, dt = yield output
            output = myIntegrator.send((wn * (x - output), dt))

    def low_pass_second_order(self, wn, dt, zeta=1, x0=0):
        """Standard second order low pass filter.

        Provide the filter frequency (rad/s), sample time (s), and
        use the .send(value) method to filter.

        For example:

        .. code-block:: python

            myFilter = filter().low_pass_second_order(20, 0.01)
            valueFiltered = next(myFilter)
            while True:
                value = some_random_function()
                valueFiltered = myFilter.send(value)

        Multiple filters can be defined for different signals.
        Do not use the same handle to filter different signals.
        """
        output = x0
        temp = 0
        myFIrstIntegrator = Calculus().integrator(dt, integrand=0)
        mySecondIntegrator = Calculus().integrator(dt, integrand=x0)
        next(myFIrstIntegrator)
        next(mySecondIntegrator)
        while True:
            x = yield output
            temp = myFIrstIntegrator.send(wn * ( x - output - 2*zeta*temp ) )
            output = mySecondIntegrator.send(wn * temp)

    def complimentary_filter(self, kp, ki, dt, x0=0):
        """Complementary filter based rate and correction signal
            using a combination of low and high pass on them respectively.
        """
        output = 0
        temp = 0
        integratorRate = Calculus().integrator(dt, integrand=0)
        integratorTuner = Calculus().integrator(dt, integrand=x0)
        next(integratorRate)
        next(integratorTuner)
        while True:
            rate, correction = yield output
            temp = integratorRate.send(rate)
            error = output - correction
            output = temp - (kp*error) - (ki*integratorTuner.send(error))

    def moving_average(self, samples, x0=0):
        """Standard moving average filter.

        Provide the number of samples to average, and use the .send(value)
        method to filter.

        For example:

        .. code-block:: python

            myFilter = filter().moving_average(20)
            valueFiltered = next(myFilter)
            while True:
                value = some_random_function()
                valueFiltered = myFilter.send(value)

        Multiple filters can be defined for different signals.
        Do not use the same handle to filter different signals.
        """
        window = x0*np.ones(samples)
        average = x0
        while True:
            newValue = yield average
            window = np.append(newValue, window[0:samples-1])
            average = window.mean()

class Signal:
    @staticmethod
    def edge_detector():
        '''Rising edge and falling edge detector.

        Monitor input signal (source) and produce an one-timestep pulse at either
        the rising edge or the falling edge of the input signal.

        '''
        rising_edge = False
        falling_edge = False
        state = False
        # elapsed_time = 0
        while True:
            source = yield rising_edge , falling_edge
            rising_edge = False
            falling_edge = False

            if state!=source:
                rising_edge=bool(source)
                falling_edge=not source

            state = source