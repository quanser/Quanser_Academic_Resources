#!/usr/bin/env python3

import rospy
import actionlib
import numpy as np
from quanser_core.p_QArm import QArm, QArmUtilities
from qarm_msgs.msg import AllCommands, AllJointState, moveQArmAction, moveQArmActionGoal, moveQArmActionResult, moveQArmFeedback, moveQArmGoal, moveQArmResult

class ActionServer(object):

	def __init__(self, name):
		super().__init__()

		# Initialize QArm
		self.myArm = QArm()

		# create messages that are used to publish feedback
		self._feedback = moveQArmFeedback()
		self._result = moveQArmResult()


		# Initialize some np arrays and stuff
		self.joint_command = np.array([0, 0, 0, 0], dtype=np.float64)
		self.gripper_command = np.zeros(1, dtype=np.float64)
		self.LED_command = np.array([0, 1, 1], dtype=np.float64)
		self.prev_phi = np.array([0, 0, 0, 0], dtype=np.float64)
		self.threshhold = 0.04

		self._action_name = name
		self._as = actionlib.SimpleActionServer(self._action_name, moveQArmAction, execute_cb=self.execute_cb, auto_start=False)
		self._as.start()


	def execute_cb(self, goal):
		if self.myArm.status == True:
			#helper variable
			r = rospy.Rate(1)
			success = True
			reached = False
			joint_check = np.array([0, 0, 0, 0])

			if self._as.is_preempt_requested():
				rospy.loginfo('%s: Preempted' % self._action_name)
				self.myArm.terminate()
				self._as.set_preempted()
				sucess = False

			positionCmd = goal.qarm_action_goal.task_space_position_and_gripper[0:3]
			gripperCmd = goal.qarm_action_goal.task_space_position_and_gripper[3]
			phi, phiOptimal = QArmUtilities.qarm_inverse_kinematics(QArmUtilities, positionCmd, 0, self.myArm.measJointPosition[0:4])
			self.joint_command = phiOptimal
			# print(self.joint_command)
			self.gripper_command[0] = gripperCmd
			self.myArm.read_write_std(phiCMD=self.joint_command, grpCMD=self.gripper_command, baseLED=self.LED_command)
			# wholejoints = np.array([self.joint_command, self.gripper_command])S
			while not reached:
				self.myArm.read_std()
				# for i in range(4):
				# 	if np.abs(self.joint_command[i] - (self.myArm.measJointPosition[0:4])[i]) <= self.threshhold:
				# 		joint_check[i] = 1
				joint_check = np.abs(self.joint_command - self.myArm.measJointPosition[0:4])
				print(np.linalg.norm(joint_check))
				
				# if all(x <= self.threshhold for x in joint_check):
				# 	reached = True
				if np.linalg.norm(joint_check) <= self.threshhold:
					reached = True

			# publish the feedback
			self._feedback.qarm_action_feedback.ajs.joint_currents = self.myArm.measJointCurrent
			self._feedback.qarm_action_feedback.ajs.joint_positions = self.myArm.measJointPosition
			self._feedback.qarm_action_feedback.ajs.joint_speeds = self.myArm.measJointSpeed
			self._feedback.qarm_action_feedback.ajs.joint_pwms = self.myArm.measJointPWM
			self._feedback.qarm_action_feedback.ajs.joint_temperatures = self.myArm.measJointTemperature
			self._as.publish_feedback(self._feedback)

			r.sleep()

			if success:
				self._result.qarm_action_result.result = 'QArm has reached the targeted position'
				# self._result.ready_for_next_goal = 1
				rospy.loginfo('%s: Succeeded' % self._action_name)
				self._as.set_succeeded(self._result)
		else:
			print('The arm is not initialized properlly.')
		
if __name__ == '__main__':
	rospy.init_node('ActionServer')
	server = ActionServer(rospy.get_name())
	# rospy.spin()

	