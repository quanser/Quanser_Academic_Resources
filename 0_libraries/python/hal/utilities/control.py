"""This module contains general implementations for various controller types.
"""
import numpy as np
from pal.utilities.math import wrap_to_pi

class PID:
    """A proportional-integral-derivative (PID) controller.

    A proportional-integral-derivative (PID) controller that produces a control
    signal based on the tracking error and specified gain terms: Kp, Ki, and
    Kd.
    """

    def __init__(self, Kp=0, Ki=0, Kd=0, uLimits=None):
        """Creates a PID Controller Instance

        Args:
            Kp (float): Proportional gain (default 0).
            Ki (float): Integral gain (default 0).
            Kd (float): Derivative gain (default 0).
            uLimits (tuple): Upper and lower limits on the output signal,
                (u_min, u_max). Defaults to None.
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.uLimits = uLimits
        self.reset()

    def reset(self):
        """Reset the controller.

        This method resets numerical integrator and derivative.
        """
        self.ei = 0
        self.prev_e = None

    def update(self, r, y, dt):
        """Update the controller output.

        This method updates the control output based on the current set-point,
        measured value, and time since last update.

        Args:
            r (float): The set-point.
            y (float): The measured value.
            dt (float): The time elapsed since the last update.

        Returns:
            float: The controller output.
        """
        # Calulate the error (e)
        e = r - y

        # Calculate the integral of the error
        self.ei += dt * e

        # Calculate derivate of the error
        if self.prev_e is None or dt < 0.001:
            de = 0
        else:
            de = (e - self.prev_e) / dt
        self.prev_e = e

        # Calculate and return the new control signal
        u = self.Kp * e + self.Ki * self.ei + self.Kd * de
        if self.uLimits is None:
            return u
        return np.clip(u, self.uLimits[0], self.uLimits[1])


class StanleyController:
    """A Stanley controller for following a path of waypoints.

    The controller determines the desired heading based on the closest point on
    the path, and computes the steering angle required to track that heading.

    Args:
        waypoints (numpy.ndarray): An array of waypoints as (x, y) tuples.
        k (float): The gain for the cross track error (default 1).
        cyclic (bool): Whether the path is cyclic (default True).
    """
    def __init__(self, waypoints, k=1, cyclic=True):
        self.updatePath(waypoints, cyclic)
        self.maxSteeringAngle = np.pi/6
        self.k = k
        self.p_ref = (0, 0)
        self.th_ref = 0

    def updatePath(self, waypoints, cyclic):
        """Update the path of waypoints.

        This method updates the array of waypoints and resets the internal
        state of the controller.

        Args:
            waypoints (numpy.ndarray): An array of waypoints as (x, y) tuples.
            cyclic (bool): Whether the path is cyclic.
        """

        self.wp = np.array(waypoints)
        self.N = len(waypoints[0, :])
        if self.N == 2:
            print('asdfasdf')
            self.wp = self.wp.T
            self.N = len(waypoints[0, :])

        self.wpi = 0
        self.cyclic = cyclic
        self.pathComplete = False

    def update(self, p, th, speed):
        """Update the controller output.

        This method updates the controller output based on the current position
        and heading.

        Args:
            p (tuple): The current position as an (x, y) tuple.
            th (float): The current heading in radians.
            speed (float): The current speed.

        Returns:
            float: The steering angle in radians.
        """
        wp_1 = self.wp[:, np.mod(self.wpi, self.N-1)]
        wp_2 = self.wp[:, np.mod(self.wpi+1, self.N-1)]

        v = wp_2 - wp_1
        v_mag = np.linalg.norm(v)
        try:
            v_uv = v / v_mag
        except ZeroDivisionError:
            return 0

        tangent = np.arctan2(v_uv[1], v_uv[0])

        s = np.dot(p-wp_1, v_uv)

        if s >= v_mag:
            if  self.cyclic or self.wpi < self.N-2:
                self.wpi += 1
            else:
                self.pathComplete = True

        ep = wp_1 + v_uv*s
        ct = ep - p
        dir = wrap_to_pi(np.arctan2(ct[1], ct[0]) - tangent)

        ect = np.linalg.norm(ct) * np.sign(dir)
        psi = wrap_to_pi(tangent-th)

        self.p_ref = ep
        self.th_ref = tangent

        return np.clip(
            wrap_to_pi(psi + np.arctan2(self.k*ect, speed)),
            -self.maxSteeringAngle,
            self.maxSteeringAngle
        )
