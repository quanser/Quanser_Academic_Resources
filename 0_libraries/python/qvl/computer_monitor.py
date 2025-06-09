from qvl.actor import QLabsActor

class QLabsComputerMonitor(QLabsActor):
    """This class is for spawning computer keyboards."""

    ID_COMPUTER_MONITOR = 10130
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
       self.classID = self.ID_COMPUTER_MONITOR
       return

