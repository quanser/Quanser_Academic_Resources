from qvl.actor import QLabsActor
import math
import struct

class QLabsStopSign(QLabsActor):
    """This class is for spawning stop signs."""

    ID_STOP_SIGN = 10020
    """Class ID"""

    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_STOP_SIGN
       return

