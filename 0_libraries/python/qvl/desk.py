from qvl.actor import QLabsActor

class QLabsDesk(QLabsActor):
    """This class is for spawning desks."""

    ID_DESK = 10100
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
       self.classID = self.ID_DESK
       return

