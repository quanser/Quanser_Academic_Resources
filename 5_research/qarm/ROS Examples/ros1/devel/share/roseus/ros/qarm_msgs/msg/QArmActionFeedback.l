;; Auto-generated. Do not edit!


(when (boundp 'qarm_msgs::QArmActionFeedback)
  (if (not (find-package "QARM_MSGS"))
    (make-package "QARM_MSGS"))
  (shadow 'QArmActionFeedback (find-package "QARM_MSGS")))
(unless (find-package "QARM_MSGS::QARMACTIONFEEDBACK")
  (make-package "QARM_MSGS::QARMACTIONFEEDBACK"))

(in-package "ROS")
;;//! \htmlinclude QArmActionFeedback.msg.html
(if (not (find-package "ACTIONLIB_MSGS"))
  (ros::roseus-add-msgs "actionlib_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass qarm_msgs::QArmActionFeedback
  :super ros::object
  :slots (_header _goal_id _ajs ))

(defmethod qarm_msgs::QArmActionFeedback
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:goal_id __goal_id) (instance actionlib_msgs::GoalID :init))
    ((:ajs __ajs) (instance qarm_msgs::AllJointState :init))
    )
   (send-super :init)
   (setq _header __header)
   (setq _goal_id __goal_id)
   (setq _ajs __ajs)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:goal_id
   (&rest __goal_id)
   (if (keywordp (car __goal_id))
       (send* _goal_id __goal_id)
     (progn
       (if __goal_id (setq _goal_id (car __goal_id)))
       _goal_id)))
  (:ajs
   (&rest __ajs)
   (if (keywordp (car __ajs))
       (send* _ajs __ajs)
     (progn
       (if __ajs (setq _ajs (car __ajs)))
       _ajs)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; actionlib_msgs/GoalID _goal_id
    (send _goal_id :serialization-length)
    ;; qarm_msgs/AllJointState _ajs
    (send _ajs :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; actionlib_msgs/GoalID _goal_id
       (send _goal_id :serialize s)
     ;; qarm_msgs/AllJointState _ajs
       (send _ajs :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; actionlib_msgs/GoalID _goal_id
     (send _goal_id :deserialize buf ptr-) (incf ptr- (send _goal_id :serialization-length))
   ;; qarm_msgs/AllJointState _ajs
     (send _ajs :deserialize buf ptr-) (incf ptr- (send _ajs :serialization-length))
   ;;
   self)
  )

(setf (get qarm_msgs::QArmActionFeedback :md5sum-) "a0649d896a8becfdc8b49598942d14f9")
(setf (get qarm_msgs::QArmActionFeedback :datatype-) "qarm_msgs/QArmActionFeedback")
(setf (get qarm_msgs::QArmActionFeedback :definition-)
      "Header header

actionlib_msgs/GoalID goal_id
qarm_msgs/AllJointState ajs
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
MSG: actionlib_msgs/GoalID
# The stamp should store the time at which this goal was requested.
# It is used by an action server when it tries to preempt all
# goals that were requested before a certain time
time stamp

# The id provides a way to associate feedback and
# result message with specific goal requests. The id
# specified must be unique.
string id


================================================================================
MSG: qarm_msgs/AllJointState

std_msgs/Header header

# Name
string joint_names

# JointCurrent
float64[] joint_currents

# JointPosition (rad)
float64[] joint_positions

# JointSpeed (rad/s)
float64[] joint_speeds

# JointPWM
float64[] joint_pwms

# JointTemperature
float64[] joint_temperatures
")



(provide :qarm_msgs/QArmActionFeedback "a0649d896a8becfdc8b49598942d14f9")


