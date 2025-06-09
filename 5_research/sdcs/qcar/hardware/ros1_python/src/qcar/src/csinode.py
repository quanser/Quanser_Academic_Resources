#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports

import rospy
from pal.products.qcar import QCarCameras
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar CSI Node

class CSINode(object):
	def __init__(self):
		super().__init__()

		# Properties for image being streamed by all 4 cameras
		self.imageWidth = 640
		self.imageHeight = 480
		self.sampleRate = 30.0

		self.rightCamPublisher = rospy.Publisher('/qcar/csi_right',
												Image,
												queue_size=10)

		self.backCamPublisher = rospy.Publisher('/qcar/csi_back',
												Image,
												queue_size=10)

		self.leftCamPublisher = rospy.Publisher('/qcar/csi_left',
												Image,
												queue_size=10)

		self.frontCamPublisher = rospy.Publisher('/qcar/csi_front',
												Image,
												queue_size=10)

		self.bridge = CvBridge()
		self.qcarCameras = QCarCameras(frameWidth  = self.imageWidth,
                                    frameHeight = self.imageHeight,
                                    frameRate   = self.sampleRate,
                                    enableRight = True,
                                    enableBack  = True,
                                    enableLeft  = True,
                                    enableFront = True)

		while not rospy.is_shutdown():
			self.qcarCameras.readAll()

			self.process_cam_data(self.qcarCameras.csiRight,
									self.rightCamPublisher)
			self.process_cam_data(self.qcarCameras.csiBack,
									self.backCamPublisher)
			self.process_cam_data(self.qcarCameras.csiLeft,
									self.leftCamPublisher)
			self.process_cam_data(self.qcarCameras.csiFront,
									self.frontCamPublisher)

	def process_cam_data(self,cameraNumber, cameraInfo):

		# Extract the image from buffer
		streamImage = cameraNumber.imageData

		# COnfigure the image publisher
		imgPublisher = self.bridge.cv2_to_imgmsg(streamImage, "bgr8")
		imgPublisher.header.stamp =  rospy.Time.now()
		imgPublisher.header.frame_id = 'cam_img_input'
		cameraInfo.publish(imgPublisher)
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run

if __name__ == '__main__':
	rospy.init_node('csi_node')
	r = CSINode()

	rospy.spin()
	if KeyboardInterrupt:
		print("Stopping all cameras....")
#endregion
