import cv2
import math
import numpy as np


class VisualizeIMU():
    '''Visualization class for IMU data (accelerometer & gyroscope)'''

    def __init__(self):
        self.img = np.zeros((480, 800), dtype=np.uint8)

    def visualize_acceleration(self, acceleration):
        # reset image and define center
        self.img = np.zeros((480, 800), dtype=np.uint8)
        centerCol, centerRow = 400, 240

        # move the point left/right or up/down based on Y and Z accel components
        point = (np.clip(centerCol - math.floor(30*acceleration[1]), 146, 654),
                 np.clip(centerRow - math.floor(20*(acceleration[2]-10)), 10, 390))

        # grow the object's size or shrink it based on the X accel component
        radius = np.clip(75 + math.floor(20*acceleration[0]/2), 5, 145)

        # draw the square marker
        cv2.drawMarker(self.img, point, 125, cv2.MARKER_SQUARE, radius, 5) # Square Marker

    def visualize_orientation(self, acceleration):
        # reset the image and define center
        self.img = np.zeros((480, 800), dtype=np.uint8)
        radius, centerCol, centerRow = 200, 400, 240

        # find the Y-Z plane rotation angle based on accel data
        theta = math.atan2(-acceleration[1], acceleration[2])

        # find the corner points of the line based on the rotation angle
        ptA = ( math.floor( radius*math.cos(theta) ) + centerCol, \
                math.floor( radius*math.sin(theta) ) + centerRow )
        ptB = ( math.floor( radius*math.cos(theta + math.pi) ) + centerCol, \
                math.floor( radius*math.sin(theta + math.pi) ) + centerRow )

        # draw the line-segment
        cv2.line(self.img, ptA, ptB, 125, 5)

        # find up/down triangle markers based on the Y-Z rotation angle
        if theta >= 0:
             markerA = cv2.MARKER_TRIANGLE_DOWN
             markerB = cv2.MARKER_TRIANGLE_UP
        else:
             markerB = cv2.MARKER_TRIANGLE_DOWN
             markerA = cv2.MARKER_TRIANGLE_UP

        # draw the markers at the line-tips
        cv2.drawMarker(self.img, ptA, 125, markerA,50,25)
        cv2.drawMarker(self.img, ptB, 125, markerB,50,25)

    def visualize_rotations(self, rates, enable):
        # reset the image and define the center as well as square-semi-sidelength
        self.img = np.zeros((480, 800), dtype=np.uint8)

        # define new center location based on gyro Y and Z component magnitudes
        center  = (400, 240)
        # calculate an appropriate rotation angle based on the gyro X rotation

        if enable[1]:
            theta       = 0
            semiSideX   = 100 - np.clip(abs(10*rates[2]), 0, 90)
            semiSideY   = 100
        elif enable[0]:
            theta       = 0
            semiSideY   = 100 - np.clip(abs(10*rates[1]), 0, 90)
            semiSideX   = 100
        else:
            theta       = (np.pi) * rates[0]/14
            semiSideX   = 100
            semiSideY   = 100

        # rotate the 4 corners of a square based on gyro X rotation angle
        points = (
                  (
                   center[0]+math.floor(semiSideX*np.cos(theta)            + semiSideY*np.sin(theta)            ),
                   center[1]+math.floor(semiSideY*np.cos(theta)            - semiSideX*np.sin(theta)            )
                  ),
                  (
                   center[0]+math.floor(semiSideY*np.cos(theta+(np.pi/2))  + semiSideX*np.sin(theta+(np.pi/2))  ),
                   center[1]+math.floor(semiSideX*np.cos(theta+(np.pi/2))  - semiSideY*np.sin(theta+(np.pi/2))  )
                  ),
                  (
                   center[0]+math.floor(semiSideX*np.cos(theta+(np.pi))    + semiSideY*np.sin(theta+(np.pi))    ),
                   center[1]+math.floor(semiSideY*np.cos(theta+(np.pi))    - semiSideX*np.sin(theta+(np.pi))    )
                  ),
                  (center[0]+math.floor(semiSideY*np.cos(theta+(3*np.pi/2))+ semiSideX*np.sin(theta+(3*np.pi/2))),
                   center[1]+math.floor(semiSideX*np.cos(theta+(3*np.pi/2))- semiSideY*np.sin(theta+(3*np.pi/2)))
                   )
                  )

        # connect the 4 corners with a line
        cv2.line(self.img,points[0], points[1],125, 5)
        cv2.line(self.img,points[1], points[2],125, 5)
        cv2.line(self.img,points[2], points[3],125, 5)
        cv2.line(self.img,points[3], points[0],125, 5)