import numpy as np
from hal.utilities.path_planning import RoadMap

class SDCSRoadMap(RoadMap):
    """A RoadMap implementation for Quanser's Self-Driving Car studio (SDCS)"""

    def __init__(self, leftHandTraffic=False, useSmallMap=False):
        """Initialize a new SDCSRoadMap instance.

        Args:
            leftHandTraffic (bool): If true, assumes cars drive on the left.
                Defaults to False.
            useSmallMap (bool): If true, will use the smaller map variant.
                Defaults to False.
        """
        super().__init__()

        # useful constants
        scale = 0.002035
        xOffset = 1134
        yOffset = 2363

        innerLaneRadius = 305.5 * scale
        outerLaneRadius = 438 * scale
        trafficCircleRadius = 333 * scale
        oneWayStreetRadius = 350 * scale
        kinkStreetRadius = 375 * scale

        pi = np.pi
        halfPi = pi/2

        def scale_then_add_nodes(nodePoses):
            for pose in nodePoses:
                pose[0] = scale * (pose[0] - xOffset)
                pose[1] = scale * (yOffset - pose[1])
                self.add_node(pose)

        if leftHandTraffic:
            nodePoses = [
                [1134, 2427, halfPi],
                [1134, 2323, halfPi],
                [1266, 2323, -halfPi],
                [1688, 2896, pi],
                [1688, 2763, 0],
                [2242, 2323, -halfPi],
                [2109, 2323, halfPi],
                [1741, 1822, 0],
                [1634, 1955, pi],
                [766, 1822, 0],
                [766, 1955, pi],
                [504, 2589, 138*pi/180],
            ]
            if not useSmallMap:
                nodePoses += [
                    [1134, 1428, halfPi],
                    [1266, 1454, -halfPi],
                    [2242, 1454, -halfPi],
                    [2109, 1200, halfPi],
                    [1854.5, 814.5, 170.6*pi/180],
                    [1580, 540, 99.4*pi/180],
                    [1440, 856, 42*pi/180],
                    [1523, 958, -138*pi/180],
                    [1400, 153, 0],
                    [1134, 286, pi],
                    [159, 905, halfPi],
                    [291, 905, -halfPi],
                ]

            edgeConfigs = [
                [0, 1, 0],
                [1, 7, outerLaneRadius],
                [1, 10, innerLaneRadius],
                [2, 4, innerLaneRadius],
                [2, 11, innerLaneRadius],
                [3, 0, outerLaneRadius],
                [3, 11, outerLaneRadius],
                [4, 6, innerLaneRadius],
                [5, 3, outerLaneRadius],
                [6, 8, innerLaneRadius],
                [7, 5, outerLaneRadius],
                [8, 2, innerLaneRadius],
                [8, 10, 0],
                [9, 2, outerLaneRadius],
                [9, 7, 0],
                [10, 1, innerLaneRadius],
                [11, 9, oneWayStreetRadius],
            ]
            if not useSmallMap:
                edgeConfigs += [
                    [1, 12, 0],
                    [6, 15, 0],
                    [7, 15, innerLaneRadius],
                    [8, 12, outerLaneRadius],
                    [9, 12, innerLaneRadius],
                    [10, 22, outerLaneRadius],
                    [11, 22, outerLaneRadius],
                    [12, 18, outerLaneRadius],
                    [13, 2, 0],
                    [13, 7, innerLaneRadius],
                    [13, 10, outerLaneRadius],
                    [14, 5, 0],
                    [14, 8, outerLaneRadius],
                    [15, 16, innerLaneRadius],
                    [16, 17, trafficCircleRadius],
                    [16, 19, innerLaneRadius],
                    [17, 14, trafficCircleRadius],
                    [17, 16, trafficCircleRadius],
                    [17, 21, innerLaneRadius],
                    [18, 17, innerLaneRadius],
                    [19, 13, innerLaneRadius],
                    [20, 14, trafficCircleRadius],
                    [20, 16, trafficCircleRadius],
                    [21, 23, innerLaneRadius],
                    [22, 20, outerLaneRadius],
                    [23, 9, innerLaneRadius],
                ]
        else: # Right-side Traffic
            nodePoses = [
                [1134, 2299, -halfPi],
                [1266, 2323, halfPi],
                [1688, 2896, 0],
                [1688, 2763, pi],
                [2242, 2323, halfPi],
                [2109, 2323, -halfPi],
                [1632, 1822, pi],
                [1741, 1955, 0],
                [766, 1822, pi],
                [766, 1955, 0],
                [504, 2589, -42*pi/180],
            ]
            if not useSmallMap:
                nodePoses += [
                    [1134, 1300, -halfPi],
                    [1134, 1454, -halfPi],
                    [1266, 1454, halfPi],
                    [2242, 905, halfPi],
                    [2109, 1454,-halfPi],
                    [1580, 540, -80.6*pi/180],
                    [1854.4, 814.5, -9.4*pi/180],
                    [1440, 856, -138*pi/180],
                    [1523, 958, 42*pi/180],
                    [1134, 153, pi],
                    [1134, 286, 0],
                    [159, 905, -halfPi],
                    [291, 905, halfPi],
                ]

            edgeConfigs = [
                [0, 2, outerLaneRadius],
                [1, 7, innerLaneRadius],
                [1, 8, outerLaneRadius],
                [2, 4, outerLaneRadius],
                [3, 1, innerLaneRadius],
                [4, 6, outerLaneRadius],
                [5, 3, innerLaneRadius],
                [6, 0, outerLaneRadius],
                [6, 8, 0],
                [7, 5, innerLaneRadius],
                [8, 10, oneWayStreetRadius],
                [9, 0, innerLaneRadius],
                [9, 7, 0],
                [10, 1, innerLaneRadius],
                [10, 2, innerLaneRadius],
            ]
            if not useSmallMap:
                edgeConfigs += [
                    [1, 13, 0],
                    [4, 14, 0],
                    [6, 13, innerLaneRadius],
                    [7, 14, outerLaneRadius],
                    [8, 23, innerLaneRadius],
                    [9, 13, outerLaneRadius],
                    [11, 12, 0],
                    [12, 0, 0],
                    [12, 7, outerLaneRadius],
                    [12, 8, innerLaneRadius],
                    [13, 19, innerLaneRadius],
                    [14, 16, trafficCircleRadius],
                    [14, 20, trafficCircleRadius],
                    [15, 5, outerLaneRadius],
                    [15, 6, innerLaneRadius],
                    [16, 17, trafficCircleRadius],
                    [16, 18, innerLaneRadius],
                    [17, 15, innerLaneRadius],
                    [17, 16, trafficCircleRadius],
                    [17, 20, trafficCircleRadius],
                    [18, 11, kinkStreetRadius],
                    [19, 17, innerLaneRadius],
                    [20, 22, outerLaneRadius],
                    [21, 16, innerLaneRadius],
                    [22, 9, outerLaneRadius],
                    [22, 10, outerLaneRadius],
                    [23, 21, innerLaneRadius],
                ]

        scale_then_add_nodes(nodePoses)
        for edgeConfig in edgeConfigs:
            self.add_edge(*edgeConfig)