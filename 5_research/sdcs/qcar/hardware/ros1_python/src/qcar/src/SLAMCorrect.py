#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

import rospy
import numpy as np
from pyquaternion import Quaternion
from geometry_msgs.msg import PoseStamped
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar Slam Pose Correction

class PoseCorrect(object):
    def __init__(self):

        # Publish frequency is set to the speed at which the slam pose from Hector is published
        publishFreq = 20
        self.slamPose = rospy.Subscriber('/slam_out_pose',
                                            PoseStamped,
                                            self.pose_msg)

        self.slamPoseCorrected = rospy.Publisher('/slam_pose_corrected',
                                            PoseStamped,
                                            queue_size = 100 )

        # Initialize cashed variables
        self.slamPoseMsg = PoseStamped()
        self.poseRotated = Quaternion()

        # Set up a timer for publishing the corrected pose
        self.publisherTimer = rospy.Timer(rospy.Duration(1.0/publishFreq),
                                                    self.pose_publisher)


    def pose_msg(self, slamPose):
        # ============== Variable Initialization ==============
        # Variable used to store the original pose from hector slam
        poseOrig = Quaternion()
        poseOrig[0] = slamPose.pose.orientation.x
        poseOrig[1] = slamPose.pose.orientation.y
        poseOrig[2] = slamPose.pose.orientation.z
        poseOrig[3] = slamPose.pose.orientation.w

        self.slamPoseMsg = slamPose

        # Rotate slam pose by 90 deg CCW to correct the RPLiDAR pose error
        qRotate = Quaternion(axis = [1, 0, 0], angle = -np.pi/4)

        # create a vector to store the normalised pose from Hector SLAM
        slamPoseNormal = poseOrig.normalised
        self.poseRotated = qRotate.rotate(slamPoseNormal)

    def pose_publisher(self):
        # Variable used for publishing rotated pose
        slamPoseRotated = PoseStamped()

        # Correct the x,y,z to match the QCar vehicle frame
        slamPoseRotated.pose.position.x = self.slamPoseMsg.pose.position.x
        slamPoseRotated.pose.position.y = self.slamPoseMsg.pose.position.y
        slamPoseRotated.pose.position.z = self.slamPoseMsg.pose.position.z

        # Define new quaternion orientation for corrected pose
        slamPoseRotated.pose.orientation.x = self.poseRotated[0]
        slamPoseRotated.pose.orientation.y = self.poseRotated[1]
        slamPoseRotated.pose.orientation.z = self.poseRotated[2]
        slamPoseRotated.pose.orientation.w = self.poseRotated[3]

        # Passing time and frame id from slam_out_pose to the corrected node.
        slamPoseRotated.header.frame_id = self.slamPoseMsg.header.frame_id
        slamPoseRotated.header.stamp = self.slamPoseMsg.header.stamp

        self.slamPoseCorrected.publish(slamPoseRotated)
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run

if __name__ == '__main__':
    rospy.init_node('PoseCorrect_node',disable_signals = True)
    r = PoseCorrect()
    rospy.spin()
#endregion
