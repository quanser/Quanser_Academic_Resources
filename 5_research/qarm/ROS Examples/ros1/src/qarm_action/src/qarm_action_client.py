#!/usr/bin/env python3

import rospy
import actionlib
import numpy as np
import sys
from quanser_core.p_QArm import QArm, QArmUtilities
from qarm_msgs.msg import QArmActionGoal, AllCommands, AllJointState, moveQArmAction, moveQArmActionGoal, moveQArmActionResult, moveQArmFeedback, moveQArmGoal, moveQArmResult

def qarm_action_client(target_position):
	# Creates the SimpleActionClient, passing the type of the action
	# (ActionServer) to the constructor.
	client = actionlib.SimpleActionClient('ActionServer', moveQArmAction)

	# Waits until the action server has started up and started
	# listening for goals.
	client.wait_for_server()
	rospy.loginfo('Found a ActionServer! Game is on!')

	# Creates a target position to send to the action server.
	# goal = QArmActionGoal()
	# goal.task_space_position_and_gripper = target_position
	this_goal = QArmActionGoal()
	this_goal.task_space_position_and_gripper = target_position
	goal = moveQArmGoal(qarm_action_goal=this_goal)

	# Sends the goal to the action server.
	client.send_goal(goal)

	# # Waits for the server to finish performing the action.
	client.wait_for_result()

	# # Prints out the result of executing the action
	return client.get_result()

def goal_sender():
	result = qarm_action_client([0.49, 0, 0.49, 0])
	result = qarm_action_client([0.30, 0.3, 0.1, 0])
	result = qarm_action_client([0.49, 0, 0.49, 0])
	result = qarm_action_client([0.30, -0.3, 0.1, 0])
	result = qarm_action_client([0.49, 0, 0.49, 0])
	result = qarm_action_client([-0.30, -0.3, 0.1, 0])
	result = qarm_action_client([0.49, 0, 0.49, 0])
	result = qarm_action_client([-0.30, 0.3, 0.1, 0])
	result = qarm_action_client([0.49, 0, 0.49, 0])
	# result = qarm_action_client([0.45, 0, 0.45, 0])
	# # print(result)
	# result = qarm_action_client([0.45, 0, 0.49, 0])
	# result = qarm_action_client([0.55, -0.2, 0.62, 0.2])
	# result = qarm_action_client([0.30, 0.3, 0.1, 0])

if __name__ == '__main__':
	try:
		rospy.init_node('ActionClient')
		goal_sender()
	except rospy.ROSInterruptException:
		print("program interrupted before completion", file=sys.stderr)