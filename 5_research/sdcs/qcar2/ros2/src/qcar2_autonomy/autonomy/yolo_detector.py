#! /usr/bin/env python3

# Quanser specific packages
from pit.YOLO.nets import YOLOv8
from pit.YOLO.utils import QCar2DepthAligned


# Generic python packages
import time  # Time library
import numpy as np
import cv2

# ROS specific packages
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

'''
Description:

Node for detecting traffic light state and signs on the road. Provides flags
which define if a traffic signal has been detected and what action to take.
'''

class ObjectDetector(Node):

    def __init__(self):
        super().__init__('yolo_detector')
        # Additional parameters
        imageWidth  = 640
        imageHeight = 480
        self.QCarImg = QCar2DepthAligned()
        self.myYolo  = YOLOv8(
                    # modelPath = 'path/to/model',
                    imageHeight= imageHeight,
                    imageWidth = imageWidth,
                )
        # Call on_timer function every second to receive pose info
        self.dt = 1/30
        self.timer = self.create_timer(self.dt, self.on_timer)

        self.motion_publisher = self.create_publisher(Bool,'/motion_enable',1)
        self.motion_enable = True
        self.detection_cooldown = 10.0
        self.disable_until = 0.0
        self.flag_value = False
        self.publish_motion_flag(True)
        self.t0 = time.time()

        self.sign_detected = False

        # publish image aligned information
        self.bridge = CvBridge()
        self.publish_rgb = self.create_publisher(Image,'/qcar_camera/rgb',10)
        self.publish_depth = self.create_publisher(Image,'/qcar_camera/depth',10)

        self.timer2 = self.create_timer(1/500, self.flag_publisher)

    def flag_publisher(self):
       self.publish_motion_flag(self.flag_value)

    def on_timer(self):
        # Get aligned RGB and Depth images and publish them
        self.QCarImg.read()
        msg_rgb = self.bridge.cv2_to_imgmsg(self.QCarImg.rgb, "bgr8")
        msg_depth = self.bridge.cv2_to_imgmsg(self.QCarImg.depth, "32FC1")
        self.publish_rgb.publish(msg_rgb)
        self.publish_depth.publish(msg_depth)

        current_time = time.time()-self.t0
        delay = 0
        sign_delay = 0
        sign_detected = False
        if not self.sign_detected:
            # send image to the sign detector to check for a sign in the scene and return
            # a delay based on what's seen
            sign_delay, sign_detected = self.yolo_detect()

            if sign_detected:
                delay = sign_delay


            if delay > 0.0 and not self.sign_detected:
              self.sign_detected = True
              self.disable_until= delay
              self.flag_value = False
            else:
              self.flag_value = True


        elif self.sign_detected:

          if current_time >= self.disable_until:
            if current_time >= self.detection_cooldown:
              self.sign_detected = False
            self.flag_value = True


    def yolo_detect(self):
        detected = False
        delay = 0.0

        rgbProcessed = self.myYolo.pre_process(self.QCarImg.rgb)
        predecion = self.myYolo.predict(inputImg = rgbProcessed,
                                    classes = [2,9,11,33],
                                    confidence = 0.3,
                                    half = True,
                                    verbose = False
                                    )

        processedResults=self.myYolo.post_processing(alignedDepth = self.QCarImg.depth,
                                                clippingDistance = 5)
        labelName = []
        labelConf = []
        for object in processedResults:
            # print(object.__dict__)

            labelName = object.__dict__["name"]
            labelConf = object.__dict__["conf"]
            objectDist = object.__dict__["distance"]

            if labelName == 'car' and labelConf > 0.9 and objectDist < 0.45 :
                self.get_logger().info("Car found!")

            elif labelName == "stop sign" and labelConf > 0.9 and objectDist < 0.52:
            # elif labelName == "stop sign" and labelConf > 0.9:

                self.get_logger().info("Stop Sign Detected!")
                delay = 3.0
                self.t0 = time.time()
                detected = True
                self.detection_cooldown =10.0

            elif labelName == "yield sign" and labelConf > 0.9 and objectDist < 0.52:
            # elif labelName == "yield sign" and labelConf > 0.9:
                self.get_logger().info("Yield Sign Detected!")
                delay = 1.5
                self.t0 = time.time()
                detected = True
                self.detection_cooldown =10.0
            # print(object.__dict__)
        print("===============================")
        return delay, detected

    def publish_motion_flag(self, enable:bool):
       msg = Bool()
       msg.data = enable
       self.motion_publisher.publish(msg)

    def terminate(self):
       self.QCarImg.terminate()


def main():

  # Start the ROS 2 Python Client Library
  rclpy.init()

  node = ObjectDetector()
  try:
      rclpy.spin(node)
  except KeyboardInterrupt:
      node.terminate()
      pass

  rclpy.shutdown()

if __name__ == '__main__':
  main()