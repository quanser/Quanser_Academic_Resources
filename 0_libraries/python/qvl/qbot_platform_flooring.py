from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import numpy as np
import math
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsQBotPlatformFlooring(QLabsActor):
    """ This class is for spawning QBot Platform floor mats."""

    ID_FLOORING = 10091
    """Class ID"""

    FLOORING_QBOT_PLATFORM_0 = 0
    """See configurations"""
    FLOORING_QBOT_PLATFORM_1 = 1
    """See configurations"""
    FLOORING_QBOT_PLATFORM_2 = 2
    """See configurations"""
    FLOORING_QBOT_PLATFORM_3 = 3
    """See configurations"""
    FLOORING_QBOT_PLATFORM_4 = 4
    """See configurations"""
    FLOORING_QBOT_PLATFORM_5 = 5
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
       self.classID = self.ID_FLOORING
       return