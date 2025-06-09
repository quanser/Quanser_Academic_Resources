#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

import rospy
from pal.products.qcar import QCarRealSense
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar RealSense Node

class RGBDNode(object):
	def __init__(self):
		super().__init__()

		# RGB camera parameters
		imageWidthRGB  = 1280
		imageHeightRGB = 720
		camRateRGB 	   = 60

		# Depth camera parameters
		imageWidthDepth = 640
		imageHeightDept = 480
		camRateDepth 	= 60

		# Initialize ros publishers
		self.imageColorPublisher = rospy.Publisher('/qcar/rgbd_color',
													Image,
													queue_size=10)

		self.imageDepthPublisher = rospy.Publisher('/qcar/rgbd_depth',
													Image,
													queue_size=10)

		self.bridge = CvBridge()

		#Initialize CV sensors
		self.rgbd = QCarRealSense(mode='RGB&DEPTH',
						frameWidthRGB    = imageWidthRGB,
						frameHeightRGB   = imageHeightRGB,
						frameRateRGB	 = camRateRGB,
						frameWidthDepth  = imageWidthDepth,
						frameHeightDepth = imageHeightDept,
						frameRateDepth   = camRateDepth)

		#Get readings
		while not rospy.is_shutdown():
			self.rgbd.read_RGB()
			self.rgbd.read_depth(dataMode='M')

			# self.rate_pub.publish(msg)
			self.process_color_data(self.imageColorPublisher,
									self.rgbd.imageBufferRGB)

			self.process_depth_data(self.imageDepthPublisher,
									self.rgbd.imageBufferDepthM)

	def process_color_data(self, camInfo, imgData):

		pub_img = self.bridge.cv2_to_imgmsg(imgData, "bgr8")
		pub_img.header.stamp =  rospy.Time.now()
		pub_img.header.frame_id = 'RGBD_color_input'
		camInfo.publish(pub_img)

	def process_depth_data(self, camInfo, imgData):

		pub_img = self.bridge.cv2_to_imgmsg(imgData, "32FC1")
		pub_img.header.stamp =  rospy.Time.now()
		pub_img.header.frame_id = 'RGBD_depth_input'
		camInfo.publish(pub_img)

	def terminate_camera(self):
			self.rgbd.terminate()
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run
if __name__ == '__main__':
	rospy.init_node('rgbd_node')
	r = RGBDNode()

	rospy.spin()
	if KeyboardInterrupt:
			r.terminate_camera()
			print("Stopping rgbd camera....")
#endregion
