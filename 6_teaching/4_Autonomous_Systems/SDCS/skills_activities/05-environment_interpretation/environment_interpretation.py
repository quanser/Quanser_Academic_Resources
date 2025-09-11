# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

"""
environment_interpretation.py

Skills activity code for environment interpretation lab guide.
Please review the accompanying "Lab Guide - Environment Interpretation" PDF
"""

import numpy as np
from scipy.special import logit, expit
from scipy import ndimage
from threading import Thread, Lock
import time
import pyqtgraph as pg
import signal

from pal.products.qcar import QCar, QCarGPS, IS_PHYSICAL_QCAR, QCAR_CONFIG
from pal.utilities.scope import MultiScope
from pal.utilities.math import find_overlap, wrap_to_2pi, wrap_to_pi
from hal.content.qcar_functions import QCarEKF, QCarDriveController
from hal.products.mats import SDCSRoadMap
#endregion

# ================ Experiment Configuration ================
# ===== Timing Parameters
# - tf: experiment duration in seconds.
# - startDelay: delay to give filters time to settle in seconds.
# - controllerUpdateRate: control update rate in Hz. Shouldn't exceed 500
tf = 100
startDelay = 1
controllerUpdateRate = 100

# ===== Vehicle Controller Parameters
# - enableVehicleControl: If true, the QCar will drive through the specified
#   node sequence. If false, the QCar will remain stationary.
# - v_ref: desired velocity in m/s
# - nodeSequence: list of nodes from roadmap. Used for trajectory generation.
enableVehicleControl = False
v_ref = 0.3
nodeSequence = [0, 20, 0]

# ===== Occupancy Grid Parameters
# - cellWidth: edge length for occupancy grid cells (in meters)
# - r_res: range resolution for polar grid cells (in meters)
# - r_max: maximum range of the lidar (in meters)
# - p_low: likelihood value for vacant cells (according to lidar scan)
# - p_high: likelihood value for occupied cells (according to lidar scan)
cellWidth = 0.02
r_res = 0.05
r_max = 4
p_low = 0.4
p_high = 0.6


#region Initial Setup
lock = Lock()

roadmap = SDCSRoadMap()
waypointSequence = roadmap.generate_path(nodeSequence)
initialPose = roadmap.get_node_pose(nodeSequence[0]).squeeze()
x_hat = initialPose
t_hat = 0

if not IS_PHYSICAL_QCAR:
    import qlabs_setup
    from qvl.qcar import QLabsQCar
    hQCar = qlabs_setup.setup(
        initialPosition=[initialPose[0], initialPose[1], 0],
        initialOrientation=[0, 0, initialPose[2]]
    )
    calibrate=False
else:
    calibrate =  'y' in input('do you want to recalibrate?(y/n)')
# Used to enable safe keyboard triggered shutdown
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)

gps = QCarGPS(initialPose=initialPose,calibrate=calibrate)
while (not KILL_THREAD) and (gps.readGPS() or  gps.readLidar()):
    pass

#endregion

class OccupancyGrid:

    def __init__(self,
            x_min=-4,
            x_max=3,
            y_min=-3,
            y_max=6,
            cellWidth=0.02,
            r_max=5,
            r_res=0.02,
            p_low=0.4,
            p_high=0.6
        ):

        #region define probabilities and their log-odds forms
        self.p_low = p_low
        self.p_prior = 0.5
        self.p_high = p_high
        self.p_sat = 0.001

        self.l_low = logit(self.p_low)
        self.l_prior = logit(self.p_prior)
        self.l_high = logit(self.p_high)
        self.l_min = logit(self.p_sat)
        self.l_max = logit(1-self.p_sat)
        #endregion

        self.init_polar_grid(r_max, r_res)

        self.init_world_map(
            x_min=x_min,
            x_max=x_max,
            y_min=y_min,
            y_max=y_max,
            cellWidth=cellWidth
        )
        self.init_patch()

    # ==============  SECTION A - Polar Grid ====================
    def init_polar_grid(self, r_max, r_res):
        # Configuration Parameters for polar grid
        fov = 2*np.pi
        self.phiRes = 1 * np.pi/180
        self.r_max = r_max
        self.r_res = r_res

        # Size of polar patch
        self.mPolarPatch = np.int_(np.ceil(fov / self.phiRes))
        self.nPolarPatch = np.int_(np.floor(self.r_max/self.r_res))


        self.polarPatch = np.zeros(
            shape = (self.mPolarPatch, self.nPolarPatch),
            dtype = np.float32
        )

    def update_polar_grid(self, r):
        # Implement code here to populate the values of self.polarPatch
        # given LiDAR range data 'r'.
        # - r is a 1D list of length self.mPolarPatch
        # - All range measurements are equally self.phiRes radians apart,
        #   starting with 0

        # Implement Your Solution Here

        pass



    # ==============  SECTION B - Interpolation ====================
    def init_patch(self):
        self.nPatch = np.int_(2*np.ceil(self.r_max/self.cellWidth) + 1)
        self.patch = np.zeros(
            shape = (self.nPatch, self.nPatch),
            dtype = np.float32
        )

    def generate_patch(self, th):
        # Implement Your Solution Here
        pass


    # ==============  SECTION C - Occupancy Grid Update  ====================
    def init_world_map(self,
            x_min = -4,
            x_max = 3,
            y_min = -3,
            y_max = 6,
            cellWidth=0.02
        ):

        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.cellWidth = cellWidth
        self.xLength = x_max - x_min
        self.yLength = y_max - y_min
        self.m = np.int_(np.ceil(self.yLength/self.cellWidth))
        self.n = np.int_(np.ceil(self.xLength/self.cellWidth))

        self.map = np.full(
            shape = (self.m, self.n),
            fill_value = self.l_prior,
            dtype = np.float32
        )

    def xy_to_ij(self, x, y):
        i = np.int_(np.round( (self.y_max - y) / self.cellWidth ))
        j = np.int_(np.round( (x - self.x_min) / self.cellWidth ))
        return i, j

    def updateMap(self, x, y, th, angles, distances):

        # Function created in SECTION A
        self.update_polar_grid(distances)

        # Function created in SECTION B
        self.generate_patch(th)
        # Implement code here to update self.map using self.patch

        pass


def controlLoop():
    #region controlLoop setup
    global KILL_THREAD, x_hat, t_hat
    u = 0
    delta = 0
    # used to limit data sampling to 10hz
    countMax = controllerUpdateRate / 10
    count = 0
    #endregion

    #region Set up plot items
    arrow1 = pg.ArrowItem(
        angle=180,
        tipAngle=60,
        headLen=10,
        tailLen=10,
        tailWidth=5,
        pen={'color': 'w', 'width': 1},
        brush='r'
    )
    arrow1.setPos(0,0)
    scope.axes[1].plot.addItem(arrow1)

    arrow2 = pg.ArrowItem(
        angle=180,
        tipAngle=60,
        headLen=10,
        tailLen=10,
        tailWidth=5,
        pen={'color': 'w', 'width': 1},
        brush='r'
    )
    scope.axes[2].plot.addItem(arrow2)
    #endregion

    #region QCar interface setup
    with lock:
        ekf = QCarEKF(x_0=x_hat)
    driveController = QCarDriveController(waypointSequence, cyclic=False)

    qcar = QCar(readMode=1, frequency=controllerUpdateRate)
    #endregion

    with qcar:
        t0 = time.time()
        t = 0
        while (t < tf+startDelay) and (not KILL_THREAD):
            #region : Loop timing update
            tp = t
            t = time.time() - t0
            dt = t-tp
            #endregion

            #region : Update QCar state estimates and drive controller
            qcar.read()
            if gps.readGPS():
                y_gps = np.array([
                    gps.position[0],
                    gps.position[1],
                    gps.orientation[2]
                ])
                ekf.update(
                    [qcar.motorTach, delta],
                    dt,
                    y_gps,
                    qcar.gyroscope[2],
                )
            else:
                ekf.update(
                    [qcar.motorTach, delta],
                    dt,
                    None,
                    qcar.gyroscope[2],
                )
            with lock:
                t_hat = time.time()
                x_hat = ekf.x_hat[:]

            x = ekf.x_hat[0, 0]
            y = ekf.x_hat[1, 0]
            v = qcar.motorTach
            th = ekf.x_hat[2, 0]
            p = np.array([x, y]) + np.array([np.cos(th), np.sin(th)]) * 0.2

            if t < startDelay or (not enableVehicleControl):
                u = 0
                delta = 0
            else:
                u, delta = driveController.update(p, th, v, v_ref, dt)
            qcar.write(u, delta)
            #endregion

            #region : Update Scopes
            count += 1
            if count >= countMax and t > startDelay:
                scope.axes[2].sample(t, [[p[0], p[1]]])
                arrow1.setStyle(angle=180-th*180/np.pi)
                arrow2.setPos(p[0],p[1])
                arrow2.setStyle(angle=180-th*180/np.pi)

                count = 0
            #endregion

            if driveController.steeringController.pathComplete:
                return
            continue
        with lock:
            print('Control thread terminated')


def mappingLoop():
    global KILL_THREAD, x_hat, t_hat

    og = OccupancyGrid(
        cellWidth=cellWidth,
        r_res=r_res,
        r_max=r_max,
        p_low=p_low,
        p_high=p_high
    )

    #region Configure Plots
    scope.axes[0].images[0].rotation = 90
    scope.axes[0].images[0].scale = (og.r_res, -og.phiRes*180/np.pi)
    scope.axes[0].images[0].offset = (0, 0)
    scope.axes[0].images[0].levels = (0, 1)

    scope.axes[1].images[0].scale = (og.r_res, -og.r_res)
    scope.axes[1].images[0].offset = (-og.nPatch/2, -og.nPatch/2)
    scope.axes[1].images[0].levels = (0, 1)

    scope.axes[2].images[0].scale = (og.cellWidth, -og.cellWidth)
    scope.axes[2].images[0].offset = (
        og.x_min/og.cellWidth,
        -og.y_max/og.cellWidth
    )
    scope.axes[2].images[0].levels = (0, 1)
    #endregion

    t0 = time.time()
    while time.time()-t0 < startDelay:
        gps.readLidar()

    while (not KILL_THREAD):
        #region Get latest pose estimate
        with lock:
            t = t_hat
            x = x_hat[0,0]
            y = x_hat[1,0]
            th = x_hat[2,0]

        x += 0.125 * np.cos(th)
        y += 0.125 * np.sin(th)
        #endregion

        #Read from Lidar and Update Occupancy Grid

        gps.readLidar()

        if gps.scanTime < t and QCAR_CONFIG['cartype'] == 1:
            continue

        og.updateMap(x, y, th, gps.angles,gps.distances)

        scope.axes[0].images[0].setImage(image=expit(og.polarPatch))
        scope.axes[1].images[0].setImage(image=expit(og.patch))
        scope.axes[2].images[0].setImage(image=expit(og.map))

    with lock:
        print('Mapping thread terminated')


#region : Setup and run experiment
if __name__ == '__main__':

    #region : Setup Scopes
    if IS_PHYSICAL_QCAR:
        fps = 10
    else:
        fps = 30

    scope = MultiScope(
        rows=2,
        cols=2,
        title='Environment Interpretation',
        fps=fps
    )

    # Polar Patch
    scope.addXYAxis(
        row=0,
        col=0,
        xLabel='Angle [deg]',
        yLabel='Range [m]'
    )
    scope.axes[0].attachImage()

    # Patch
    scope.addXYAxis(
        row=1,
        col=0,
        xLabel='x Position [m]',
        yLabel='y Position [m]'
    )
    scope.axes[1].attachImage()

    # Generated Map and followed trajectory
    scope.addXYAxis(
        row=0,
        col=1,
        rowSpan=2,
        xLabel='x Position [m]',
        yLabel='y Position [m]',
        xLim=(-4, 3),
        yLim=(-2, 6)
    )
    scope.axes[2].attachSignal(name='Measured', width=2, style='--.')
    scope.axes[2].attachImage()

    referencePath = pg.PlotDataItem(
        pen={'color': (85,168,104), 'width': 2},
        name='Reference'
    )
    referencePath.setData(waypointSequence[0, :], waypointSequence[1, :])
    scope.axes[2].plot.addItem(referencePath)
    #endregion

    #region : Setup threads, then run experiment
    controlThread = Thread(target=controlLoop)
    mappingThread = Thread(target=mappingLoop)

    controlThread.start()
    mappingThread.start()

    try:
        while controlThread.is_alive() and mappingThread.is_alive():
            MultiScope.refreshAll()
            time.sleep(0.01)
    finally:
        KILL_THREAD = True
        controlThread.join()
        mappingThread.join()
        gps.terminate()
    #endregion

    if not IS_PHYSICAL_QCAR:
        qlabs_setup.terminate()

    input('Experiment complete. Press any key to exit...')
#endregion