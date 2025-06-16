#! /usr/bin/env python3

# Generic python packages
import time  # Time library
import numpy as np
import cv2

# ROS specific packages
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from rcl_interfaces.msg import SetParametersResult
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

'''
Secondary node to determine road signs and traffic lights based on classic
object and color detection techniques.
'''

class ObjectDetector(Node):

    def __init__(self):
      super().__init__('traffic_system_detector')


      self.camera_image_subscriber = self.create_subscription(Image ,'/camera/color_image',self.image_callback, 10)

      self.motion_publisher = self.create_publisher(Bool,'motion_enable',10)
      self.motion_enable = True
      self.detection_cooldown = 10.0
      self.disable_until = 0.0
      self.light_detected = False

      self.publish_motion_flag(True)
      self.t0 = time.time()

      self.bridge = CvBridge()
      self.sign_detected = False

    def image_callback(self,msg):
      current_time = time.time()-self.t0
      delay = 0
      sign_delay = 0
      light_delay = 0
      light_detected = False
      sign_detected = False
      cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')


      try:
        height, width, channel = cv_image.shape
        # Convert from BGR to HSV
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        if not self.sign_detected and not self.light_detected:
            # send image to the sign detector to check for a sign in the scene and return
            # a delay based on what's seen
            sign_delay, sign_detected = self.sign_detector(hsv=hsv)
            if sign_detected == False:
              light_delay, self.light_detected = self.Light_detector(hsv=hsv)

            elif not self.light_detected:
              if sign_detected:
                delay = sign_delay


            if delay > 0.0 and not self.sign_detected:
              self.sign_detected = True
              self.disable_until= delay
              self.publish_motion_flag(False)
            else:
              self.publish_motion_flag(True)



        if self.sign_detected and not self.light_detected:

          if current_time >= self.disable_until:
            if current_time >= self.detection_cooldown:
              self.sign_detected = False
            self.publish_motion_flag(True)


        if self.light_detected:
            # This forces just the traffic light check to work and request information
            self.publish_motion_flag(False)
            light_delay, self.light_detected = self.Light_detector(hsv=hsv)
            if self.light_detected == False:
              self.sign_detected = False

      except AttributeError:
          self.get_logger().info("No image received")


    def publish_motion_flag(self, enable:bool):
       msg = Bool()
       msg.data = enable
       self.motion_publisher.publish(msg)

    def sign_detector(self, hsv):
        detected = False
        delay = 0.0
        height, width, _ =  hsv.shape

        roi = hsv[:, int(3*width/4)::]

        # Define the red color range in HSV
        lower_red1 = np.array([0,120,70])
        upper_red1 = np.array([10,255,255])
        lower_red2 = np.array([170,120,70])
        upper_red2 = np.array([180,255,255])

        mask1 = cv2.inRange(roi,lower_red1,upper_red1)
        mask2 = cv2.inRange(roi,lower_red2,upper_red2)
        mask = mask1 | mask2

        mask = cv2.morphologyEx(mask,cv2.MORPH_OPEN, np.ones((3,3), np.uint8))

        #find countours
        contours,_ = cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
          area = cv2.contourArea(cnt)
          if area < 1000:
            continue

          #approximate shape
          epsilon = 0.04*cv2.arcLength(cnt,True)
          approx = cv2.approxPolyDP(cnt,epsilon,True)
          sides = len(approx)


          if sides == 3:
            print("Yield! Pausing for 1.5s...")
            delay = 1.5
            self.t0 = time.time()
            detected = True
            self.detection_cooldown =10.0
          elif 7<=sides<=9:
            print("Stop!  Pausing for 3.0s...")
            delay = 3.0
            self.t0 = time.time()
            detected = True
            self.detection_cooldown =10.0
        cv2.imshow("Sign Detection Mask",mask)
        cv2.waitKey(1)
        return delay, detected

    def Light_detector(self,hsv):
      height, width, _ =  hsv.shape
      offset = int(20)
      # roi = hsv[offset:offset+int(height/3), int(width/3):2*int(2*width/3)]
      roi = hsv[offset:offset+int(height/3)-offset, int(width/3)-offset*2:int(2*width/3)-offset*3]

      detected = False
      delay = 0

      # Color thresholds
      lower_red1 = np.array([0,200,200])
      upper_red1 = np.array([10,255,255])
      lower_red2 = np.array([245,150,150])
      upper_red2 = np.array([255,255,255])

      lower_yellow = np.array([20,100,100])
      upper_yellow = np.array([30,255,255])

      lower_green = np.array([40,100,100])
      upper_green = np.array([90,255,255])

      # Apply masks
      mask1 = cv2.inRange(roi,lower_red1,upper_red1)
      mask2 = cv2.inRange(roi,lower_yellow,upper_yellow)
      mask3 = cv2.inRange(roi,lower_green,upper_green)


      # Count pixels
      red_pxl_cnt = cv2.countNonZero(mask1) >= 5
      yellow_pxl_cnt = cv2.countNonZero(mask2) > 200
      green_pxl_cnt = cv2.countNonZero(mask3) > 30
      # Pixel Count mind

      if red_pxl_cnt  and (not green_pxl_cnt):
        delay = 0.01
        self.t0 = time.time()
        self.detection_cooldown =0.01

        print("Red light detected waiting to be allowed to move...")
        detected = True

      elif not red_pxl_cnt  and green_pxl_cnt:
        print("green Light detected... Good to keep moving")
        detected = False

      cv2.imshow("TF Detector Mask",mask1)
      cv2.waitKey(1)
      return delay, detected




def main():

  # Start the ROS 2 Python Client Library
  rclpy.init()

  node = ObjectDetector()
  try:
      rclpy.spin(node)
  except KeyboardInterrupt:
      pass

  rclpy.shutdown()
  cv2.destroyAllWindows()

if __name__ == '__main__':
  main()