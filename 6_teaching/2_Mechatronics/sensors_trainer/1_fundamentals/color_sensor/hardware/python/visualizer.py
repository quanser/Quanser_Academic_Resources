import cv2

class ColorDisplay:
    """ An classical object detection algorithm with different options of detection
        methods, as well as visualization tools.

    """

    def __init__(self,name="Solid Color"):
        ''' Initializes the object detection class.
        '''
        self.name = name


    def set_tracker(self):
        """Set trackers in CV2 window to assist in color thresholding.

        Args:
            mode (ndarray): Input image type, 'rgb' or 'hsv'.

        """

        cv2.namedWindow(self.name)

        cv2.createTrackbar('R', self.name, 0, 255,self._nothing)
        cv2.createTrackbar('G', self.name, 0, 255,self._nothing)
        cv2.createTrackbar('B', self.name, 0, 255,self._nothing)

    def get_tracker(self):
        """Get tracker values to be used for creating thresholding masks.

        Return:
            tuple: Index 0 - Lower bound of the threhold values (RBG or HSV)
                   Index 1 - Upper bound of the threhold values (RBG or HSV)

        """
        r_value = cv2.getTrackbarPos('R',self.name)
        g_value = cv2.getTrackbarPos('G',self.name)
        b_value = cv2.getTrackbarPos('B',self.name)
        return r_value,g_value,b_value
    
    @staticmethod
    def _nothing(val):
        ''' Dummy function used in cv2.createTrackbar().
        
        '''
        pass