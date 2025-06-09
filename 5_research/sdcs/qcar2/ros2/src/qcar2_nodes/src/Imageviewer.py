#!/usr/bin/env python3
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSReliabilityPolicy
from rclpy.qos import QoSHistoryPolicy, QoSDurabilityPolicy
import numpy as np
import cv2
import time


from sensor_msgs.msg import Image,CompressedImage
from cv_bridge import CvBridge
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : QCar ImageViewer Node

class ImageSubscriber(Node):
    def __init__(self, topicName,imageType):
        super().__init__('image_subscriber',
        allow_undeclared_parameters=True,
		automatically_declare_parameters_from_overrides=True
	)

        # test out making custom QoS profile:
        self.qcar_qos_profile = QoSProfile(
                reliability   = QoSReliabilityPolicy.BEST_EFFORT,
                history 	  = QoSHistoryPolicy.KEEP_LAST,
                durability    = QoSDurabilityPolicy.VOLATILE,
                depth 		  = 10)

        print("Subscribing to: {}".format(topicName))

        # start counter for time delta
        self.startTime = time.perf_counter()
        self.bridge    = CvBridge()

        if imageType == "CompressedImage":
            self.subscription = self.create_subscription(CompressedImage,
                                                        str(topicName),
                                                        self.Compressed_Image_callback,
                                                        self.qcar_qos_profile)
        elif imageType == "Image":
            self.subscription = self.create_subscription(Image,
                                                        str(topicName),
                                                        self.Image_callback,
                                                        self.qcar_qos_profile)
        else:
            print("Incorrect topic type!")


    def Compressed_Image_callback(self,data):

        # Convert compressed image msg to cv2 format
        currentImage = self.bridge.compressed_imgmsg_to_cv2(data)

        #Display image using cv2
        self.Image_display(currentImage)


    def Image_callback(self, data):

        # Convert image msg to cv2 format
        currentImage  = self.bridge.imgmsg_to_cv2(data)

        #Display image using cv2
        self.Image_display(currentImage)


    def Image_display(self, currentFrame):

        time2 = time.perf_counter()

        # time from start of script or previous call
        timeDelta       = time2 - self.startTime
        framesPerSecond = str(1/timeDelta)


        # Image information:
        imageInfo = str(np.shape(currentFrame))

        # text settings for open cv
        fpsCoordinate = (50,50)
        font          = cv2.FONT_HERSHEY_PLAIN
        fontScale     = 1
        color         = (255,0,0)
        thickness     = 2

        text  = framesPerSecond + str(" ")+ imageInfo
        image = cv2.putText(currentFrame, text , fpsCoordinate, font, fontScale, color, thickness, cv2.LINE_AA )

        cv2.imshow("Camera Video Stream", image)
        cv2.waitKey(1)
        self.startTime = time2

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Main

def main(args=None):
    rclpy.init(args=args)


    # prompt the user which camera topic they would like to view:
    topic_name = input("Please input the name of the image node you will like to subscribe to (example: /qcar/csi_left): ")
    print("Please input image message type.\nFor compressed image topic use: CompressedImage , for regular Image topic use: Image")
    Image_type = input ("Image message type: ")
    image_subscriber = ImageSubscriber(topic_name, Image_type)


    while rclpy.ok():
        try:
            rclpy.spin_once(image_subscriber)
        except KeyboardInterrupt:
            print("\nDone")
            break
    image_subscriber.destroy_node()
    rclpy.shutdown()
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run

if __name__ == '__main__':
    main()
#endregion
