#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
import numpy as np
from pal.products.qcar import QCar
from geometry_msgs.msg import Vector3Stamped
from sensor_msgs.msg import BatteryState, Imu
import time
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar Drive Node

class QCarNode(Node):

	def __init__(self):
		super().__init__(
			'qcar_node',
			allow_undeclared_parameters=True,
			automatically_declare_parameters_from_overrides=True
		)

		# test out making custom QoS profile:
		self.qcar_qos_profile = QoSProfile(
				reliability   = 1,
				history 	  = 1,
				durability    = 1,
				depth 		  = 1)

		# User configurable publishers and publisher rates
		self.config = {
			'publishers': ['imu', 'battery', 'velocity'],
			'imu_publish_frequency': 100,
			'battery_publish_frequency': 1,
			'velocity_publish_frequency': 10}


		# Initialize publisher data
		self.dataIMU 	 	= np.zeros((6,1))
		self.dataBattery 	= 0
		self.linearVelocity = 0



		# Initialize Publishers
		self.imuPublisher = self.create_publisher(Imu, 
												'/qcar/imu', 
												self.qcar_qos_profile)

		self.imuTimer     = self.create_timer(1/self.config["imu_publish_frequency"],
												 self.IMU_callback)

		self.batteryPublisher = self.create_publisher(BatteryState, 
												'/qcar/stateBattery', 
												self.qcar_qos_profile)
		
		self.batteryTimer 	  = self.create_timer(1/self.config["battery_publish_frequency"],
												self.battery_callback)


		self.carVelocityPublisher = self.create_publisher(Vector3Stamped,
												'/qcar/velocity', 
												self.qcar_qos_profile)

										
		self.carVelocityTimer 	  = self.create_timer(1/self.config["velocity_publish_frequency"],
												self.velocity_callback)


		# Initialize QCar Subscribers
		self.command   = np.array([0, 0])
		self.motor_cmd = np.array([0, 0])
		self.LEDs      = np.array([0, 0, 0, 0, 0, 0, 1, 1])

		# Subscriber for user throttle and steering commands
		self.commandSubscriber = self.create_subscription(Vector3Stamped,
														'/qcar/user_command', 
														self.process_cmd, 1)

		# Configure QCar properties
		self.taskRate = int(500) #Hz
		self.hardware = 1
		self.readMode = 1

		# Initialize QCar using task based I/O
		self.myCar = QCar( readMode=self.readMode,
							frequency=self.taskRate)


	# Taskbased implementation of QCar control
	def QCar_Taskbase(self):
		self.start_time = time.perf_counter()

		# Reading QCar data using task based IO
		self.myCar.read_write_std(throttle= self.command[0],
								  steering= self.command[1],
								  LEDs=self.LEDs)

		# Split QCar Read data
		self.dataIMU        = np.concatenate((self.myCar.accelerometer, self.myCar.gyroscope))
		dataTach            = self.myCar.motorTach
		self.dataBattery    = self.myCar.batteryVoltage
		self.linearVelocity = dataTach*(1/self.myCar.ENCODER_COUNTS_PER_REV/4)*self.myCar.PIN_TO_SPUR_RATIO*2*np.pi*self.myCar.WHEEL_RADIUS


	# Configure Callback functions for publishing sensor information
	def IMU_callback(self):

		dataIMU = self.dataIMU

		# Initialize Imu msg type
		stateIMU 					   = Imu()
		stateIMU.header.stamp 		   = self.get_clock().now().to_msg()
		stateIMU.header.frame_id 	   = 'imu'
		stateIMU.angular_velocity.x    = float(dataIMU[0])
		stateIMU.angular_velocity.y    = float(dataIMU[1])
		stateIMU.angular_velocity.z    = float(dataIMU[2])
		stateIMU.linear_acceleration.x = float(dataIMU[3])
		stateIMU.linear_acceleration.y = float(dataIMU[4])
		stateIMU.linear_acceleration.z = float(dataIMU[5])
		self.imuPublisher.publish(stateIMU)

	def battery_callback(self):

		batteryVoltage = self.dataBattery

		# Initialize BatteryState msg type
		stateBattery                 = BatteryState()
		stateBattery.header.stamp    = self.get_clock().now().to_msg()
		stateBattery.header.frame_id = 'battery_voltage'
		stateBattery.voltage         = batteryVoltage
		self.batteryPublisher.publish(stateBattery)

	def velocity_callback(self):

		linearVelocity = self.linearVelocity

		# Initialize Vector3Stamped msg type
		stateVelocity 				  = Vector3Stamped()
		stateVelocity.header.stamp    = self.get_clock().now().to_msg()
		stateVelocity.header.frame_id = 'car_velocity'
		stateVelocity.vector.x 		  = float(np.cos(self.command[1]) * linearVelocity)
		stateVelocity.vector.y        = float(np.sin(self.command[1]) * linearVelocity)
		self.carVelocityPublisher.publish(stateVelocity)

	def process_cmd(self, inputCommand):

		# Throttle and steering command from command publisher
		vel_cmd      = inputCommand.vector.x
		str_cmd      = inputCommand.vector.y
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

#region : main
def main(args=None):
	rclpy.init(args=args)
	r = QCarNode()

	while True:
		try:
			rclpy.spin_once(r)
			r.QCar_Taskbase()
		except KeyboardInterrupt:

			r.stop_qcar()
			r.destroy_node()
			rclpy.shutdown()
			break
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : run
if __name__ == '__main__':
	main()
#endregion
