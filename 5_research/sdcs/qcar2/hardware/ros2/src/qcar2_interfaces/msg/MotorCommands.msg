## Driving command for QCar2 to directly control the Steering angle and Motor throttle
#std_msgs/Header header

# Names of whether to drive steering or throttle. Must be "steering_angle" or "motor_throttle"
string[] motor_names

# Values for the "command_names".
# The order must be identical to the "command_names".
# Units are:
#   "rad" for "steering_angle"
#   "%" for "motor_throttle" (as in 0 to 1 represeting 0 to 100%)
float64[] values
