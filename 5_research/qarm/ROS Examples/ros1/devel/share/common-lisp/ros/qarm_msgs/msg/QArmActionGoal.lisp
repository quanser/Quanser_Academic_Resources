; Auto-generated. Do not edit!


(cl:in-package qarm_msgs-msg)


;//! \htmlinclude QArmActionGoal.msg.html

(cl:defclass <QArmActionGoal> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (goal_id
    :reader goal_id
    :initarg :goal_id
    :type actionlib_msgs-msg:GoalID
    :initform (cl:make-instance 'actionlib_msgs-msg:GoalID))
   (task_space_position_and_gripper
    :reader task_space_position_and_gripper
    :initarg :task_space_position_and_gripper
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass QArmActionGoal (<QArmActionGoal>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <QArmActionGoal>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'QArmActionGoal)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name qarm_msgs-msg:<QArmActionGoal> is deprecated: use qarm_msgs-msg:QArmActionGoal instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <QArmActionGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:header-val is deprecated.  Use qarm_msgs-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'goal_id-val :lambda-list '(m))
(cl:defmethod goal_id-val ((m <QArmActionGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:goal_id-val is deprecated.  Use qarm_msgs-msg:goal_id instead.")
  (goal_id m))

(cl:ensure-generic-function 'task_space_position_and_gripper-val :lambda-list '(m))
(cl:defmethod task_space_position_and_gripper-val ((m <QArmActionGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:task_space_position_and_gripper-val is deprecated.  Use qarm_msgs-msg:task_space_position_and_gripper instead.")
  (task_space_position_and_gripper m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <QArmActionGoal>) ostream)
  "Serializes a message object of type '<QArmActionGoal>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'goal_id) ostream)
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'task_space_position_and_gripper))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_arr_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_arr_len) ostream))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-double-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream)))
   (cl:slot-value msg 'task_space_position_and_gripper))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <QArmActionGoal>) istream)
  "Deserializes a message object of type '<QArmActionGoal>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'goal_id) istream)
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'task_space_position_and_gripper) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'task_space_position_and_gripper)))
    (cl:dotimes (i __ros_arr_len)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-double-float-bits bits))))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<QArmActionGoal>)))
  "Returns string type for a message object of type '<QArmActionGoal>"
  "qarm_msgs/QArmActionGoal")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'QArmActionGoal)))
  "Returns string type for a message object of type 'QArmActionGoal"
  "qarm_msgs/QArmActionGoal")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<QArmActionGoal>)))
  "Returns md5sum for a message object of type '<QArmActionGoal>"
  "8b2615bf7d9cbd023ac805bbdd42fa97")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'QArmActionGoal)))
  "Returns md5sum for a message object of type 'QArmActionGoal"
  "8b2615bf7d9cbd023ac805bbdd42fa97")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<QArmActionGoal>)))
  "Returns full string definition for message of type '<QArmActionGoal>"
  (cl:format cl:nil "Header header~%~%actionlib_msgs/GoalID goal_id~%float64[] task_space_position_and_gripper~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: actionlib_msgs/GoalID~%# The stamp should store the time at which this goal was requested.~%# It is used by an action server when it tries to preempt all~%# goals that were requested before a certain time~%time stamp~%~%# The id provides a way to associate feedback and~%# result message with specific goal requests. The id~%# specified must be unique.~%string id~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'QArmActionGoal)))
  "Returns full string definition for message of type 'QArmActionGoal"
  (cl:format cl:nil "Header header~%~%actionlib_msgs/GoalID goal_id~%float64[] task_space_position_and_gripper~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: actionlib_msgs/GoalID~%# The stamp should store the time at which this goal was requested.~%# It is used by an action server when it tries to preempt all~%# goals that were requested before a certain time~%time stamp~%~%# The id provides a way to associate feedback and~%# result message with specific goal requests. The id~%# specified must be unique.~%string id~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <QArmActionGoal>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'goal_id))
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'task_space_position_and_gripper) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <QArmActionGoal>))
  "Converts a ROS message object to a list"
  (cl:list 'QArmActionGoal
    (cl:cons ':header (header msg))
    (cl:cons ':goal_id (goal_id msg))
    (cl:cons ':task_space_position_and_gripper (task_space_position_and_gripper msg))
))
