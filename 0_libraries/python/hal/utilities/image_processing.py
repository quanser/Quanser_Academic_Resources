import cv2
import numpy as np


class ImageProcessing():

    def __init__(self):
        self.imageCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Part of the Lane Detector class
        # --------------------------------
        self.blur = (5, 5)
        self.cannyLowerThreshold = 100
        self.cannyUpperThreshold = 200
        self.DEPTH_CAMERA_AVAILABLE = False
        # --------------------------------
    def calibrate_camera(self, imageCaptures, chessboardDimensions,boxSize):

        print("Performing Camera Calibration")

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((chessboardDimensions[0]*chessboardDimensions[1],3), np.float32)
        # Scaling the location of boxes on the captured image based on the size of the measured chessboard square
        objp[:,:2] = np.mgrid[0:chessboardDimensions[0],0:chessboardDimensions[1]].T.reshape(-1,2)*boxSize

        # Arrays to store object points and image points from all the images.
        objPoints = [] # 3d point in real world space
        imgPoints = [] # 2d points in image plane.

        for image in imageCaptures:
            cv2.imshow("CalibImage", image)
            cv2.waitKey(500)

            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(image, (chessboardDimensions[0],chessboardDimensions[1]), None)

            # Find corners based on valid checkerboard patterns
            if ret:
                objPoints.append(objp)
                corners2 = cv2.cornerSubPix(image,corners, (11,11), (-1,-1), self.imageCriteria)
                imgPoints.append(corners2)

            '''
            Outputs for openCV camera calibraton function
            ret_val            = Average projection error, the closer to 0 the better
            camera_matrix      = Calibrated camera matrix
            dist_coeffs        = radial and tangential distortion coefficients
            r_vecs             = Rotation vectors for each image
            t_vecs             = translation vector for each image
            std_dev_intrinsics = Camera intrinsics standard deviation
            std_dev_extrinsics = Camera extrinsics standard deviation
            '''
        retval, cameraMatrix, distCoeffs, rvecs, tvecs, stdDevIntrinsics, stdDevExtrinsics, PerViewErrors = cv2.calibrateCameraExtended(objPoints, imgPoints, image.shape[::-1], None, None)

        print("Calibration projection error: ", retval)

        return  cameraMatrix , distCoeffs

    def undistort_img(self,distImgs,cameraMatrix,distCoefficients):
 
        undist = cv2.undistort(distImgs,cameraMatrix, distCoefficients,None,cameraMatrix)
        return undist

    def do_canny(self, frame):
        # Converts frame to grayscale because we only need the luminance channel for detecting edges - less computationally expensive
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        # Applies a 5x5 gaussian blur with deviation of 0 to frame - not mandatory since Canny will do this for us
        blur = cv2.GaussianBlur(gray, self.blur, 0)
        # Applies Canny edge detector with minVal of 50 and maxVal of 150
        canny = cv2.Canny(blur, self.cannyLowerThreshold, self.cannyUpperThreshold)
        return canny

    def do_segment(self, frame, steering = 0):

        # Creates a polygon for the mask defined by multiple coordinates
        polygons = np.array([
                                [(0, int(0.9*self.height - 0.4*self.height*steering)),
                                (0, self.height),
                                (self.width, self.height),
                                (self.width, int(0.9*self.height + 0.4*self.height*steering)),
                                (int(self.width/2 + int(self.width/6) - int(self.width/3)*3*steering), int(3.5*self.height/5)),
                                (int(self.width/2 - int(self.width/6) - int(self.width/3)*3*steering), int(3.5*self.height/5))]
                            ])

        # Creates an image filled with zero intensities with the same dimensions as the frame
        mask = np.zeros_like(frame)

        # Allows the mask to be filled with values of 1 and the other areas to be filled with values of 0
        cv2.fillPoly(mask, polygons, 255)
        # A bitwise and operation between the mask and frame keeps only the triangular area of the frame
        segment = cv2.bitwise_and(frame, mask)

        return segment, mask

    def calculate_lines(self, segment):
        # +--------> x-axis
        # |               /          |               \
        # |             /            | Inf slope      \                     0 slope
        # v           / -ve slope    |                 \ +ve slope      _______________
        # y-axis    /                |                  \
        #
        # Use hough function to get the lines in the image. vertical line has Infinite slope. Horizontal line has slope 0.
        lines = cv2.HoughLinesP(segment, 2, np.pi/180, 100, np.array([]), minLineLength = 150, maxLineGap = 100)

        # Empty arrays to store the coordinates of the left and right lines
        left = []
        right = []

        # Loops through every detected line
        if lines is None:
            # No lines were found, womp womp
            return [], []
        else:
            # Group the lines into a left/right category
            for line in lines:
                # Reshapes line from 2D array to 1D array
                x1, y1, x2, y2 = line.reshape(4)
                # Fit a linear polynomial to the x and y coordinates and returns a vector of coefficients which describe the slope and y-intercept
                parameters = np.polyfit((x1, x2), (y1, y2), 1)
                slope = parameters[0]
                y_intercept = parameters[1]

                # Avoid lines that have slopes close to 0, as these might be crosswalks,
                # or parking lanes, etc. Thus, anything with a slope higher than 0.1, will
                # be the right lane, and less than -0.1 will be the left lane.
                if slope < -0.1:
                    left.append([slope, y_intercept])
                elif slope > 0.1:
                    right.append([slope, y_intercept])
            return left, right

    def average_lines(self, frame, left, right):
        # Averages out all the values for left and right into a single slope and y-intercept value for each line

        if len(left) > 0:
            leftParameter = np.average(left, axis = 0)
            leftLine = self.calculate_coordinates(leftParameter)
        else:
            leftParameter = None
            leftLine = None
        if len(right) > 0:
            rightParameter = np.average(right, axis = 0)
            rightLine = self.calculate_coordinates(rightParameter)
        else:
            rightParameter = None
            rightLine = None

        return [leftParameter, rightParameter], self.visualizeLines(frame, np.array([leftLine, rightLine]))

    def calculate_coordinates(self, parameters):

        slope, intercept = parameters
        # Sets initial y-coordinate as height from top down (bottom of the frame)
        y1 = self.height
        # Sets final y-coordinate as 150 above the bottom of the frame
        y2 = int(y1 - 1.5*self.height/5)
        # Sets initial x-coordinate as (y1 - b) / m since y1 = mx1 + b
        x1 = int((y1 - intercept) / slope)
        # Sets final x-coordinate as (y2 - b) / m since y2 = mx2 + b
        x2 = int((y2 - intercept) / slope)

        return np.array([x1, y1, x2, y2])

    def driving_parameters(self, lineParameters):
        if lineParameters[0] is not None:
            m, b = lineParameters[0]
            actualLeft  = int((255 - b)/m)
            desiredLeft = int((255 - 423)/(-0.53))
            motorSpeed = 0.05
            steering = (desiredLeft - actualLeft)/600 + 0.5*(m + 0.53)
            print('Using Left Lane:', lineParameters[0], steering)

        elif lineParameters[1] is not None:
            m, b = lineParameters[1]
            actualRight  = int((255 - b)/m)
            desiredRight = int((255 - 30)/(0.65))
            motorSpeed = 0.05
            steering = (desiredRight - actualRight)/600 + 0.5*(m - 0.65)
            print('Using Right Lane:', lineParameters[1], steering)

        else:
            steering = 0
            motorSpeed = 0
            print('No Driving Lane Available')

        return motorSpeed, steering

    def visualize_lines(self, frame, lines):
        # Checks if any lines are detected

        for line in lines:
            if line is not None:
                x1, y1, x2, y2 = line
                # Draws lines between two coordinates with green color and 5 thickness
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        return frame

    def detect_yelllow_lane(self, frame):
        lowerBounds = (40, 200, 200)
        upperBounds = (120, 255, 255)
        mask = cv2.inRange(frame, lowerBounds, upperBounds)
        mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=1)
        return mask

    def extract_point_given_row(self, row):
        counter = len(row)
        solution = -1
        for i in range(len(row)):
            if row[counter - 1 - i] > 0:
                solution = counter - 1 - i
                break

        return solution

    def body_to_image(self, bodyPoint, extrinsicMatrix,intrinsicMatrix ):


        # convert from tuple to 2D numpy array
        bodyPoint = np.array([[bodyPoint[0]], [bodyPoint[1]], [bodyPoint[2]]])

        # convert body point to camera point using Extrinsic Matrix
        cameraPoint = extrinsicMatrix@np.concatenate((bodyPoint, np.array([[1]])))

        # convert camera point to image point - the camera point is an [cx, cy, cz, 1] vector. Ignore the 1, and
        # premultiply it to get the image point, of form, [ix, iy, iz]
        imagePoint = intrinsicMatrix@cameraPoint[0:3]

        # convert camera point and image point back to tuple for return
        cameraPoint = (cameraPoint[0, 0], cameraPoint[1, 0], cameraPoint[2, 0])
        imagePoint = (imagePoint[0, 0] / imagePoint[2, 0], imagePoint[1, 0] / imagePoint[2, 0])

        return cameraPoint, imagePoint

    def image_to_body(self, imagePoint,extrinsicMatrix,intrinsicMatrix):

        # Use the camera intrinsic matrix to extract the principle point and the focal length
        principlePoint = [intrinsicMatrix[0][2],intrinsicMatrix[1][2]]
        focalLength    = [intrinsicMatrix[0][0],intrinsicMatrix[1][1]]

        imagePoint = np.array([[imagePoint[0]], [imagePoint[1]]])
        cameraPointRatio = (imagePoint - principlePoint)/focalLength

        # cameraPointRatio is (Cx/Cz, Cy/Cz). The Cy value for a road is fixed, which is the extrinsicMatrix(1,3), that is, 2nd row 4th col
        Cy = extrinsicMatrix[1,3]
        Cz = Cy / cameraPointRatio[1, 0]
        Cx = Cz * cameraPointRatio[0, 0]

        cameraPoint = np.array([[Cx], [Cy], [Cz], [1]], dtype = np.float64)

        # map the point back to body frame
        bodyPoint = np.linalg.inv(extrinsicMatrix)@cameraPoint

        cameraPoint = (cameraPoint[0, 0], cameraPoint[1, 0], cameraPoint[2, 0])
        bodyPoint = (bodyPoint[0, 0], bodyPoint[1, 0], bodyPoint[2, 0])

        return cameraPoint, bodyPoint

    def binary_thresholding(frame, lowerBounds, upperBounds):
        """This function will automatically detect 3-color (BGR, RGB, HSV) or Grayscale images, and corresponding threshold using the bounds. \n

        INPUTS: \n
        frame - 3-color (BGR, RGB, HSV) image or Grayscale image  \n
        lower_bounds - 'numpy (3,) array for RGB' or 'scalar for grayscale' \n
        upper_bounds - 'numpy (3,) array for RGB' or 'scalar for grayscale' \n

        OUTPUTS: \n
        binary - image that is 255 within the bounds and 0 otherwise \n
        """

        if len(frame.shape) == 3: # 3-color (BGR, RGB, HSV) Image input
            binary = cv2.inRange(frame, lowerBounds, upperBounds)
        elif len(frame.shape) == 2: # Grayscale Image input
            _, binary_low = cv2.threshold(frame, lowerBounds, 255, cv2.THRESH_BINARY) 		# find binary for lower threshold
            _, binary_high = cv2.threshold(frame, upperBounds, 255, cv2.THRESH_BINARY_INV) 	# find inverse binary for upper threshold
            binary = cv2.bitwise_and(binary_low/255, binary_high/255) 								# combine the binaries

        return binary

    def image_filtering_close(frame, dilate=1, erode=1, total=1):
        """This function performs a morphological dilation followed by erosion, useful for filling small holes/gaps in the image. \n

        INPUTS: \n
        frame - 3-color (BGR, RGB, HSV) or Grayscale or Binary Image  \n

        OUTPUTS: \n
        clean - morphologically closed copy of the input frame \n
        """

        kernel 	= np.ones((5,5), np.uint8)
        for _ in range(total):
            dilated = cv2.dilate(frame, kernel, iterations=dilate)
            clean 	= cv2.erode(dilated, kernel, iterations=erode)

        return clean

    def image_filtering_open(frame, dilate=1, erode=1, total=1):
        """This function performs a morphological erosion followed by dilation, useful for removing small objects in the image. \n

        INPUTS: \n
        frame - 3-color (BGR, RGB, HSV) or Grayscale or Binary Image  \n

        OUTPUTS: \n
        clean - morphologically opened copy of the input frame \n
        """

        kernel	= np.ones((5,5), np.uint8)
        for _ in range(total):
            eroded 	= cv2.erode(frame, kernel, iterations=erode)
            clean 	= cv2.dilate(eroded, kernel, iterations=dilate)

        return clean

    def image_filtering_skeletonize(frame):
        """This function performs a morphological skeletonization, useful for retrieving the skeleton of an image while maintaining the Euler # of objects. \n

        INPUTS: \n
        frame - Grayscale or Binary Image  \n

        OUTPUTS: \n
        clean - morphologically skeletonized copy of the input frame \n
        """
        totalSize = np.size(frame) # Retrieve total number of pixels in the image
        imageTemp = frame.copy()
        skel = np.zeros(imageTemp.shape, dtype='uint8')
        done = False
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))

        while (not done):

            eroded 		= cv2.erode(imageTemp, kernel) 	# Erode the image first.
            dilated 	= cv2.dilate(eroded, kernel)		# Dilate the eroded image. The dilated result should will be larger than eroded, but smaller than imageTemp.
            difference 	= cv2.subtract(imageTemp, dilated) # Find the stuff that is different -> imageTemp minus dilated (not vice versa)
            skel 		= cv2.bitwise_or(skel, difference)  # Take a bitwise_or between skel and and difference. Skel will become thinner
            imageTemp 	= eroded.copy()						# Overwrite imageTemp with the eroded version. This ensures that imageTemp becomes smaller with time, and faster so than dilated.

            numZeros = totalSize - cv2.countNonZero(imageTemp) # If cv2.countNonZero(imageTemp) becomes 0, you've gone too far with imageTemp. One previous version is skel, and so you are done.
            if numZeros == totalSize:
                done = True

        return skel

    def mask_image(frame, rowUp, rowDown, colLeft, colRight):
        """This function masks the provided binary image outside the rectangle defined by input parameters.
        If any of the row/col parameters are negative, or outside the bounds of the image size, the returned
        image will be the frame itself. \n

        INPUTS: \n
        frame - Binary Image  \n
        rowUp - Row index for upper edge of rectangle  \n
        rowDown - Row index for lower edge of rectangle  \n
        colLeft - Col index for left edge of rectangle  \n
        colRight - Col index for right edge of rectangle  \n

        OUTPUTS: \n
        maskedFrame - masked copy of frame \n
        """

        rows, cols 	= frame.shape
        masked 		= np.zeros((rows, cols), dtype='uint8')

        if  rowUp <= rowDown and 		\
            rowDown < rows and 		\
            colLeft <= colRight and 	\
            colRight < cols and 		\
            rowUp > 0 and rowDown > 0 and colLeft > 0 and colRight > 0:

            for i in range(rowUp, rowDown+1):
                temp = np.append( np.zeros((1, colLeft), dtype='uint8'), 255*np.ones((1, colRight-colLeft), dtype='uint8') )
                masked[i] = np.append( temp, np.zeros((1, cols-colRight), dtype='uint8') )
            maskedFrame = cv2.bitwise_and(frame, masked)
        else:
            maskedFrame = frame

        return maskedFrame

    def extract_lane_points_by_row(frame, row):
        """This function extracts the left most and right most point in provided row in the input frame where a black to white pixel transition is detected. \n

        INPUTS: \n
        frame - binary image \n
        row - row in which the points are found \n

        OUTPUTS: \n
        pts - numpy (2,2) array in format: [ [left_col, row],  [right_col, row] ] \n
        """

        # binary Image expected in frame
        _, cols = frame.shape
        delta = 0

        # Scan from Right moving Left to find the edges
        rowRight = row
        i = 0
        while i <= (5*cols/8):
            rightEnd = cols-1
            if (i == 5*cols/8) and (rowRight >= row - delta):
                i = 0
                rowRight -= 1
                continue
            if rowRight < row - delta:
                break
            if (frame[rowRight, (cols-1)-(i+1)] > frame[rowRight, (cols-1)-(i)]) or (frame[rowRight, (cols-1)-(i+1)] > 0):
                rightEnd = cols-i
                break
            i += 1

        # Scan from Left moving Right to find objects
        rowLeft = row
        i = 0
        while i <= (5*cols/8):
            leftEnd = 0
            if (i == 5*cols/8) and (rowLeft >= row - delta):
                i = 0
                rowLeft -= 1
                continue
            if rowLeft < row - delta:
                break
            if (frame[rowLeft, (i+1)] > frame[rowLeft, i]) or (frame[rowLeft, (i+1)] > 0):
                leftEnd = i
                break
            i += 1

        # Construct pts format and return it
        pts = np.float32([[leftEnd, row],[rightEnd, row]])
        return pts

    def find_slope_intercept_from_binary(binary):
        """This function will return the linear polynomial fit coefficients to the lane found in a binary image. \n

        INPUTS: \n
        binary - binary image \n

        OUTPUTS: \n
        slope - slope m of the line found \n
        intercept - intercept b of the line found \n
        """

        # parameters expected normally
        slope, intercept = 0.3419, 0

        try:
            # find indices where the binary image is TRUE and convert the indices to row/col format
            totalNumIndices = np.argwhere(binary > 0)
            rows = totalNumIndices[0:-1, 0]
            cols = totalNumIndices[0:-1, 1]

        # if you found more than a 1000 points
            n = len(rows)
            if n > 1000:
                p = int(n/10)
                idx = np.random.choice(n, p)

                x = cols
                y = binary.shape[0] - rows

                if len(x) == 0 or len(y) == 0:
                    return 0, 0
                fit = np.polyfit(x[idx], y[idx], 1)
                slope, intercept = fit

        except KeyboardInterrupt:
            print('User Interupted')
        finally:
            return slope, intercept

    def get_perspective_transform(ptsUpperRow, ptsLowerRow):
        """This function returns a perspective transform from the provided points for a birds-eye-view.
        Use this function during calibration to retrieve a transform with atleast 2 markings perpendicular
        to the camera.\n

        INPUTS: \n
        ptsUpperRow - pts extracted using the extract_lane_points_by_row function for 'upper_row' \n
        ptsLowerRow - pts extracted using the extract_lane_points_by_row function for 'lower_row' \n

        OUTPUTS: \n
        M - numpy (3,2) perspective transform \n
        """
        # Restructuring the Original points
        pts1 = np.array([ptsUpperRow[0], \
                        ptsUpperRow[1], \
                        ptsLowerRow[0], \
                        ptsLowerRow[1]] )
        # Restructuring the Final points
        pts2 = np.array([ [ptsLowerRow[0][0], ptsUpperRow[0][1]] , \
                        [ptsLowerRow[1][0], ptsUpperRow[0][1]] , \
                        ptsLowerRow[0] , \
                        ptsLowerRow[1] ])
        # Get the Perspective Transform
        M = cv2.getPerspectiveTransform(pts1, pts2)
        return M

    def circle_pts(frame, pts, radius, color):
        """This function draws a circle in the input image at the provided points. \n

        INPUTS: \n
        frame - RGB or Grayscale image \n
        pts - numpy (n,2) array of n points in the col, row format \n
        radius - scalar integer representing the radius in pixels of the circle that will be drawn \n
        color - numpy (3,) array of RGB values \n

        OUTPUTS: \n
        None, as the original frame is modified \n
        """
        for i in range(pts.shape[0]):
            cv2.circle(frame, (pts[i][0], pts[i][1]), radius, ( int(color[0]), int(color[1]), int(color[2]) ), thickness=5 )

    def extract_lines(self,filteredImage, originalImage):

        linesImage = np.copy(originalImage)

        # Using the probabilistic hough transform to get line points from filtered image:
        lines = cv2.HoughLinesP(filteredImage, 1, np.pi/180, 10,1,1)

        try:
            # Extract the starting and ending points of all the lines found and draw them on the original image
            for line in lines:
                x1,y1, x2,y2 = line[0]
                cv2.line(linesImage, (x1,y1), (x2,y2), (0,0,255),2)
        except:
            lines = 0
        return linesImage, lines
