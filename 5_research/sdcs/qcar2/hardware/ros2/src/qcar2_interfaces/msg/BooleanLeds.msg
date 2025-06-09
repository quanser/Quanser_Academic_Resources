## LED commands for QCar2
#std_msgs/Header header

# Names of the LED.
# Must be the following:
#    "left_outside_brake_light"
#    "left_inside_brake_light"
#    "right_inside_brake_light"
#    "right_outside_brake_light"
#    "left_reverse_light"
#    "right_reverse_light"
#    "left_rear_signal"
#    "right_rear_signal"
#    "left_outside_headlight"
#    "left_middle_headlight"
#    "left_inside_headlight"
#    "right_inside_headlight"
#    "right_middle_headlight"
#    "right_outside_headlight"
#    "left_front_signal"
#    "right_front_signal"
string[] led_names

# Values for the "led_names".
# The order must be identical to the "led_names".
# Units are:
#   false or true
bool[] values
