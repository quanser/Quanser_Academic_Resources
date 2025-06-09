# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

"""
state_estimation.py

Skills activity code for state estimation lab guide.
Students will implement three types of state estimation techniques for
localizing the QCar in space.
Please review Lab Guide - State Estimation PDF
"""

import numpy as np
from threading import Thread
import time
import signal

from pal.products.qcar import QCar, QCarGPS, IS_PHYSICAL_QCAR
from pal.utilities.scope import MultiScope
from pal.utilities.math import wrap_to_pi


if not IS_PHYSICAL_QCAR:
    import qlabs_setup
    qlabs_setup.setup(
        initialPosition=[0, 0, 0],
        initialOrientation=[0, 0, 0]
    )
    calibrate = False
else:
    calibrate = 'y' in input('do you want to recalibrate?(y/n)')

#================ Experiment Configuration ================
# ===== Timing Parameters
# - tf: experiment duration in seconds.
# - controllerUpdateRate: control update rate in Hz. Shouldn't exceed 500

tf = 10
controllerUpdateRate = 100

# Used to enable safe keyboard triggered shutdown
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

class QcarEKF:

    def __init__(self, x0, P0, Q, R):
        # Nomenclature:
        # - x0: initial estimate
        # - P0: initial covariance matrix estimate
        # - Q: process noise covariance matrix
        # - R: observation noise covariance matrix
        # - xHat: state estimate
        # - P: state covariance matrix
        # - L: wheel base of the QCar
        # - C: output matrix

        self.L = 0.257

        self.I = np.eye(3)
        self.xHat = x0
        self.P = P0
        self.Q = Q
        self.R = R

        self.C = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ])

    # ==============  SECTION A -  Motion Model ====================
    def f(self, X, u, dt):
        # Kinematic Bicycle Model:
        # - X = [x, y, theta]
        # - u[0] = v (speed in [m/s])
        # - u[1] = delta (steering Angle in [rad])
        # - dt: change in time since last update

        return X



    # ==============  SECTION B -  Motion Model Jacobian ====================
    def Jf(self, X, u, dt):
        # Jacobian for the kinematic bicycle model (see self.f)
 
        return np.eye(3)

    # ==============  SECTION C -  Motion Model Prediction ====================
    def prediction(self, dt, u):

        return


    # ==============  SECTION D -  Measurement correction ====================

    def correction(self, y):
        
        return


class GyroKF:

    def __init__(self, x0, P0, Q, R):
        # Nomenclature:
        # - x0: initial estimate
        # - P0: initial covariance matrix estimate
        # - Q: process noise covariance matrix
        # - R: observation noise covariance matrix
        # - xHat: state estimate
        # - P: state covariance matrix
        # - A: state matrix
        # - B: input matrix
        # - C: output matrix

        self.I = np.eye(2)
        self.xHat = x0
        self.P = P0
        self.Q = Q
        self.R = R

        # State Space Representation Matrices
        self.A = np.array([
            [0, -1],
            [0, 0]
        ])
        self.B = np.array([
            [1],
            [0]
        ])
        self.C = np.array([
            [1, 0]
        ])


    # ==========  SECTION F -  Gyro Heading Prediction  ================
    def prediction(self, dt, u):
        # - dt: change in time since last prediction
        # - u: most recent gyroscope measurement
        pass
    
    # ==========  SECTION G -  GPS Heading Correction  ================
    def correction(self, y):
        # - y: heading measurement from GPS
        pass

def controlLoop():
    #region controlLoop setup
    global KILL_THREAD
    # used to limit data sampling to 10hz
    countMax = controllerUpdateRate / 10
    count = 0
    #endregion

    #region : Estimators Setup
    # Initial estimates for QCar state and covarience matrix (P)
    x0 = np.zeros((3,1))
    P0 = np.eye(3)

    # Estimator 1: EKF performing dead reckoning
    ekf_dr = QcarEKF(
        x0=x0,
        P0=P0,
        Q=np.diagflat([0.01, 0.01, 0.01]),
        R=None
    )

    # Estimator 2: EKF combining the kinematic bicycle model with GPS data
    ekf_gps = QcarEKF(
        x0=x0,
        P0=P0,
        Q=np.diagflat([0.01, 0.01, 0.01]),
        R=np.diagflat([0.2, 0.2, 0.1])
    )

    # Estimator 3: Cascaded (E)KF
    # 3.a Kalman filter fusing gyroscope data with GPS heading data
    kf = GyroKF(
        x0=np.zeros((2,1)),
        P0=np.eye(2),
        Q=np.diagflat([0.00001, 0.00001]),
        R=np.diagflat([.1])
    )

    # 3.b EKF combining bicycle model with GPS pos. and KF heading estimate
    C_combined = np.eye(3)
    C_headingOnly = np.array([[0, 0, 1]])
    R_combined = np.diagflat([0.8, 0.8, 0.01])
    R_headingOnly = np.diagflat([0.01])

    ekf_sf = QcarEKF(
        x0=x0,
        P0=P0,
        Q=np.diagflat([0.0001, 0.0001, 0.0001]),
        R=R_combined
    )
    #endregion

    #region : Main Control Loop
    qcar = QCar(readMode=1, frequency=controllerUpdateRate)
    gps = QCarGPS(initialPose=x0[:,0],calibrate=calibrate)

    with qcar, gps:
        t0 = time.time()
        t = 0
        while (t < tf) and (not KILL_THREAD):
            #region : Loop timing update
            tp = t
            t = time.time() - t0
            dt = t-tp
            #endregion

            #region : QCar Input / Output Update
            # Read from QCar sensors
            qcar.read()
            speed_tach = qcar.motorTach
            th_gyro = qcar.gyroscope[2]

            # Update and write QCar control values
            # - u: throttle [%]. Shouldn't exceed 0.2 percent
            # - delta: steering angle [radians]. Shouldn't exceed pi/6.
            u = 0.1
            delta =  np.pi/12
            qcar.write(u, delta)
            #endregion

            # ======= Section For enabling Kalman Filter Estimators =======
            ekf_dr.prediction(dt, [speed_tach, delta])
            # ekf_gps.prediction(dt, [speed_tach, delta])
            # ekf_sf.prediction(dt, [speed_tach, delta])
            # kf.prediction(dt, th_gyro)

            #region : Correction Update for Filters
            if gps.readGPS():
                # ==========  SECTION E -  Measurement Update  ================
                '''
                # Collect new GPS readings

                '''
                ekf_sf.C = C_combined
                ekf_sf.R = R_combined
                # Correction for estimator 3.a using GPS
                '''
                kf.correction(th_gps)
                '''

                # Correction for estimator 3.b using GPS and heading estimate

            else:
                # Correction for 3.b using only heading estimate
                pass

            #endregion

            #region Update Scopes with New Data Samples
            count += 1 
            if count >= countMax:
                # x position estimates
                scope.axes[0].sample(t, [
                    ekf_dr.xHat[0,0],
                    ekf_gps.xHat[0,0],
                    ekf_sf.xHat[0,0]
                ])
                # y position estimates
                scope.axes[1].sample(t, [
                    ekf_dr.xHat[1,0],
                    ekf_gps.xHat[1,0],
                    ekf_sf.xHat[1,0]
                ])
                # Heading angle estimate
                scope.axes[2].sample(t, [
                    ekf_dr.xHat[2,0],
                    ekf_gps.xHat[2,0],
                    ekf_sf.xHat[2,0]
                ])
                # x-y view of estimated trajectory
                scope.axes[3].sample(t, [
                    [ekf_dr.xHat[0,0], ekf_dr.xHat[1,0]],
                    [ekf_gps.xHat[0,0], ekf_gps.xHat[1,0]],
                    [ekf_sf.xHat[0,0], ekf_sf.xHat[1,0]],
                ])

                biasScope.axes[0].sample(t, [kf.xHat[0]])
                biasScope.axes[1].sample(t, [kf.xHat[1]])

                count = 0
            #endregion
            continue

    #endregion
    return

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Setup and run experiment
if __name__ == '__main__':

    #region : Setup Scopes
    if IS_PHYSICAL_QCAR:
        fps = 10
    else:
        fps = 30
    # Scope for displaying estimated gyroscope bias
    biasScope = MultiScope(
        rows=2,
        cols=1,
        title='Heading Kalman Filter',
        fps=fps
    )
    biasScope.addAxis(
        row=0,
        col=0,
        xLabel='Time [s]',
        yLabel='Heading Angle [rad]',
        timeWindow=tf
    )
    biasScope.axes[0].attachSignal()
    biasScope.addAxis(
        row=1,
        col=0,
        xLabel='Time [s]',
        yLabel='Gyroscope Bias [rad/s]',
        timeWindow=tf
    )
    biasScope.axes[1].attachSignal()

    # Scope for comparing performance of various estimator types
    scope = MultiScope(rows=3, cols=2, title='QCar State Estimation', fps=fps)

    scope.addAxis(row=0, col=0, timeWindow=tf, yLabel='x Position [m]')
    scope.axes[0].attachSignal(name='x_dr')
    scope.axes[0].attachSignal(name='x_ekf_gps')
    scope.axes[0].attachSignal(name='x_ekf_sf')

    scope.addAxis(row=1, col=0, timeWindow=tf, yLabel='y Position [m]')
    scope.axes[1].attachSignal(name='y_dr')
    scope.axes[1].attachSignal(name='y_ekf_gps')
    scope.axes[1].attachSignal(name='y_ekf_sf')

    scope.addAxis(row=2, col=0, timeWindow=tf, yLabel='Heading Angle [rad]')
    scope.axes[2].xLabel = 'Time [s]'
    scope.axes[2].attachSignal(name='th_dr')
    scope.axes[2].attachSignal(name='th_ekf_gps')
    scope.axes[2].attachSignal(name='th_ekf_sf')

    scope.addXYAxis(
        row=0,
        col=1,
        rowSpan=3,
        xLabel='x Position [m]',
        yLabel='y Position [m]',
        xLim=(-1.5, 1.5),
        yLim=(-0.5, 2.5)
    )
    scope.axes[3].attachSignal(name='ekf_dr')
    scope.axes[3].attachSignal(name='ekf_gps')
    scope.axes[3].attachSignal(name='ekf_sf')
    #endregion

    #region : Setup control thread, then run experiment
    controlThread = Thread(target=controlLoop)
    controlThread.start()

    try:
        while controlThread.is_alive() and (not KILL_THREAD):
            MultiScope.refreshAll()
            time.sleep(0.01)
    finally:
        KILL_THREAD = True
    #endregion
    if not IS_PHYSICAL_QCAR:
            qlabs_setup.terminate()

    input('Experiment complete. Press any key to exit...')
#endregion