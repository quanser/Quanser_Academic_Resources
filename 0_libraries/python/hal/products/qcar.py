"""This module contains QCar specific implementations of the hal.utilities.geometry features"""

from pytransform3d import rotations as pr   

from hal.utilities.geometry import MobileRobotGeometry
import numpy as np

class QCarGeometry(MobileRobotGeometry):
    """QCarGeometry class for defining QCar-specific frames of reference.

    This class inherits from the MobileRobotGeometry class and adds frames
    specific to the QCar, such as the front and rear axles, CSI sensors,
    IMU, Realsense, and RPLidar.
    """

    def __init__(self):
        """Initialize the QCarGeometry class with QCar-specific frames."""

        super().__init__()

        self.defaultFrame = 'body'

        # Body reference frame center is located at,
        # X: halfway between front and rear axles
        # Y: halway between left and right wheels
        # Z: 0.0103 m above the ground (chassis bottom)
        # the following frames are all defined w.r.t this center
        self.add_frame(
            name='CG',
            p=[0.0248, -0.0074, 0.0606],
            R=np.eye(3)
        )
        self.add_frame(
            name='front_axle',
            p=[0.1300, 0, 0.0207],
            R=np.eye(3)
        )
        self.add_frame(
            name='rear_axle',
            p=[-0.1300, 0, 0.0207],
            R=np.eye(3)
        )
        self.add_frame(
            name='csi_front',
            p=[0.1930, 0, 0.0850],
            R=pr.active_matrix_from_extrinsic_euler_xyz(
                [-np.pi/2, 0, -np.pi/2]
            )
        )
        self.add_frame(
            name='csi_left',
            p=[0.0140, 0.0438, 0.0850],
            R=pr.active_matrix_from_extrinsic_euler_xyz([-np.pi/2, 0, 0])
        )
        self.add_frame(
            name='csi_rear',
            p=[-0.1650, 0, 0.0850],
            R=pr.active_matrix_from_extrinsic_euler_xyz([-np.pi/2, 0, np.pi/2])
        )
        self.add_frame(
            name='csi_right',
            p=[0.0140, -0.0674, 0.0850],
            R=pr.active_matrix_from_extrinsic_euler_xyz([-np.pi/2, 0, np.pi])
        )
        self.add_frame(
            name='imu',
            p=[0.1278, 0.0223, 0.0792],
            R=np.eye(3)
        )
        self.add_frame(
            name='realsense',
            p=[0.0822, 0.0003, 0.1479],
            R=pr.active_matrix_from_extrinsic_euler_xyz(
                [-np.pi/2, 0, -np.pi/2]
            )
        )
        self.add_frame(
            name='rplidar',
            p=[-0.0108, 0, 0.1696],
            R=np.eye(3)
        )

        self.defaultFrame = 'world'

