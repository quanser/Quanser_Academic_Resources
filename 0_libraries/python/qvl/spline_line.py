from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import math
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsSplineLine(QLabsActor):


    ID_SPLINE_LINE = 180
    """Class ID"""

    FCN_SPLINE_LINE_SET_POINTS = 12
    FCN_SPLINE_LINE_SET_POINTS_ACK = 13

    LINEAR = 0
    """See configurations"""
    CURVE = 1
    """See configurations"""
    CONSTANT = 2
    """See configurations"""
    CLAMPED_CURVE = 3
    """See configurations"""


    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_SPLINE_LINE
       return

    def set_points(self, color, pointList, alignEndPointTangents=False, waitForConfirmation=True):
        """After spawning the origin of the spline actor, this method is used to create the individual points. At least 2 points must be specified to make a line.

        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param pointList: A 2D array with each row containing [x,y,z,width] elements. Width is in m.
        :param alignEndPointTangents: (Optional) Sets the tangent of the first and last point to be the same.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type color: float array[3]
        :type pointList: float 2D array[4][n]
        :type alignEndPointTangents: boolean
        :type waitForConfirmation: boolean
        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean
        """
        c = CommModularContainer()
        c.classID = self.ID_SPLINE_LINE
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_SPLINE_LINE_SET_POINTS
        c.payload = bytearray(struct.pack(">fffB", color[0], color[1], color[2], alignEndPointTangents))

        for point in pointList:
            c.payload = c.payload + bytearray(struct.pack(">ffff", point[0], point[1], point[2], point[3]))


        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_SPLINE_LINE, self.actorNumber, self.FCN_SPLINE_LINE_SET_POINTS_ACK)
                if c == None:
                    if (self._verbose):
                        print('spawn_id: Communication timeout (spline classID {}, actorNumber {}).'.format(self.classID, c.actorNumber))
                    return False

            return True
        else:
            if (self._verbose):
                print('spawn_id: Communication failed (spline classID {}, actorNumber {}).'.format(self.classID, c.actorNumber))
            return False

    def circle_from_center(self, radius, lineWidth=0.1, color=[1,0,0], numSplinePoints=8, waitForConfirmation=True):
        """After spawning the origin of the spline actor, this method is used to create a circle. Configuration 1 is recommended when spawning the line.

        :param radius: Radius in m
        :param lineWidth: Line width in m
        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param numSplinePoints: The number of points distributed around the circle. Splines will automatically round the edges, but more points will be needed for larger circles to achieve an accurate circle.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type radius: float
        :type lineWidth: float
        :type color: float array[3]
        :type numSplinePoints: integer
        :type waitForConfirmation: boolean
        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean
        """
        _waitForConfirmation = waitForConfirmation;
        points = []
        for angle in range(0, numSplinePoints):
            points.append([radius*math.sin(angle/numSplinePoints*math.pi*2), radius*math.cos(angle/numSplinePoints*math.pi*2), 0, lineWidth])

        points.append(points[0])

        return self.set_points(color, pointList=points, alignEndPointTangents=True, waitForConfirmation=_waitForConfirmation)

    def arc_from_center(self, radius, startAngle=0, endAngle=math.pi/2, lineWidth=1, color=[1,0,0], numSplinePoints=8, waitForConfirmation=True):

        """After spawning the origin of the spline actor, this method is used to create an arc. Configuration 1 is recommended when spawning the line.

        :param radius: Radius in m
        :param startAngle: Angle relative to the spawn orientation in radians
        :param endAngle: Angle relative to the spawn orientation in radians
        :param lineWidth: Line width in m
        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param numSplinePoints: The number of points distributed around the circle. Splines will automatically round the edges, but more points will be needed for larger circles to achieve an accurate circle.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type radius: float
        :type startAngle: float
        :type endAngle: float
        :type lineWidth: float
        :type color: float array[3]
        :type numSplinePoints: integer
        :type waitForConfirmation: boolean
        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean
        """

        points = []

        for angle in range(0, numSplinePoints+1):
            points.append([radius*math.cos(angle/numSplinePoints*(endAngle-startAngle)+startAngle), radius*math.sin(angle/numSplinePoints*(endAngle-startAngle)+startAngle), 0, lineWidth])

        return self.set_points(color, pointList=points, alignEndPointTangents=False)

    def arc_from_center_degrees(self, radius, startAngle=0, endAngle=90, lineWidth=1, color=[1,0,0], numSplinePoints=4, waitForConfirmation=True):
        """After spawning the origin of the spline actor, this method is used to create an arc. Configuration 1 is recommended when spawning the line.

        :param radius: Radius in m
        :param startAngle: Angle relative to the spawn orientation in degrees
        :param endAngle: Angle relative to the spawn orientation in degrees
        :param lineWidth: Line width in m
        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param numSplinePoints: The number of points distributed around the circle. Splines will automatically round the edges, but more points will be needed for larger circles to achieve an accurate circle.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type radius: float
        :type startAngle: float
        :type endAngle: float
        :type lineWidth: float
        :type color: float array[3]
        :type numSplinePoints: integer
        :type waitForConfirmation: boolean
        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean
        """

        return  self.arc_from_center(radius, startAngle/180*math.pi, endAngle/180*math.pi, lineWidth, color, numSplinePoints, waitForConfirmation)

    def rounded_rectangle_from_center(self, cornerRadius, xWidth, yLength, lineWidth=0.1, color=[1,0,0], waitForConfirmation=True):

        """After spawning the origin of the spline actor, this method is used to create a rounded rectangle. Configuration 1 is recommended when spawning the line.

        :param cornerRadius: Corner radius in m
        :param xWidth: Dimension in m of the rectangle in the local x axis
        :param yLength: Dimension in m of the rectangle in the local y axis
        :param lineWidth: Line width in m
        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type cornerRadius: float
        :type xWidth: float
        :type yLength: float
        :type lineWidth: float
        :type color: float array[3]
        :type numSplinePoints: integer
        :type waitForConfirmation: boolean
        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean
        """

        points = self._spawn_spline_rounded_rectangle_from_center_point_list(cornerRadius, xWidth, yLength, lineWidth)

        return self.set_points(color, pointList=points, alignEndPointTangents=True)

    def _spawn_spline_rounded_rectangle_from_center_point_list(self, cornerRadius, xWidth, yLength, lineWidth=1):
        if (xWidth <= cornerRadius*2):
            xWidth = cornerRadius*2

        if (yLength <= cornerRadius*2):
            yLength = cornerRadius*2

        circleSegmentLength = math.pi*cornerRadius*2/8

        xCount = math.ceil((xWidth - 2*cornerRadius)/circleSegmentLength)
        yCount = math.ceil((yLength - 2*cornerRadius)/circleSegmentLength)

        # Y
        # ▲
        # │
        # ┼───► X
        #
        #   4───────3
        #   │       │
        #   │   ┼   │
        #   │       │
        #   1───────2

        offset225deg = cornerRadius-cornerRadius*math.sin(math.pi/8)
        offset45deg = cornerRadius-cornerRadius*math.sin(math.pi/8*2)
        offset675deg = cornerRadius-cornerRadius*math.sin(math.pi/8*3)

        # corner 1
        points = []
        points.append([-xWidth/2, -yLength/2+cornerRadius, 0, lineWidth])
        points.append([-xWidth/2+offset675deg, -yLength/2+offset225deg, 0, lineWidth])
        points.append([-xWidth/2+offset45deg, -yLength/2+offset45deg, 0, lineWidth])
        points.append([-xWidth/2+offset225deg, -yLength/2+offset675deg, 0, lineWidth])
        points.append([-xWidth/2+cornerRadius,-yLength/2, 0, lineWidth])

        # x1
        if (xWidth > cornerRadius*2):
            sideSegmentLength = (xWidth - 2*cornerRadius)/xCount

            for sideCount in range(1,xCount):
                 points.append([-xWidth/2+cornerRadius + sideCount*sideSegmentLength,-yLength/2, 0, lineWidth])

            points.append([xWidth/2-cornerRadius,-yLength/2, 0, lineWidth])

        # corner 2
        points.append([xWidth/2-offset225deg, -yLength/2+offset675deg, 0, lineWidth])
        points.append([xWidth/2-offset45deg, -yLength/2+offset45deg, 0, lineWidth])
        points.append([xWidth/2-offset675deg, -yLength/2+offset225deg, 0, lineWidth])
        points.append([xWidth/2, -yLength/2+cornerRadius, 0, lineWidth])

        # y1
        if (yLength > cornerRadius*2):
            sideSegmentLength = (yLength - 2*cornerRadius)/yCount

            for sideCount in range(1,yCount):
                points.append([xWidth/2, -yLength/2+cornerRadius  + sideCount*sideSegmentLength, 0, lineWidth])

            points.append([xWidth/2, yLength/2-cornerRadius, 0, lineWidth])

        # corner 3
        points.append([xWidth/2-offset675deg, yLength/2-offset225deg, 0, lineWidth])
        points.append([xWidth/2-offset45deg, yLength/2-offset45deg, 0, lineWidth])
        points.append([xWidth/2-offset225deg, yLength/2-offset675deg, 0, lineWidth])
        points.append([xWidth/2-cornerRadius, yLength/2, 0, lineWidth])

        # x2
        if (xWidth > cornerRadius*2):
            sideSegmentLength = (xWidth - 2*cornerRadius)/xCount

            for sideCount in range(1,xCount):
                points.append([xWidth/2-cornerRadius - sideCount*sideSegmentLength, yLength/2, 0, lineWidth])

            points.append([-xWidth/2+cornerRadius, yLength/2, 0, lineWidth])

        # corner 4
        points.append([-xWidth/2+offset225deg, yLength/2-offset675deg, 0, lineWidth])
        points.append([-xWidth/2+offset45deg, yLength/2-offset45deg, 0, lineWidth])
        points.append([-xWidth/2+offset675deg, yLength/2-offset225deg, 0, lineWidth])
        points.append([-xWidth/2, yLength/2-cornerRadius, 0, lineWidth])

        # y2
        if (yLength > cornerRadius*2):
            sideSegmentLength = (yLength - 2*cornerRadius)/yCount

            for sideCount in range(1,yCount):
                points.append([-xWidth/2, yLength/2-cornerRadius - sideCount*sideSegmentLength, 0, lineWidth])

            points.append(points[0])

        return points