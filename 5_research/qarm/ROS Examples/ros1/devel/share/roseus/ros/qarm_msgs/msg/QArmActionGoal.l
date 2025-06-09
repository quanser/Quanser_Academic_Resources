;; Auto-generated. Do not edit!


(when (boundp 'qarm_msgs::QArmActionGoal)
  (if (not (find-package "QARM_MSGS"))
    (make-package "QARM_MSGS"))
  (shadow 'QArmActionGoal (find-package "QARM_MSGS")))
(unless (find-package "QARM_MSGS::QARMACTIONGOAL")
  (make-package "QARM_MSGS::QARMACTIONGOAL"))

(in-package "ROS")
;;//! \htmlinclude QArmActionGoal.msg.html
(if (not (find-package "ACTIONLIB_MSGS"))
  (ros::roseus-add-msgs "actionlib_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass qarm_msgs::QArmActionGoal
  :super ros::object
  :slots (_header _goal_id _task_space_position_and_gripper ))

(defmethod qarm_msgs::QArmActionGoal
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:goal_id __goal_id) (instance actionlib_msgs::GoalID :init))
    ((:task_space_position_and_gripper __task_space_position_and_gripper) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _header __header)
   (setq _goal_id __goal_id)
   (setq _task_space_position_and_gripper __task_space_position_and_gripper)
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
  (:task_space_position_and_gripper
   (&optional __task_space_position_and_gripper)
   (if __task_space_position_and_gripper (setq _task_space_position_and_gripper __task_space_position_and_gripper)) _task_space_position_and_gripper)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; actionlib_msgs/GoalID _goal_id
    (send _goal_id :serialization-length)
    ;; float64[] _task_space_position_and_gripper
    (* 8    (length _task_space_position_and_gripper)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; actionlib_msgs/GoalID _goal_id
       (send _goal_id :serialize s)
     ;; float64[] _task_space_position_and_gripper
     (write-long (length _task_space_position_and_gripper) s)
     (dotimes (i (length _task_space_position_and_gripper))
       (sys::poke (elt _task_space_position_and_gripper i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; actionlib_msgs/GoalID _goal_id
     (send _goal_id :deserialize buf ptr-) (incf ptr- (send _goal_id :serialization-length))
   ;; float64[] _task_space_position_and_gripper
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _task_space_position_and_gripper (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _task_space_position_and_gripper i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get qarm_msgs::QArmActionGoal :md5sum-) "8b2615bf7d9cbd023ac805bbdd42fa97")
(setf (get qarm_msgs::QArmActionGoal :datatype-) "qarm_msgs/QArmActionGoal")
(setf (get qarm_msgs::QArmActionGoal :definition-)
      "Header header

actionlib_msgs/GoalID goal_id
float64[] task_space_position_and_gripper
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


")



(provide :qarm_msgs/QArmActionGoal "8b2615bf7d9cbd023ac805bbdd42fa97")


