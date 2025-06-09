from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import numpy as np
import math
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsQCarFlooring(QLabsActor):
    """ This class is for spawning qcar floor maps."""

    ID_FLOORING = 10090
    """Class ID"""

    FLOORING_QCAR_MAP_LARGE = 0
    FLOORING_QCAR_MAP_SMALL = 1


    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_FLOORING
       return