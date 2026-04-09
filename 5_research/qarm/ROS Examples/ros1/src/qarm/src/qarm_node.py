#!/usr/bin/env python3

from __future__ import division, print_function, absolute_import

# Import libraries
import roslib
import rospy
import numpy as np
from quanser_core.p_QArm import QArm, QArmUtilities
from quanser_core.q_misc import Calculus, Utilities
from qarm_msgs.msg import AllCommands, AllJointState

class QarmNode(object):

	def __init__(self):
		super().__init__()

		# Initialize QArm
		self.myArm = QArm()

		# Initialize some np arrays
		self.joint_command = np.array([0, 0, 0, 0], dtype=np.float64)
		self.gripper_command = np.zeros(1, dtype=np.float64)
		self.LED_command = np.array([0, 0, 0], dtype=np.float64)

		# Initialize Publihser
		self.joint_state_pub = rospy.Publisher('/qarm/all_joint_state', AllJointState, queue_size=100)

		# Initialize Subscriber
		self.cmd_sub_ = rospy.Subscriber('/qarm/all_command', AllCommands, self.process_cmd, queue_size=100)
		
		

	def process_cmd(self, sub_cmd):
		# Getting Joint command from all_command
		self.joint_command = np.array(sub_cmd.jointcommand.joint_command)

		# Getting gripper command from all_command
		self.gripper_command[0] = sub_cmd.grippercommand.gripper_command

		# Getting LED from all_command
		self.LED_command = np.array(sub_cmd.ledcommand.RGB)


	def write_arm_and_pub_states(self):
		if self.myArm.status == True:
			# Write them to the arm
			self.myArm.read_write_std(phiCMD=self.joint_command, grpCMD=self.gripper_command, baseLED=self.LED_command)

			# Pub All Joint States
			ajs = AllJointState()
			ajs.header.stamp = rospy.Time.now()
			ajs.header.frame_id = 'all_joint_state'
			ajs.joint_names = 'Base, Shoulder, Arm, Wrist, Gripper'
			ajs.joint_currents = self.myArm.measJointCurrent
			ajs.joint_positions = self.myArm.measJointPosition
			ajs.joint_speeds = self.myArm.measJointSpeed
			ajs.joint_pwms = self.myArm.measJointPWM
			ajs.joint_temperatures = self.myArm.measJointTemperature
			self.joint_state_pub.publish(ajs)
		else:
			print('The arm is not initialized properlly.')

	def terminate_arm(self):
		self.myArm.terminate()

if __name__ == '__main__':
	rospy.init_node('qarm_node')

	# QArm Rate at 200 Hz
	rate = rospy.Rate(200)
	
	r = QarmNode()
	while not rospy.is_shutdown():
		r.write_arm_and_pub_states()
		rate.sleep()
	r.terminate_arm()

