#!/usr/bin/env python3

from __future__ import division, print_function, absolute_import

# Import libraries
import roslib
import rospy
import numpy as np
from quanser_core.p_QArm import QArm, QArmUtilities
from quanser_core.q_misc import Calculus, Utilities
from qarm_msgs.msg import AllCommands, AllJointState

class JointSpaceNode(object):

	def __init__(self):
		super().__init__()

		# Take user command
		self.take_user_input = QArmUtilities.take_user_input_joint_space

		# Set up default LED colour
		self.ledCmd = np.array([0, 1, 1], dtype=np.float64)

		# Set up publisher for the command
		self.pub_cmd = rospy.Publisher('/qarm/all_command', AllCommands, queue_size=100)


	def take_input(self):
		result = self.take_user_input()
		phiCmd = result[0:4]
		gripCmd = result[4]
		ac = AllCommands()
		ac.jointcommand.joint_command = phiCmd
		ac.grippercommand.gripper_command = gripCmd
		ac.ledcommand.RGB = self.ledCmd
		self.pub_cmd.publish(ac)

if __name__ == '__main__':
	rospy.init_node('joint_space_command_node')

	# Command Rate at 1 Hz
	rate = rospy.Rate(1)

	r = JointSpaceNode()


	while not rospy.is_shutdown():
		r.take_input()
		rate.sleep()



