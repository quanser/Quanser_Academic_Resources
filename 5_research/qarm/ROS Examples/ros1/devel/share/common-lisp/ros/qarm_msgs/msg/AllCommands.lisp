; Auto-generated. Do not edit!


(cl:in-package qarm_msgs-msg)


;//! \htmlinclude AllCommands.msg.html

(cl:defclass <AllCommands> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (jointcommand
    :reader jointcommand
    :initarg :jointcommand
    :type qarm_msgs-msg:JointCommand
    :initform (cl:make-instance 'qarm_msgs-msg:JointCommand))
   (grippercommand
    :reader grippercommand
    :initarg :grippercommand
    :type qarm_msgs-msg:GripperCommand
    :initform (cl:make-instance 'qarm_msgs-msg:GripperCommand))
   (ledcommand
    :reader ledcommand
    :initarg :ledcommand
    :type qarm_msgs-msg:LEDCommand
    :initform (cl:make-instance 'qarm_msgs-msg:LEDCommand)))
)

(cl:defclass AllCommands (<AllCommands>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <AllCommands>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'AllCommands)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name qarm_msgs-msg:<AllCommands> is deprecated: use qarm_msgs-msg:AllCommands instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <AllCommands>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:header-val is deprecated.  Use qarm_msgs-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'jointcommand-val :lambda-list '(m))
(cl:defmethod jointcommand-val ((m <AllCommands>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:jointcommand-val is deprecated.  Use qarm_msgs-msg:jointcommand instead.")
  (jointcommand m))

(cl:ensure-generic-function 'grippercommand-val :lambda-list '(m))
(cl:defmethod grippercommand-val ((m <AllCommands>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:grippercommand-val is deprecated.  Use qarm_msgs-msg:grippercommand instead.")
  (grippercommand m))

(cl:ensure-generic-function 'ledcommand-val :lambda-list '(m))
(cl:defmethod ledcommand-val ((m <AllCommands>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:ledcommand-val is deprecated.  Use qarm_msgs-msg:ledcommand instead.")
  (ledcommand m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <AllCommands>) ostream)
  "Serializes a message object of type '<AllCommands>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'jointcommand) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'grippercommand) ostream)
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'ledcommand) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <AllCommands>) istream)
  "Deserializes a message object of type '<AllCommands>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'jointcommand) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'grippercommand) istream)
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'ledcommand) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<AllCommands>)))
  "Returns string type for a message object of type '<AllCommands>"
  "qarm_msgs/AllCommands")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'AllCommands)))
  "Returns string type for a message object of type 'AllCommands"
  "qarm_msgs/AllCommands")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<AllCommands>)))
  "Returns md5sum for a message object of type '<AllCommands>"
  "f0d189c98e3eb187f5c6801c66a284fe")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'AllCommands)))
  "Returns md5sum for a message object of type 'AllCommands"
  "f0d189c98e3eb187f5c6801c66a284fe")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<AllCommands>)))
  "Returns full string definition for message of type '<AllCommands>"
  (cl:format cl:nil "~%std_msgs/Header header~%~%qarm_msgs/JointCommand jointcommand~%qarm_msgs/GripperCommand grippercommand~%qarm_msgs/LEDCommand ledcommand~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: qarm_msgs/JointCommand~%~%# all values are in rad~%~%float64[] joint_command~%================================================================================~%MSG: qarm_msgs/GripperCommand~%~%# Gripper 0 - 1~%# O is fully open, 1 is fully closed~%~%float64 gripper_command~%================================================================================~%MSG: qarm_msgs/LEDCommand~%~%# RGB values are scaled from 0 - 255 to 0 - 1 in this msg~%# so 0 is 0, 1 is 255, 0.5 is 127, etc~%# It should be an arrary of three elements like [1, 0, 0]~%~%float64[] RGB~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'AllCommands)))
  "Returns full string definition for message of type 'AllCommands"
  (cl:format cl:nil "~%std_msgs/Header header~%~%qarm_msgs/JointCommand jointcommand~%qarm_msgs/GripperCommand grippercommand~%qarm_msgs/LEDCommand ledcommand~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%================================================================================~%MSG: qarm_msgs/JointCommand~%~%# all values are in rad~%~%float64[] joint_command~%================================================================================~%MSG: qarm_msgs/GripperCommand~%~%# Gripper 0 - 1~%# O is fully open, 1 is fully closed~%~%float64 gripper_command~%================================================================================~%MSG: qarm_msgs/LEDCommand~%~%# RGB values are scaled from 0 - 255 to 0 - 1 in this msg~%# so 0 is 0, 1 is 255, 0.5 is 127, etc~%# It should be an arrary of three elements like [1, 0, 0]~%~%float64[] RGB~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <AllCommands>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'jointcommand))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'grippercommand))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'ledcommand))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <AllCommands>))
  "Converts a ROS message object to a list"
  (cl:list 'AllCommands
    (cl:cons ':header (header msg))
    (cl:cons ':jointcommand (jointcommand msg))
    (cl:cons ':grippercommand (grippercommand msg))
    (cl:cons ':ledcommand (ledcommand msg))
))
