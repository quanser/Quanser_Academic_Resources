from qvl.qlabs import CommModularContainer

import math
import struct

######################### MODULAR CONTAINER CLASS #########################

class QLabsSystem:
    """The System is a special class that allows you to modify elements of the user interface and application."""

    ID_SYSTEM = 1000
    """Class ID."""
    FCN_SYSTEM_SET_TITLE_STRING = 10
    FCN_SYSTEM_SET_TITLE_STRING_ACK = 11
    FCN_SYSTEM_EXIT_APP = 100
    FCN_SYSTEM_EXIT_APP_ACK = 101

    _qlabs = None
    _verbose = False

    def __init__(self, qlabs, verbose=False):
       """ Constructor method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       return

    def set_title_string(self, titleString, waitForConfirmation=True):
        """Sets the title string in the upper left of the window to custom text. This can be useful when doing screen recordings or labeling experiment configurations.

        :param titleString: User defined string to replace the default title text
        :param waitForConfirmation: (Optional) Wait for confirmation of the before proceeding. This makes the method a blocking operation.
        :type titleString: string
        :type waitForConfirmation: boolean
        :return: `True` if successful, `False` otherwise.
        :rtype: boolean
        """
        c = CommModularContainer()
        c.classID = self.ID_SYSTEM
        c.actorNumber = 0
        c.actorFunction = self.FCN_SYSTEM_SET_TITLE_STRING
        c.payload = bytearray(struct.pack(">I", len(titleString)))
        c.payload = c.payload + bytearray(titleString.encode('utf-8'))

        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_SYSTEM, 0, self.FCN_SYSTEM_SET_TITLE_STRING_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False
        
    def exit_application(self, delay, waitForConfirmation=True):
        """Requests QLabs to exit after the specified time delay.

        :param delay: Delay time before the application exits
        :param waitForConfirmation: (Optional) Wait for confirmation of the before proceeding. This makes the method a blocking operation.
        :type titleString: float
        :type waitForConfirmation: boolean
        :return: `True` if successful, `False` otherwise.
        :rtype: boolean
        """
        c = CommModularContainer()
        c.classID = self.ID_SYSTEM
        c.actorNumber = 0
        c.actorFunction = self.FCN_SYSTEM_EXIT_APP
        c.payload = bytearray(struct.pack(">f", delay))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_SYSTEM, 0, self.FCN_SYSTEM_EXIT_APP_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False        