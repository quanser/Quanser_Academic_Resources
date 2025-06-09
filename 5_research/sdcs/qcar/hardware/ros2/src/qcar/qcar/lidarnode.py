#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
import numpy as np
from pal.products.qcar import QCarLidar
from sensor_msgs.msg import LaserScan
import time
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar LiDAR Node

class LIDARNode(Node):
	def __init__(self):
		super().__init__(
			'lidar_node',
			allow_undeclared_parameters=True,
			automatically_declare_parameters_from_overrides=True
		)

		# test out making custom QoS profile:
		self.qcar_qos_profile = QoSProfile(
				reliability   = 1,
				history 	  = 1,
				durability    = 1,
				depth 		  = 1)


		# Specify number of samples and data publish rate
		self.numMeasurements = 360	# Points
		self.publishRate = 1/10 	# Publish at 10 Hz


		# Lidar settings
		self.LIDAR_MEASUREMENT_MODE 	= 2
		self.LIDAR_INTERPOlATION_MODE	= 0

		# Lidar publisher constants:
		self.RANGE_MIN	= float(0)
		self.RANGE_MAX 	= float(12)

		self.previousScan = time.perf_counter()

		# Initialize RP Lidar
		self.lidar = QCarLidar(numMeasurements=self.numMeasurements,
							rangingDistanceMode= self.LIDAR_MEASUREMENT_MODE,
							interpolationMode= self.LIDAR_INTERPOlATION_MODE)

		# Sensor distances and angles measurements
		self.distances = np.zeros((self.numMeasurements,1))
		self.angles    = np.zeros((self.numMeasurements,1))

		# Start ROS publisher
		self._gen_publishers()


	#parse the publisher config to create publishers and timers
	def _gen_publishers(self):
		self.lidarPub = self.create_publisher(LaserScan, '/qcar/scan', 1)
		self.lidarTimer = self.create_timer(self.publishRate , self.lidar_callback)

	def lidar_callback(self):
		# Get time for current scan
		currentScanTime = time.perf_counter()
		self.lidar.read()

		# Delta in time between scans
		self.scan_time    = currentScanTime - self.previousScan
		self.previousScan = currentScanTime

		self.filter_lidar_data(self.lidar.distances, self.lidar.angles)

	def filter_lidar_data(self, currentScan, currentAngles):
		# Initial check for lidar values, usually zeros for the first 2s
		anglesNotZero = len(np.flatnonzero(currentAngles))

		if anglesNotZero > 0:

			# Check valid angles and ranges to be passed to LaseScan msg
			validIndex  	  = np.flatnonzero(currentAngles)
			validMeasurements = len(validIndex)
			validRanges       = currentScan[validIndex]
			validAngles       = currentAngles[validIndex]

			# Reverse the range data to be compatible with the C.C.W convention used by the LaserScan msg
			flippedRanges = np.flipud(validRanges)

			# Error checking for RP Lidar, some scans stop at 2*Pi midway through a scan
			checkedAngles = currentAngles>6.2

			# Only publish data where RP Lidar gives consistent angle measurements
			if not checkedAngles.any():

				# Specify scan angular range based on headings from measured lidar data
				self.angleMin 		 = float(validAngles[0])
				self.angleMax 		 = float(validAngles[-1])
				self.angleIncrement  = float(validAngles[-1]/validMeasurements)
				self.timeIncrement   = float((1/self.publishRate)/validMeasurements)
				self.process_lidar_data(flippedRanges,self.scan_time)

	def process_lidar_data(self, distances, scan_times):

		# Initialize LaserScan msg type
		scan = LaserScan()

		# What if range is a constant value?
		# distances = np.ones((20,1), dtype=float).flatten() # Dummy range data 1m from center
		# scan.angle_min 		 = float(0) 			 # rad
		# scan.angle_max 		 = float(2*np.pi*0.2)	 # rad
		# scan.angle_increment   = float(2*np.pi*0.2/20) # rad/measurement

		scan.header.stamp    = self.get_clock().now().to_msg()
		scan.header.frame_id = 'lidar'
		scan.angle_min 		 = self.angleMin 	   # rad
		scan.angle_max 		 = self.angleMax 	   # rad
		scan.angle_increment = self.angleIncrement # rad/measurement
		scan.time_increment  = self.timeIncrement  # s/measurement
		scan.scan_time 		 = float(scan_times)   # seconds
		scan.range_min 		 = self.RANGE_MIN      # m
		scan.range_max       = self.RANGE_MAX      # m
		scan.ranges 		 = distances.tolist()  # m
		self.lidarPub.publish(scan)

	def stop_lidar(self):
		self.lidar.terminate()
		print('lidar terminated')
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Main

def main(args=None):
	rclpy.init(args=args)

	r = LIDARNode()
	while rclpy.ok():
		try:
			rclpy.spin_once(r)
		except KeyboardInterrupt:
			r.stop_lidar()
			break

	r.destroy_node()
	rclpy.shutdown()
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run

if __name__ == '__main__':
	main()
#endregion
