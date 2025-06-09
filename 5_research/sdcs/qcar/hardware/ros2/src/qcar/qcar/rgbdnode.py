#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from rclpy.qos import QoSHistoryPolicy, QoSDurabilityPolicy

from pal.products.qcar import QCarRealSense

from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar Realsense Node

class RGBDNode(Node):
	def __init__(self):
		super().__init__(
		'rgbd_node',
		allow_undeclared_parameters=True,
		automatically_declare_parameters_from_overrides=True
		)


		# test out making custom QoS profile:
		self.qcar_qos_profile = QoSProfile(
				reliability   = QoSReliabilityPolicy.BEST_EFFORT,
				history 	  = QoSHistoryPolicy.KEEP_LAST,
				durability    = QoSDurabilityPolicy.VOLATILE,
				depth 		  = 10)

		self.config = {
			'publishers': ['rgbd_color', 'rgbd_depth'],
			'rgbd_color_resolution': [640, 480],
			'rgbd_depth_resolution': [640, 480],
			'rgbd_color_freq': 60,
			'rgbd_depth_freq': 90}

		self._parse_config()
		self._gen_publishers()

	def _parse_config(self):
		params = [p for p in self._parameters]
		for item in self.config:
			if item in params:
				self.config[item] = self.get_parameter(item).value

	#parse the publisher config to create publishers and timers
	def _gen_publishers(self):

		print("Color Stream  configuration is: frame rate `{}`, image size [W,H] = `{}`  .".format(self.config["rgbd_color_freq"],self.config["rgbd_color_resolution"]))
		print("Depth Stream  configuration is: frame rate `{}`, image size [W,H] = `{}`  .".format(self.config["rgbd_depth_freq"],self.config["rgbd_depth_resolution"]))

		for publisher in self.config['publishers']:
			self.bridge = CvBridge()

			if publisher.lower() == 'rgbd_color':

				self.imageColorPublisher = self.create_publisher(CompressedImage,
														'/qcar/rgbd_color',
														self.qcar_qos_profile)

				self.imageColor	= QCarRealSense(mode='RGB',
					frameWidthRGB  = self.config["rgbd_color_resolution"][0],
					frameHeightRGB = self.config["rgbd_color_resolution"][1],
					frameRateRGB   = self.config["rgbd_color_freq"])

				self.imageColorTimer = self.create_timer(1/self.config["rgbd_color_freq"],
													self.rgbd_color_callback)

			elif publisher.lower() == 'rgbd_depth':

				self.imageDepthPublisher = self.create_publisher(Image,
														'/qcar/rgbd_depth',
														self.qcar_qos_profile)

				self.imageDepth		 = QCarRealSense(mode='DEPTH',
					frameWidthDepth	 = self.config["rgbd_depth_resolution"][0],
					frameHeightDepth = self.config["rgbd_depth_resolution"][1],
					frameRateDepth 	 = self.config["rgbd_depth_freq"])

				self.imageDepthTimer = self.create_timer(1/self.config["rgbd_depth_freq"],
										self.rgbd_depth_callback)

			else:

				self.get_logger().warn("Unsupported publisher `{}` for qcar node.".format(publisher))

	def rgbd_color_callback(self):
		cameraInfo = self.imageColorPublisher

		# read IntelRealsense color information based on camera settings
		self.imageColor.read_RGB()

		# Conversion and publishing camera image infromation
		publishImage	= self.bridge.cv2_to_compressed_imgmsg(self.imageColor.imageBufferRGB,
															dst_format = "jpg")

		publishImage.header.stamp    =  self.get_clock().now().to_msg()
		publishImage.header.frame_id = 'RGBD_color_input'
		cameraInfo.publish(publishImage)

	def rgbd_depth_callback(self):
		cameraInfo = self.imageDepthPublisher

		# read IntelRealsense Depth information based on camera settings
		self.imageDepth.read_depth(dataMode='m')

		# Conversion and publishing camera image infromation
		publishImage	= self.bridge.cv2_to_imgmsg(self.imageDepth.imageBufferDepthM,
																	 "32FC1")

		publishImage.header.stamp 	 =  self.get_clock().now().to_msg()
		publishImage.header.frame_id = 'RGBD_depth_input'
		cameraInfo.publish(publishImage)

	def stop_rgbd(self):

		print("stopping Intel RealSense Nodes please wait...")

		# Checking if the stream is indeed open, close the ones that are open.
		for publisher in self.config['publishers']:

			if publisher.lower() == 'rgbd_color':
				self.imageColor.terminate()

			if publisher.lower() == 'rgbd_depth':
				self.imageDepth.terminate()
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Main

def main(args=None):
	rclpy.init(args=args)
	r = RGBDNode()
	while rclpy.ok():
		try:
			rclpy.spin_once(r)
		except KeyboardInterrupt:
			r.stop_rgbd()
			break

	r.destroy_node()
	rclpy.shutdown()
	print("Intel RealSense nodes have been stopped....")
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run

if __name__ == '__main__':
	main()
#endregion
