; Auto-generated. Do not edit!


(cl:in-package qarm_msgs-msg)


;//! \htmlinclude GripperCommand.msg.html

(cl:defclass <GripperCommand> (roslisp-msg-protocol:ros-message)
  ((gripper_command
    :reader gripper_command
    :initarg :gripper_command
    :type cl:float
    :initform 0.0))
)

(cl:defclass GripperCommand (<GripperCommand>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GripperCommand>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GripperCommand)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name qarm_msgs-msg:<GripperCommand> is deprecated: use qarm_msgs-msg:GripperCommand instead.")))

(cl:ensure-generic-function 'gripper_command-val :lambda-list '(m))
(cl:defmethod gripper_command-val ((m <GripperCommand>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:gripper_command-val is deprecated.  Use qarm_msgs-msg:gripper_command instead.")
  (gripper_command m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GripperCommand>) ostream)
  "Serializes a message object of type '<GripperCommand>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'gripper_command))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GripperCommand>) istream)
  "Deserializes a message object of type '<GripperCommand>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'gripper_command) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GripperCommand>)))
  "Returns string type for a message object of type '<GripperCommand>"
  "qarm_msgs/GripperCommand")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GripperCommand)))
  "Returns string type for a message object of type 'GripperCommand"
  "qarm_msgs/GripperCommand")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GripperCommand>)))
  "Returns md5sum for a message object of type '<GripperCommand>"
  "a6ae6f959759a14d8596011d33fb4140")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GripperCommand)))
  "Returns md5sum for a message object of type 'GripperCommand"
  "a6ae6f959759a14d8596011d33fb4140")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GripperCommand>)))
  "Returns full string definition for message of type '<GripperCommand>"
  (cl:format cl:nil "~%# Gripper 0 - 1~%# O is fully open, 1 is fully closed~%~%float64 gripper_command~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GripperCommand)))
  "Returns full string definition for message of type 'GripperCommand"
  (cl:format cl:nil "~%# Gripper 0 - 1~%# O is fully open, 1 is fully closed~%~%float64 gripper_command~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GripperCommand>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GripperCommand>))
  "Converts a ROS message object to a list"
  (cl:list 'GripperCommand
    (cl:cons ':gripper_command (gripper_command msg))
))
