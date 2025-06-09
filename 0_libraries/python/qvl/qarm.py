from qvl.qlabs import QuanserInteractiveLabs, CommModularContainer
from quanser.common import GenericError
from qvl.actor import QLabsActor
import math

import sys
import struct
import os

sys.path.append('../Common/')

######################### MODULAR CONTAINER CLASS #########################

class QLabsQArm(QLabsActor):

    ID_QARM = 10

    # Initialize class
    def __init__(self, qlabs, verbose=False):
        """ Constructor Method

        :param qlabs: A QuanserInteractiveLabs object
        :param verbose: (Optional) Print error information to the console.
        :type qlabs: object
        :type verbose: boolean
        """

        self._qlabs = qlabs
        self._verbose = verbose
        self.classID = self.ID_QARM
        return

