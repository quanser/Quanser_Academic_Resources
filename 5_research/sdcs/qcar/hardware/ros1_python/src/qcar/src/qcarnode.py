#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

import rospy
import numpy as np
from pal.products.qcar import QCar
from geometry_msgs.msg import Vector3Stamped
from sensor_msgs.msg import BatteryState, Imu
import time
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar Drive Node

class QcarNode(object):

	def __init__(self):
		super().__init__()

		# Initialize publisher data
		self.dataIMU 	 	= np.zeros((6,1))
		self.dataBattery 	= 0
		self.linearVelocity = 0

		self.imuPublisher	= rospy.Publisher('/qcar/imu',
											Imu,
											queue_size= 10)

		self.batteryPublisher	= rospy.Publisher('/qcar/battery_state',
											BatteryState,
											queue_size=10)

		self.carVelocityPublisher = rospy.Publisher('/qcar/velocity',
											Vector3Stamped,
											queue_size=10)

		# Configure QCar properties
		self.taskRate = int(500) #Hz
		self.readMode = 0

		# Initialize QCar using task based I/O
		self.myCar = QCar( readMode=self.readMode,
							frequency=self.taskRate)

		self.sampleTime = 0.001
		self.command 	 = np.array([0, 0])
		self.LEDs        = np.array([0, 0, 0, 0, 0, 0, 1, 1])

		# Subscribe to user commands
		self.commandSubscriber = rospy.Subscriber('/qcar/user_command',
												Vector3Stamped,
												self.process_cmd,
												queue_size=100)

	def looping(self):

		while not rospy.is_shutdown():
			# talk to QCar
			self.myCar.read_write_std(throttle= self.command[0],
									steering= self.command[1],
									LEDs=self.LEDs)

			# Split QCar Read data
			dataIMU        = np.concatenate((self.myCar.accelerometer, self.myCar.gyroscope))
			dataTach       = self.myCar.motorTach
			dataBattery    = self.myCar.batteryVoltage
			linearVelocity = dataTach*(1/self.myCar.ENCODER_COUNTS_PER_REV/4)*self.myCar.PIN_TO_SPUR_RATIO*2*np.pi*self.myCar.WHEEL_RADIUS

			# IMU Topic
			# Initialize Imu msg type
			stateIMU 					   = Imu()
			stateIMU.header.stamp 		   = rospy.Time.now()
			stateIMU.header.frame_id 	   = 'base'
			stateIMU.angular_velocity.x    = float(dataIMU[0])
			stateIMU.angular_velocity.y    = float(dataIMU[1])
			stateIMU.angular_velocity.z    = float(dataIMU[2])
			stateIMU.linear_acceleration.x = float(dataIMU[3])
			stateIMU.linear_acceleration.y = float(dataIMU[4])
			stateIMU.linear_acceleration.z = float(dataIMU[5])
			self.imuPublisher.publish(stateIMU)


			# Battery Topic
			stateBattery 			 	 = BatteryState()
			stateBattery.header.stamp 	 = rospy.Time.now()
			stateBattery.header.frame_id = 'battery_voltage'
			stateBattery.voltage 		 = dataBattery
			self.batteryPublisher.publish(stateBattery)

			# Velocity Topic
			velocity_state 				   = Vector3Stamped()
			velocity_state.header.stamp    = rospy.Time.now()
			velocity_state.header.frame_id = 'car_velocity'
			velocity_state.vector.x 	   = float(np.cos(self.command[1]) * linearVelocity)
			velocity_state.vector.y 	   = float(np.sin(self.command[1]) * linearVelocity)
			self.carVelocityPublisher.publish(velocity_state)

			time.sleep(self.sampleTime)

	def process_cmd(self, sub_cmd):
		vel_cmd = sub_cmd.vector.x
		str_cmd = sub_cmd.vector.y - 0.01
		self.command = np.array([vel_cmd, str_cmd])

		# Configure LEDs
		if str_cmd > 0.3:
			self.LEDs[0] = 1
			self.LEDs[2] = 1
		elif str_cmd < -0.3:
			self.LEDs[1] = 1
			self.LEDs[3] = 1
		if str_cmd < 0:
			self.LEDs[5] = 1

	def stop_qcar(self):
		self.myCar.terminate()
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run

if __name__ == '__main__':
	rospy.init_node('qcar_node')
	r = QcarNode()
	r.looping()
	rospy.spin()
	if KeyboardInterrupt:
		r.stop_qcar()
		print("Stopping QCar")
#endregion
