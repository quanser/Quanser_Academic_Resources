"""geometry.py: A module for managing coordinate frames and transformations.

This module provides the Geometry and MobileRobotGeometry classes, which allow
users to manage a collection of coordinate frames and perform transformations
between them. The Geometry class stores the frames and their transformations as
a directed graph, where nodes represent frames and edges represent
transformations. Users can add, modify, and retrieve transformations, as well
as perform operations such as obtaining a frame's pose or translation in
different representations (Euler angles, quaternions, rotation matrices, etc.).
"""
import numpy as np
from pytransform3d import rotations as pr
from pytransform3d import transformations as pt
from pytransform3d.transform_manager import TransformManager


#TODO: Can be sped up by caching generated TMs
class Geometry:
    """
    A class for managing frames and transformations in a 3D coordinate system.

    This class provides a convenient interface for adding frames, retrieving,
    and setting transformations, as well as converting between different
    rotation representations. The Geometry class is built on top of the
    pytransform3d package, which is responsible for handling the underlying
    data organization and transformations.
    """

    def __init__(self):
        """Initialize a new Geometry instance with a default 'world' frame."""
        self._tm = TransformManager()
        self.defaultFrame = 'world'

    def add_frame(self, name, p=[0,0,0], R=np.eye(3), base=None):
        """Add a new frame, defined relative to the specified base frame.

        Add a new frame with a specified name, position, rotation, and
        optional base frame.

        Args:
            name (str): The name of the new frame.
            p (list or array): The position of the new frame relative to the
                base frame (default [0, 0, 0]).
            R (array): The rotation matrix representing the orientation of the
                new frame relative to the base frame (default identity matrix).
            base (str, optional): The name of the base frame to which the new
                frame is relative (default is the 'world' frame).
        """
        if base is None: base = self.defaultFrame

        T = pt.transform_from(R, p)
        self._tm.add_transform(name, base, T)

    # ===== Get Functions =====
    def get_frames(self):
        """Get a list of all frame names in the calling instance.

        Returns:
            list: A list of frame names.
        """
        return self._tm.nodes

    def get_transform(self, frame, base=None):
        """Get the 4x4 transformation matrix between the frame and base.

        Args:
            frame (str): The name of the frame to get the transform from.
            base (str, optional): The name of the base frame (default is the
                'world' frame).

        Returns:
            array: A 4x4 transformation matrix.
        """
        if base is None: base = self.defaultFrame
        return self._tm.get_transform(frame, base)

    def get_translation(self, frame, base=None):
        """Get the translation vector between the frame and base.

        Args:
            frame (str): The name of the frame to get the translation from.
            base (str, optional): The name of the base frame (default is the
                'world' frame).

        Returns:
            array: A 3-element translation vector.
        """
        if base is None: base = self.defaultFrame
        return self._tm.get_transform(frame, base)[0:3,3]

    def get_rotation_rm(self,frame,base=None):
        """Get the rotation matrix between the specified frame and base.

        Args:
            frame (str): The name of the frame to get the rotation matrix from.
            base (str, optional): The name of the base frame (default is the
                'world' frame).

        Returns:
            array: A 3x3 rotation matrix.
        """
        if base is None: base = self.defaultFrame
        return self._tm.get_transform(frame, base)[0:3,0:3]

    def get_rotation_ea(self, frame, base=None):
        """Get the Euler angles (extrinsic XYZ) between frame and base.

        Args:
            frame (str): The name of the frame to get the Euler angles from.
            base (str, optional): The name of the base frame (default is the
                'world' frame).

        Returns:
            array: A 3-element array of Euler angles (extrinsic XYZ).
        """
        if base is None: base = self.defaultFrame
        return pr.extrinsic_euler_xyz_from_active_matrix(
            self._tm.get_transform(frame, base)[0:3,0:3]
        )

    def get_rotation_q(self, frame, base=None):
        """Get the quaternion representing the rotation between frame and base.

        Args:
            frame (str): The name of the frame to get the quaternion from.
            base (str, optional): The name of the base frame (default is the
                'world' frame).

        Returns:
            array: A 4-element quaternion (scalar last).
        """
        if base is None: base = self.defaultFrame
        return self.get_pose_pq(frame, base)[3:7]

    def get_pose_pea(self, frame, base=None):
        """Get the pose (position and Euler angles) of frame w.r.t. base.

        Get the pose of the specified frame with respect to the given base
        frame.

        Args:
            frame (str): The name of the frame to get the pose from.
            base (str, optional): The name of the base frame (default is the
                'world' frame).

        Returns:
            array: A 6-element array with the first 3 elements representing the
                position and the last 3 elements representing the Euler angles
                (extrinsic XYZ).
        """
        if base is None: base = self.defaultFrame
        T = self._tm.get_transform(frame, base)
        p = T[0:3,3]
        ea = pr.extrinsic_euler_xyz_from_active_matrix(T[0:3,0:3])
        return  np.concatenate((p, ea))

    def get_pose_pq(self, frame, base=None):
        """Get the pose (position and quaternion) of frame w.r.t. base.

        Get the pose of the specified frame with respect to the given base
        frame.

        Args:
            frame (str): The name of the frame to get the pose from.
            base (str, optional): The name of the base frame (default is the
                'world' frame).

        Returns:
            array: A 7-element array with the first 3 elements representing the
                position and the last 4 elements representing the quaternion
                (scalar last).
        """
        if base is None: base = self.defaultFrame
        return pt.pq_from_transform(self.get_transform(frame, base))

    # ===== Set functions =====
    def set_transform(self, T, frame, base=None):
        """Set the 4x4 transformation matrix for frame relative to base.

        Args:
            T (array): The 4x4 transformation matrix.
            frame (str): The name of the frame to set the transform for.
            base (str, optional): The name of the base frame (default is the
                'world' frame).
        """
        if base is None: base = self.defaultFrame
        if (frame, base) in self._tm.transforms:
            self._tm.transforms[frame,base] = T

    def set_pose_prm(self, p, R, frame, base=None):
        """Set the pose (position and rotation matrix) of frame w.r.t. base.

        Set the pose of the specified frame with respect to the given base
        frame.

        Args:
            p (array): The position vector.
            R (array): The rotation matrix.
            frame (str): The name of the frame to set the pose for.
            base (str, optional): The name of the base frame (default is the
                'world' frame).
        """
        if base is None: base = self.defaultFrame
        if (frame, base) in self._tm.transforms:
            self._tm.transforms[frame,base][0:3,3] = p
            self._tm.transforms[frame,base][0:3,0:3] = R

    def set_pose_pea(self, pose, frame, base=None):
        """Set the pose (position and Euler angles) of frame w.r.t. base.

        Set the pose of the specified frame with respect to the given base
        frame.

        Args:
            pose (array): A 6-element array with the first 3 elements
                representing the position and the last 3 elements representing
                the Euler angles (extrinsic XYZ).
            frame (str): The name of the frame to set the pose for.
            base (str, optional): The name of the base frame (default is the
                'world' frame).
        """
        if base is None: base = self.defaultFrame
        if (frame, base) in self._tm.transforms:
            self._tm.transforms[frame,base][0:3,3] = pose[0:3]
            self._tm.transforms[frame,base][0:3,0:3] =\
                pr.active_matrix_from_extrinsic_euler_xyz(pose[3:6])

    def set_pose_pq(self, pose, frame, base=None):
        """Set the pose (position and quaternion) of frame w.r.t. base.

        Set the pose of the specified frame with respect to the given base
        frame.

        Args:
            pose (array): A 7-element array with the first 3 elements
                representing the position and the last 4 elements representing
                the quaternion (scalar last).
            frame (str): The name of the frame to set the pose for.
            base (str, optional): The name of the base frame (default is the
                'world' frame).
        """
        if base is None: base = self.defaultFrame
        if (frame, base) in self._tm.transforms:
            self._tm.transforms[frame,base] =\
                pt.transform_from_pq(pose)

    def set_translation(self, p, frame, base=None):
        """Set the translation vector for frame relative to the base.

        Args:
            p (array): The position vector.
            frame (str): The name of the frame to set the translation for.
            base (str, optional): The name of the base frame (default is the
                'world' frame).
        """
        if base is None: base = self.defaultFrame
        if (frame, base) in self._tm.transforms:
            self._tm.transforms[frame,base][0:3,3] = p
        pass

    def set_rotation_rm(self, R, frame, base=None):
        """Set the rotation matrix for frame relative to base.

        Args:
            R (array): The rotation matrix.
            frame (str): The name of the frame to set the rotation for.
            base (str, optional): The name of the base frame (default is the
                'world' frame).
        """
        if base is None: base = self.defaultFrame
        if (frame, base) in self._tm.transforms:
            self._tm.transforms[frame,base][0:3,0:3] = R

    def set_rotation_ea(self, ea, frame, base=None):
        """Set the Euler angles (extrinsic XYZ) for frame relative to base.

        Args:
            ea (array): A 3-element array of Euler angles (extrinsic XYZ).
            frame (str): The name of the frame to set the Euler angles for.
            base (str, optional): The name of the base frame (default is the
                'world' frame).
        """
        if base is None: base = self.defaultFrame
        if (frame, base) in self._tm.transforms:
            self._tm.transforms[frame,base][0:3,0:3] =\
                pr.active_matrix_from_extrinsic_euler_xyz(ea)

    def set_rotation_q(self, q, frame, base=None):
        """Set the quaternion for the frame relative to base.

        Args:
            q (array): A 4-element quaternion (scalar last).
            frame (str): The name of the frame to set the quaternion for.
            base (str, optional): The name of the base frame (default is the
                'world' frame).
        """
        if base is None: base = self.defaultFrame
        if (frame,base) in self._tm.transforms:
            self._tm.transforms[frame,base][0:3,0:3] =\
                pr.matrix_from_quaternion(q)


class MobileRobotGeometry(Geometry):
    """A class for managing frames and transformations for mobile robots.

    This class extends the Geometry class and provides additional functionality
    for managing the coordinate frames and transformations related to mobile
    robots. It offers methods for getting and setting 2D poses and headings,
    as well as methods for setting the pose of the robot body in different
    representations.
    """

    def __init__(self):
        """Initialize a new instance and add the 'body' frame."""
        super().__init__()
        self.add_frame(name='body')

    def get_pose_2d(self, frame='body', base='world'):
        """Get the 2D pose (x, y, heading) of frame relative to base.

        Args:
            frame (str, optional): The name of the frame to get the 2D pose for
                (default is 'body').
            base (str, optional): The name of the base frame
                (default is 'world').

        Returns:
            array: A 3-element array representing the 2D pose (x, y, heading).
        """
        return np.concatenate((
            self._tm.get_transform(frame, base)[0:2,3],
            self.get_heading(frame, base)
        ))

    def get_heading(self, frame='body', base='world'):
        """Get the heading angle of frame relative base.

        Args:
            frame (str, optional): The name of the frame to get the heading for
                (default is 'body').
            base (str, optional): The name of the base frame
                (default is 'world').

        Returns:
            float: The heading angle in radians.
        """
        h = np.dot(self.get_rotation_rm(frame,base), [[1],[0],[0]])
        return np.arctan2(h[1], h[0])

    def set_pose_2d(self, pth, frame='body', base='world'):
        """Set the 2D pose (x, y, heading) of frame relative to base.

        Args:
            pth (array): A 3-element array representing the 2D pose
                (x, y, heading).
            frame (str, optional): The name of the frame to set the 2D pose for
                (default is 'body').
            base (str, optional): The name of the base frame
                (default is 'world').
        """
        if (frame, base) in self._tm.transforms:
            self._tm.transforms[frame,base][0:2,3] = pth[0:2]
            self._tm.transforms[frame,base][0:3,0:3] =\
                MobileRobotGeometry._rm_from_heading(pth[2])

    def set_body_from_T(self,T,frame):
        """
        Sets the body frame relative to the world frame using a transformation
        matrix 'T', defined relative to 'frame'.

        Args:
            T (array): The 4x4 transformation matrix.
            frame (str): The name of the frame relative to which T is defined.
        """
        self._tm.transforms['body','world'] =\
            T @ self._tm.get_transform('body',frame)

    def set_body_from_Rp(self,R,p,frame):
        """Set the body frame relative to the world frame using a rotation
            matrix R and a translation vector p relative to another frame.

        Args:
            R (array): The 3x3 rotation matrix.
            p (array): The 3-element translation vector.
            frame (str): The name of the frame relative to which R and p
                are defined.
        """
        self.set_body_from_T(pt.transform_from(R,p), frame)

    def set_body_from_pea(self, p, ea, frame):
        """Set the body frame relative to the world frame using a translation
            vector p and extrinsic Euler angles ea relative to another frame.

        Args:
            p (array): The 3-element translation vector.
            ea (array): The 3-element extrinsic Euler angles (roll, pitch, yaw).
            frame (str): The name of the frame relative to which p and ea
                are defined.
        """
        self.set_body_from_Rp(
             pr.active_matrix_from_extrinsic_euler_xyz(ea),
             p,
             frame
        )

    def set_body_from_pth(self, p, th, frame):
        """Set the body frame relative to the world frame using a translation
            vector p and a heading angle th relative to another frame.

        Args:
            p (array): The 3-element translation vector.
            th (float): The heading angle in radians.
            frame (str): The name of the frame relative to which p and th are
                defined.
        """
        self.set_body_from_Rp(
             pr.active_matrix_from_extrinsic_euler_xyz([0, 0, th]),
             p,
             frame
        )

    def _rm_from_heading(th):
        """Create a 3x3 rotation matrix from a heading angle.

        Args:
            th (float): The heading angle in radians.

        Returns:
            array: The 3x3 rotation matrix corresponding to the heading angle.
        """
        cth = np.cos(th)
        sth = np.sin(th)
        return [[cth,-sth,0], [sth,cth,0], [0,0,1]]
    