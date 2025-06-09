#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

import rospy
from pal.utilities.gamepad import LogitechF710
from geometry_msgs.msg import Vector3Stamped
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar Command Node

class CommandNode(object):
	def __init__(self):
		super().__init__()
		self.gpad = LogitechF710()

		gamepadPublishRate = 1000 # Hz
		self.gpadPublisher = rospy.Publisher('/qcar/user_command',
											Vector3Stamped,
											queue_size=100)

		rate = rospy.Rate(gamepadPublishRate)

		# save joystick commands
		self.userCommand     = [0,0]
		self.throttleCommand = 0
		self.steeringCommand = 0

		while not rospy.is_shutdown():
			self.gamepad_control()
			rate.sleep()

	def gamepad_control(self):
		# check if there is new data from the logitech gamepad
		new = self.gpad.read()
		# Define user commands based on new signals
		if new and self.gpad.buttonLeft == 1:
			# Command to be +/- 0.3 radian
			self.steeringCommand = self.gpad.leftJoystickX*0.3

			# Configure throttle to be from 0 to + 30% PWM command
			self.throttleCommand = (self.gpad.trigger)*0.3

			# Change throttle direction when A is pressed
			if self.gpad.buttonA == 1:
				self.throttleCommand = self.throttleCommand*-1

		self.userCommand  = [self.throttleCommand, self.steeringCommand]
		self.process_command(new)

	def process_command(self, new):
		if new:
			commandPublisher = Vector3Stamped()
			commandPublisher.header.stamp = rospy.Time.now()
			commandPublisher.header.frame_id = 'command_input'
			commandPublisher.vector.x = float(self.userCommand[0])
			commandPublisher.vector.y = float(self.userCommand[1])
			self.gpadPublisher.publish(commandPublisher)

		else:
			commandPublisher = Vector3Stamped()
			commandPublisher.header.stamp = rospy.Time.now()
			commandPublisher.header.frame_id = 'command_input'
			commandPublisher.vector.x = float(self.userCommand[0])
			commandPublisher.vector.y = float(self.userCommand[1])
			self.gpadPublisher.publish(commandPublisher)

	def stop_gampad(self):
		self.gpad.terminate()
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run

if __name__ == '__main__':
	rospy.init_node('command_node')
	r = CommandNode()
	rospy.spin()
	if KeyboardInterrupt:
		r.stop_gampad()
		print("Gamepad has been stopped....")
#endregion
