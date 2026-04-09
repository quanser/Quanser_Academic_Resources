#!/usr/bin/env python3

from __future__ import division, print_function, absolute_import

# Import libraries
import roslib
import rospy
import numpy as np
from quanser_core.p_QArm import QArm, QArmUtilities
from quanser_core.q_misc import Calculus, Utilities
from qarm_msgs.msg import AllCommands, AllJointState

class TaskSpaceNode(object):

	def __init__(self):
		super().__init__()

		# Take user command
		self.take_user_input = QArmUtilities.take_user_input_task_space

		#Initialize some np arrays
		self.prev_joint_state = np.array([0, 0, 0, 0], dtype=np.float64)

		# Set up default LED colour
		self.ledCmd = np.array([0, 1, 1], dtype=np.float64)
		
		# Initialize Publihser
		self.joint_state_pub = rospy.Publisher('/qarm/all_command', AllCommands, queue_size=100)

		# Setup subscriber coming from the QArm
		self.state_sub_ = rospy.Subscriber('/qarm/all_joint_state', AllJointState, self.get_joint_position, queue_size=100)

	def get_joint_position(self, sub_state):

		#Getting the joint position from QArm
		self.prev_joint_state = np.array(sub_state.joint_positions[0:4])

	def take_input(self):
		prev_phi = self.prev_joint_state
		result = self.take_user_input()
		positionCmd = result[0:3]
		gripCmd = result[3]
		phi, phiOptimal = QArmUtilities.qarm_inverse_kinematics(QArmUtilities, positionCmd, 0, prev_phi)
		ac = AllCommands()
		ac.jointcommand.joint_command = phiOptimal
		ac.grippercommand.gripper_command = gripCmd
		ac.ledcommand.RGB = self.ledCmd
		self.joint_state_pub.publish(ac)

if __name__ == '__main__':
	rospy.init_node('task_space_command_node')

	# Command Rate at 1 Hz
	rate = rospy.Rate(1)

	r = TaskSpaceNode()

	while not rospy.is_shutdown():
		r.take_input()
		rate.sleep()