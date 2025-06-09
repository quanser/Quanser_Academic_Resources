from qvl.actor import QLabsActor
import math
import struct

class QLabsRoundaboutSign(QLabsActor):
    """This class is for spawning roundabout signs."""

    ID_ROUNDABOUT_SIGN = 10060
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
       self.classID = self.ID_ROUNDABOUT_SIGN
       return

