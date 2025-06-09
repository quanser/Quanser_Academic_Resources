from qvl.qlabs import QuanserInteractiveLabs, CommModularContainer
from quanser.common import GenericError
from qvl.actor import QLabsActor
import math

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsShredder(QLabsActor):


    ID_SHREDDER = 190

    RED = 0
    GREEN = 1
    BLUE = 2
    WHITE = 3

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
        self.classID = self.ID_SHREDDER
        return
