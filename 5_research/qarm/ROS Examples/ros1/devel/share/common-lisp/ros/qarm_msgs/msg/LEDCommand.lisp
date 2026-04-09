; Auto-generated. Do not edit!


(cl:in-package qarm_msgs-msg)


;//! \htmlinclude LEDCommand.msg.html

(cl:defclass <LEDCommand> (roslisp-msg-protocol:ros-message)
  ((RGB
    :reader RGB
    :initarg :RGB
    :type (cl:vector cl:float)
   :initform (cl:make-array 0 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass LEDCommand (<LEDCommand>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <LEDCommand>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'LEDCommand)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name qarm_msgs-msg:<LEDCommand> is deprecated: use qarm_msgs-msg:LEDCommand instead.")))

(cl:ensure-generic-function 'RGB-val :lambda-list '(m))
(cl:defmethod RGB-val ((m <LEDCommand>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader qarm_msgs-msg:RGB-val is deprecated.  Use qarm_msgs-msg:RGB instead.")
  (RGB m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <LEDCommand>) ostream)
  "Serializes a message object of type '<LEDCommand>"
  (cl:let ((__ros_arr_len (cl:length (cl:slot-value msg 'RGB))))
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
   (cl:slot-value msg 'RGB))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <LEDCommand>) istream)
  "Deserializes a message object of type '<LEDCommand>"
  (cl:let ((__ros_arr_len 0))
    (cl:setf (cl:ldb (cl:byte 8 0) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) __ros_arr_len) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) __ros_arr_len) (cl:read-byte istream))
  (cl:setf (cl:slot-value msg 'RGB) (cl:make-array __ros_arr_len))
  (cl:let ((vals (cl:slot-value msg 'RGB)))
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
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<LEDCommand>)))
  "Returns string type for a message object of type '<LEDCommand>"
  "qarm_msgs/LEDCommand")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'LEDCommand)))
  "Returns string type for a message object of type 'LEDCommand"
  "qarm_msgs/LEDCommand")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<LEDCommand>)))
  "Returns md5sum for a message object of type '<LEDCommand>"
  "f723af9a2be20e93588f85bf623cd8b4")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'LEDCommand)))
  "Returns md5sum for a message object of type 'LEDCommand"
  "f723af9a2be20e93588f85bf623cd8b4")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<LEDCommand>)))
  "Returns full string definition for message of type '<LEDCommand>"
  (cl:format cl:nil "~%# RGB values are scaled from 0 - 255 to 0 - 1 in this msg~%# so 0 is 0, 1 is 255, 0.5 is 127, etc~%# It should be an arrary of three elements like [1, 0, 0]~%~%float64[] RGB~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'LEDCommand)))
  "Returns full string definition for message of type 'LEDCommand"
  (cl:format cl:nil "~%# RGB values are scaled from 0 - 255 to 0 - 1 in this msg~%# so 0 is 0, 1 is 255, 0.5 is 127, etc~%# It should be an arrary of three elements like [1, 0, 0]~%~%float64[] RGB~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <LEDCommand>))
  (cl:+ 0
     4 (cl:reduce #'cl:+ (cl:slot-value msg 'RGB) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 8)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <LEDCommand>))
  "Converts a ROS message object to a list"
  (cl:list 'LEDCommand
    (cl:cons ':RGB (RGB msg))
))
