import numpy as np
import cv2
import struct
import socket
import time

def binary_thresholding(frame, lower_bounds, upper_bounds):
	"""This function will automatically detect 3-color (BGR, RGB, HSV) or Grayscale images, and corresponding threshold using the bounds. \n

	INPUTS: \n
	frame - 3-color (BGR, RGB, HSV) image or Grayscale image  \n
	lower_bounds - 'numpy (3,) array for RGB' or 'scalar for grayscale' \n
	upper_bounds - 'numpy (3,) array for RGB' or 'scalar for grayscale' \n  

	OUTPUTS: \n
	binary - image that is 255 within the bounds and 0 otherwise \n
	"""

	if len(frame.shape) == 3: # 3-color (BGR, RGB, HSV) Image input
		binary = cv2.inRange(frame, lower_bounds, upper_bounds)
	elif len(frame.shape) == 2: # Grayscale Image input
		_, binary_low = cv2.threshold(frame, lower_bounds, 255, cv2.THRESH_BINARY) 		# find binary for lower threshold
		_, binary_high = cv2.threshold(frame, upper_bounds, 255, cv2.THRESH_BINARY_INV) 	# find inverse binary for upper threshold
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
	total_size = np.size(frame) # Retrieve total number of pixels in the image
	image_temp = frame.copy()		
	skel = np.zeros(image_temp.shape, dtype='uint8')		
	done = False
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))

	while (not done):

		eroded 		= cv2.erode(image_temp, kernel) 	# Erode the image first.
		dilated 	= cv2.dilate(eroded, kernel)		# Dilate the eroded image. The dilated result should will be larger than eroded, but smaller than image_temp.
		difference 	= cv2.subtract(image_temp, dilated) # Find the stuff that is different -> image_temp minus dilated (not vice versa)
		skel 		= cv2.bitwise_or(skel, difference)  # Take a bitwise_or between skel and and difference. Skel will become thinner
		image_temp 	= eroded.copy()						# Overwrite image_temp with the eroded version. This ensures that image_temp becomes smaller with time, and faster so than dilated.  

		num_zeros = total_size - cv2.countNonZero(image_temp) # If cv2.countNonZero(image_temp) becomes 0, you've gone too far with image_temp. One previous version is skel, and so you are done.
		if num_zeros == total_size:
			done = True
	
	return skel	

def mask_image(frame, row_up, row_down, col_left, col_right):
	"""This function masks the provided binary image outside the rectangle defined by input parameters. 
	If any of the row/col parameters are negative, or outside the bounds of the image size, the returned
	image will be the frame itself. \n
	
	INPUTS: \n
	frame - Binary Image  \n
	row_up - Row index for upper edge of rectangle  \n
	row_down - Row index for lower edge of rectangle  \n
	col_left - Col index for left edge of rectangle  \n
	col_right - Col index for right edge of rectangle  \n
	
	OUTPUTS: \n
	masked_frame - masked copy of frame \n
	"""

	rows, cols 	= frame.shape
	masked 		= np.zeros((rows, cols), dtype='uint8')
	
	if  row_up <= row_down and 		\
		row_down < rows and 		\
		col_left <= col_right and 	\
		col_right < cols and 		\
		row_up > 0 and row_down > 0 and col_left > 0 and col_right > 0: 

		for i in range(row_up, row_down+1):
			temp = np.append( np.zeros((1, col_left), dtype='uint8'), 255*np.ones((1, col_right-col_left), dtype='uint8') )
			masked[i] = np.append( temp, np.zeros((1, cols-col_right), dtype='uint8') )
		masked_frame = cv2.bitwise_and(frame, masked)
	else:
		masked_frame = frame

	return masked_frame

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
	row_right = row
	i = 0
	while i <= (5*cols/8):
		right_end = cols-1
		if (i == 5*cols/8) and (row_right >= row - delta):
			i = 0
			row_right -= 1
			continue
		if row_right < row - delta:
			break
		if (frame[row_right, (cols-1)-(i+1)] > frame[row_right, (cols-1)-(i)]) or (frame[row_right, (cols-1)-(i+1)] > 0):
			right_end = cols-i
			break
		i += 1
	
	# Scan from Left moving Right to find objects
	row_left = row
	i = 0
	while i <= (5*cols/8):
		left_end = 0
		if (i == 5*cols/8) and (row_left >= row - delta):
			i = 0
			row_left -= 1
			continue
		if row_left < row - delta:
			break
		if (frame[row_left, (i+1)] > frame[row_left, i]) or (frame[row_left, (i+1)] > 0):
			left_end = i
			break
		i += 1
	
	# Construct pts format and return it
	pts = np.float32([[left_end, row],[right_end, row]])
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
		all_indices = np.argwhere(binary > 0)
		rows = all_indices[0:-1, 0]
		cols = all_indices[0:-1, 1]
		
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

def get_perspective_transform(pts_upper_row, pts_lower_row):
	"""This function returns a perspective transform from the provided points for a birds-eye-view.
	Use this function during calibration to retrieve a transform with atleast 2 markings perpendicular 
	to the camera.\n
	
	INPUTS: \n
	pts_upper_row - pts extracted using the extract_lane_points_by_row function for 'upper_row' \n
	pts_lower_row - pts extracted using the extract_lane_points_by_row function for 'lower_row' \n

	OUTPUTS: \n
	M - numpy (3,2) perspective transform \n
	"""
	# Restructuring the Original points 
	pts1 = np.array([pts_upper_row[0], \
	 				   pts_upper_row[1], \
					   pts_lower_row[0], \
					   pts_lower_row[1]] )
	# Restructuring the Final points 
	pts2 = np.array([ [pts_lower_row[0][0], pts_upper_row[0][1]] , \
					  [pts_lower_row[1][0], pts_upper_row[0][1]] , \
					   pts_lower_row[0] , \
					   pts_lower_row[1] ])
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

def line_pts(frame, pts, color, closed=False):
	"""This function draws lines in the input image between the provided points. Note 
	that n-1 lines will be drawn for n pts by default. If 'closed' is 'True', then the
	last point will be connected to the first point as well. \n
	
	INPUTS: \n
	frame - RGB or Grayscale image \n
	pts - numpy (n,2) array of n points in the col, row format \n
	color - numpy (3,) array of RGB values \n
	closed - set this to True if you want a closed polygon \n

	OUTPUTS: \n
	None, as the original frame is modified. \n
	"""
	# Draw n-1 lines
	for i in range(pts.shape[0] - 1):
		cv2.line(frame, (pts[i][0], pts[i][1]), (pts[i+1][0], pts[i+1][1]), ( int(color[0]), int(color[1]), int(color[2]) ) )
	# Draw the n-th line if closed is set to True
	if closed==True:	
			cv2.line(frame, (pts[pts.shape[0]][0], pts[pts.shape[0]][1]), (pts[0][0], pts[0][1]), ( int(color[0]), int(color[1]), int(color[2]) ) )

def basic_speed_estimation(mtr_speed):
	'''This function contains the out-of-the-box mapping from encoder counts/s to the longitudonal 
	speed of the QCar. 

	Inputs:
	mtr_speed - encoder speed in counts/s
	
	Outputs:
	car_speed - longitudonal car speed in m/s'''

	# term 1 - counts/s to rot/s 
	# term 2 - ( diff pinion * pinion )  /  ( spur * diff spur )
	# term 3 - shaft to axle gain 
	# term 4 - rot/s to rad/s 
	# term 5 - wheel radius 

	#		  term 1            term 2            term 3   term 4      term 5
	return  (1/720/4)  *  ( (13*19) / (70*37) )  *  1   *  2*np.pi  *  0.0342  *  mtr_speed

def power_consumption_monitor(mtr_current, bat_voltage, min_bat_voltage=10.5, max_bat_voltage=12.6):
	'''This function monitors power consumption and provides a percentage battery remaining indicator as well.

	Inputs:
	mtr_current - motor current input in Amps
	bat_voltage - battery voltage in volts

	Outputs:
	power - power consumption in watts
	bat_level - percentage battery level left'''

	return mtr_current*bat_voltage, 100*((max_bat_voltage - bat_voltage)/(max_bat_voltage - min_bat_voltage))

def control_from_gamepad(LB, RT, left_lateral, X):
	if LB == 1:
		if X == 1 :
			throttle_axis = -(RT + 1) /2 * 0.1 #going backward
			steering_axis = -left_lateral * 0.5 
		else:
			throttle_axis = (RT + 1) /2 * 0.3 #going forward
			steering_axis = -left_lateral * 0.5
	else:
		throttle_axis = 0 
		steering_axis = 0

	command = np.array([throttle_axis, steering_axis])
	return command
