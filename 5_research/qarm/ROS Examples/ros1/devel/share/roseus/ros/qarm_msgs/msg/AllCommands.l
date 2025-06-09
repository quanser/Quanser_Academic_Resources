;; Auto-generated. Do not edit!


(when (boundp 'qarm_msgs::AllCommands)
  (if (not (find-package "QARM_MSGS"))
    (make-package "QARM_MSGS"))
  (shadow 'AllCommands (find-package "QARM_MSGS")))
(unless (find-package "QARM_MSGS::ALLCOMMANDS")
  (make-package "QARM_MSGS::ALLCOMMANDS"))

(in-package "ROS")
;;//! \htmlinclude AllCommands.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass qarm_msgs::AllCommands
  :super ros::object
  :slots (_header _jointcommand _grippercommand _ledcommand ))

(defmethod qarm_msgs::AllCommands
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:jointcommand __jointcommand) (instance qarm_msgs::JointCommand :init))
    ((:grippercommand __grippercommand) (instance qarm_msgs::GripperCommand :init))
    ((:ledcommand __ledcommand) (instance qarm_msgs::LEDCommand :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _jointcommand __jointcommand)
   (setq _grippercommand __grippercommand)
   (setq _ledcommand __ledcommand)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:jointcommand
   (&rest __jointcommand)
   (if (keywordp (car __jointcommand))
       (send* _jointcommand __jointcommand)
     (progn
       (if __jointcommand (setq _jointcommand (car __jointcommand)))
       _jointcommand)))
  (:grippercommand
   (&rest __grippercommand)
   (if (keywordp (car __grippercommand))
       (send* _grippercommand __grippercommand)
     (progn
       (if __grippercommand (setq _grippercommand (car __grippercommand)))
       _grippercommand)))
  (:ledcommand
   (&rest __ledcommand)
   (if (keywordp (car __ledcommand))
       (send* _ledcommand __ledcommand)
     (progn
       (if __ledcommand (setq _ledcommand (car __ledcommand)))
       _ledcommand)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; qarm_msgs/JointCommand _jointcommand
    (send _jointcommand :serialization-length)
    ;; qarm_msgs/GripperCommand _grippercommand
    (send _grippercommand :serialization-length)
    ;; qarm_msgs/LEDCommand _ledcommand
    (send _ledcommand :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; qarm_msgs/JointCommand _jointcommand
       (send _jointcommand :serialize s)
     ;; qarm_msgs/GripperCommand _grippercommand
       (send _grippercommand :serialize s)
     ;; qarm_msgs/LEDCommand _ledcommand
       (send _ledcommand :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; qarm_msgs/JointCommand _jointcommand
     (send _jointcommand :deserialize buf ptr-) (incf ptr- (send _jointcommand :serialization-length))
   ;; qarm_msgs/GripperCommand _grippercommand
     (send _grippercommand :deserialize buf ptr-) (incf ptr- (send _grippercommand :serialization-length))
   ;; qarm_msgs/LEDCommand _ledcommand
     (send _ledcommand :deserialize buf ptr-) (incf ptr- (send _ledcommand :serialization-length))
   ;;
   self)
  )

(setf (get qarm_msgs::AllCommands :md5sum-) "f0d189c98e3eb187f5c6801c66a284fe")
(setf (get qarm_msgs::AllCommands :datatype-) "qarm_msgs/AllCommands")
(setf (get qarm_msgs::AllCommands :definition-)
      "
std_msgs/Header header

qarm_msgs/JointCommand jointcommand
qarm_msgs/GripperCommand grippercommand
qarm_msgs/LEDCommand ledcommand
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

================================================================================
MSG: qarm_msgs/JointCommand

# all values are in rad

float64[] joint_command
================================================================================
MSG: qarm_msgs/GripperCommand

# Gripper 0 - 1
# O is fully open, 1 is fully closed

float64 gripper_command
================================================================================
MSG: qarm_msgs/LEDCommand

# RGB values are scaled from 0 - 255 to 0 - 1 in this msg
# so 0 is 0, 1 is 255, 0.5 is 127, etc
# It should be an arrary of three elements like [1, 0, 0]

float64[] RGB
")



(provide :qarm_msgs/AllCommands "f0d189c98e3eb187f5c6801c66a284fe")


