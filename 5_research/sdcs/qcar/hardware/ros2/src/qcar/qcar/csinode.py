#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from rclpy.qos import QoSHistoryPolicy, QoSDurabilityPolicy
from rclpy.duration import Duration

from pal.utilities.vision import Camera2D

from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar CSI Node

class CSINode(Node):
	def __init__(self):
		super().__init__(
			'csi_node',
			allow_undeclared_parameters=True,
			automatically_declare_parameters_from_overrides=True
		)

		# test out making custom QoS profile:
		self.qcar_qos_profile = QoSProfile(
				reliability   = QoSReliabilityPolicy.RELIABLE,
				history 	  = QoSHistoryPolicy.KEEP_LAST,
				durability    = QoSDurabilityPolicy.TRANSIENT_LOCAL,
				depth 		  = 1)

		self.config = {
			'publishers': ['csi_right', 'csi_left', 'csi_front', 'csi_back'],
			'csi_right_resolution': [640,480],
			'csi_left_resolution': [640,480],
			'csi_front_resolution': [640,480],
			'csi_back_resolution': [640,480],
			'csi_right_freq': 30,
			'csi_left_freq': 30,
			'csi_front_freq': 30,
			'csi_back_freq': 30}

		# Start ROS publisher
		self._parse_config()
		self._gen_publishers()

	#parse the ROS2 parameters for the desired config settings from the launch file
	def _parse_config(self):
		params = [p for p in self._parameters]
		for item in self.config:
			if item in params:
				self.config[item] = self.get_parameter(item).value

	#parse the publisher config to create publishers and timers
	def _gen_publishers(self):


		for publisher in self.config['publishers']:
			self.bridge = CvBridge()

			if publisher.lower() == 'csi_right':

				self.rightCamPublisher = self.create_publisher(CompressedImage,
														'/qcar/csi_right',
														self.qcar_qos_profile)

				self.csi1 = Camera2D(cameraId="0",
							frameRate=self.config["csi_right_freq"],
							frameWidth=self.config["csi_right_resolution"][0],
							frameHeight=self.config["csi_right_resolution"][1])

				self.camRightTimer  = self.create_timer(self.config["csi_right_freq"],
											self.cam_right_callback)

			elif publisher.lower() == 'csi_left':

				self.leftCamPublisher = self.create_publisher(CompressedImage,
														'/qcar/csi_left',
														self.qcar_qos_profile)

				self.csi3 = Camera2D(cameraId="2",
							frameRate=self.config["csi_left_freq"],
							frameWidth=self.config["csi_left_resolution"][0],
							frameHeight=self.config["csi_left_resolution"][1])

				self.camLeftTImer = self.create_timer(1/self.config["csi_left_freq"],
											self.cam_left_callback)

			elif publisher.lower() == 'csi_front':

				self.frontCamPublisher = self.create_publisher(CompressedImage,
															'/qcar/csi_front',
														self.qcar_qos_profile)

				self.csi4 = Camera2D(cameraId="3",
							frameRate=self.config["csi_front_freq"],
							frameWidth=self.config["csi_front_resolution"][0],
							frameHeight=self.config["csi_front_resolution"][1])

				self.camFrontTimer = self.create_timer(1/self.config["csi_front_freq"],
												self.cam_front_callback)

			elif publisher.lower() == 'csi_back':

				self.backCamPublisher = self.create_publisher(CompressedImage,
														'/qcar/csi_back',
														self.qcar_qos_profile)

				self.csi2 = Camera2D(cameraId="1",
							frameRate=self.config["csi_back_freq"],
							frameWidth=self.config["csi_back_resolution"][0],
							frameHeight=self.config["csi_back_resolution"][1])

				self.camBackTimer = self.create_timer(1/self.config["csi_back_freq"],
												self.cam_back_callback)

			else:

				self.get_logger().warn("Unsupported publisher `{}` for qcar node.".format(publisher))


	def cam_right_callback(self):

		cameraInfo = self.rightCamPublisher

		# read CSI camera information based on camera settings
		self.csi1.read()

		# Conversion and publishing camera image infromation
		publishImage1 				  = self.bridge.cv2_to_compressed_imgmsg(self.csi1.imageData, dst_format='jpg')
		publishImage1.header.stamp 	  =  self.get_clock().now().to_msg()
		publishImage1.header.frame_id = 'cam_img_input1'
		cameraInfo.publish(publishImage1)


	def cam_back_callback(self):
		cameraInfo = self.backCamPublisher

		# read CSI camera information based on camera settings
		self.csi2.read()

		# Conversion and publishing camera image infromation
		publishImage2 				  = self.bridge.cv2_to_compressed_imgmsg(self.csi2.imageData, dst_format = 'jpg')
		publishImage2.header.stamp 	  =  self.get_clock().now().to_msg()
		publishImage2.header.frame_id = 'cam_img_input2'
		cameraInfo.publish(publishImage2)


	def cam_left_callback(self):
		cameraInfo =self.leftCamPublisher

		# read CSI camera information based on camera settings
		self.csi3.read()

		# Conversion and publishing camera image infromation
		publishImage3 				  = self.bridge.cv2_to_compressed_imgmsg(self.csi3.imageData, dst_format = 'jpg')
		publishImage3.header.stamp    =  self.get_clock().now().to_msg()
		publishImage3.header.frame_id = 'cam_img_input3'
		cameraInfo.publish(publishImage3)


	def cam_front_callback(self):
		cameraInfo = self.frontCamPublisher

		# read CSI camera information based on camera settings
		self.csi4.read()

		# Conversion and publishing camera image infromation
		publishImage4 				  = self.bridge.cv2_to_compressed_imgmsg(self.csi4.imageData, dst_format = 'jpg')
		publishImage4.header.stamp 	  =  self.get_clock().now().to_msg()
		publishImage4.header.frame_id = 'cam_img_input4'
		cameraInfo.publish(publishImage4)



	def stop_csi(self):
		print("\n stopping CSI Nodes please wait...")

		# Checking if the stream is indeed open, close the ones that are open.
		for publisher in self.config['publishers']:

			if publisher.lower() == 'csi_right':
				self.csi1.terminate()

			elif publisher.lower() == 'csi_left':
				self.csi2.terminate()

			elif publisher.lower() == 'csi_front':
				self.csi3.terminate()

			elif publisher.lower() == 'csi_back':
				self.csi4.terminate()
			else:
				print(" No CSI camera to close")

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Main

def main(args=None):
	rclpy.init(args=args)
	r = CSINode()
	while rclpy.ok():
		try:
			rclpy.spin_once(r)
		except KeyboardInterrupt:
			r.stop_csi()
			break
	r.destroy_node()
	rclpy.shutdown()
	print("CSI nodes have been stopped....")
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run

if __name__ == '__main__':
	main()
#endregion
