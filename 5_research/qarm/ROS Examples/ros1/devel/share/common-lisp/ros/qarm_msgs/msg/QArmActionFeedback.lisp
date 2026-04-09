; Auto-generated. Do not edit!


(cl:in-package qarm_msgs-msg)


;//! \htmlinclude QArmActionFeedback.msg.html

(cl:defclass <QArmActionFeedback> (roslisp-msg-protocol:ros-message)
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
   (ajs
    :reader ajs
    :initarg :ajs
    :type qarm_msgs-msg:AllJointState
    :initform (cl:make-instance 'qarm_msgs-msg:AllJointState)))
)

(cl:defclass QArmActionFeedback (<QArmActionFeedback>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <QArmActionFeedback>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'QArmActionFeedback)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name qarm_msgs-msg:<QArmActionFeedback> is deprecated: use qarm_msgs-msg:QArmActionFeedback instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <QArmActionFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:header-val is deprecated.  Use qarm_msgs-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'goal_id-val :lambda-list '(m))
(cl:defmethod goal_id-val ((m <QArmActionFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:goal_id-val is deprecated.  Use qarm_msgs-msg:goal_id instead.")
  (goal_id m))

(cl:ensure-generic-function 'ajs-val :lambda-list '(m))
(cl:defmethod ajs-val ((m <QArmActionFeedback>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:ajs-val is deprecated.  Use qarm_msgs-msg:ajs instead.")
  (ajs m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <QArmActionFeedback>) ostream)
  "Serializes a message object of type '<QArmActionFeedback>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'goal_id) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'ajs) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <QArmActionFeedback>) istream)
  "Deserializes a message object of type '<QArmActionFeedback>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'goal_id) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'ajs) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<QArmActionFeedback>)))
  "Returns string type for a message object of type '<QArmActionFeedback>"
  "qarm_msgs/QArmActionFeedback")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'QArmActionFeedback)))
  "Returns string type for a message object of type 'QArmActionFeedback"
  "qarm_msgs/QArmActionFeedback")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<QArmActionFeedback>)))
  "Returns md5sum for a message object of type '<QArmActionFeedback>"
  "a0649d896a8becfdc8b49598942d14f9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'QArmActionFeedback)))
  "Returns md5sum for a message object of type 'QArmActionFeedback"
  "a0649d896a8becfdc8b49598942d14f9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<QArmActionFeedback>)))
  "Returns full string definition for message of type '<QArmActionFeedback>"
  (cl:format cl:nil "Header header~%~%actionlib_msgs/GoalID goal_id~%qarm_msgs/AllJointState ajs~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: actionlib_msgs/GoalID~%# The stamp should store the time at which this goal was requested.~%# It is used by an action server when it tries to preempt all~%# goals that were requested before a certain time~%time stamp~%~%# The id provides a way to associate feedback and~%# result message with specific goal requests. The id~%# specified must be unique.~%string id~%~%~%================================================================================~%MSG: qarm_msgs/AllJointState~%~%std_msgs/Header header~%~%# Name~%string joint_names~%~%# JointCurrent~%float64[] joint_currents~%~%# JointPosition (rad)~%float64[] joint_positions~%~%# JointSpeed (rad/s)~%float64[] joint_speeds~%~%# JointPWM~%float64[] joint_pwms~%~%# JointTemperature~%float64[] joint_temperatures~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'QArmActionFeedback)))
  "Returns full string definition for message of type 'QArmActionFeedback"
  (cl:format cl:nil "Header header~%~%actionlib_msgs/GoalID goal_id~%qarm_msgs/AllJointState ajs~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: actionlib_msgs/GoalID~%# The stamp should store the time at which this goal was requested.~%# It is used by an action server when it tries to preempt all~%# goals that were requested before a certain time~%time stamp~%~%# The id provides a way to associate feedback and~%# result message with specific goal requests. The id~%# specified must be unique.~%string id~%~%~%================================================================================~%MSG: qarm_msgs/AllJointState~%~%std_msgs/Header header~%~%# Name~%string joint_names~%~%# JointCurrent~%float64[] joint_currents~%~%# JointPosition (rad)~%float64[] joint_positions~%~%# JointSpeed (rad/s)~%float64[] joint_speeds~%~%# JointPWM~%float64[] joint_pwms~%~%# JointTemperature~%float64[] joint_temperatures~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <QArmActionFeedback>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'goal_id))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'ajs))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <QArmActionFeedback>))
  "Converts a ROS message object to a list"
  (cl:list 'QArmActionFeedback
    (cl:cons ':header (header msg))
    (cl:cons ':goal_id (goal_id msg))
    (cl:cons ':ajs (ajs msg))
))
