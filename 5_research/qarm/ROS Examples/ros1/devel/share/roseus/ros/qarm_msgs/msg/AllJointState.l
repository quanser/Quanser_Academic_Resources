;; Auto-generated. Do not edit!


(when (boundp 'qarm_msgs::AllJointState)
  (if (not (find-package "QARM_MSGS"))
    (make-package "QARM_MSGS"))
  (shadow 'AllJointState (find-package "QARM_MSGS")))
(unless (find-package "QARM_MSGS::ALLJOINTSTATE")
  (make-package "QARM_MSGS::ALLJOINTSTATE"))

(in-package "ROS")
;;//! \htmlinclude AllJointState.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass qarm_msgs::AllJointState
  :super ros::object
  :slots (_header _joint_names _joint_currents _joint_positions _joint_speeds _joint_pwms _joint_temperatures ))

(defmethod qarm_msgs::AllJointState
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:joint_names __joint_names) "")
    ((:joint_currents __joint_currents) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:joint_positions __joint_positions) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:joint_speeds __joint_speeds) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:joint_pwms __joint_pwms) (make-array 0 :initial-element 0.0 :element-type :float))
    ((:joint_temperatures __joint_temperatures) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _header __header)
   (setq _joint_names (string __joint_names))
   (setq _joint_currents __joint_currents)
   (setq _joint_positions __joint_positions)
   (setq _joint_speeds __joint_speeds)
   (setq _joint_pwms __joint_pwms)
   (setq _joint_temperatures __joint_temperatures)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:joint_names
   (&optional __joint_names)
   (if __joint_names (setq _joint_names __joint_names)) _joint_names)
  (:joint_currents
   (&optional __joint_currents)
   (if __joint_currents (setq _joint_currents __joint_currents)) _joint_currents)
  (:joint_positions
   (&optional __joint_positions)
   (if __joint_positions (setq _joint_positions __joint_positions)) _joint_positions)
  (:joint_speeds
   (&optional __joint_speeds)
   (if __joint_speeds (setq _joint_speeds __joint_speeds)) _joint_speeds)
  (:joint_pwms
   (&optional __joint_pwms)
   (if __joint_pwms (setq _joint_pwms __joint_pwms)) _joint_pwms)
  (:joint_temperatures
   (&optional __joint_temperatures)
   (if __joint_temperatures (setq _joint_temperatures __joint_temperatures)) _joint_temperatures)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; string _joint_names
    4 (length _joint_names)
    ;; float64[] _joint_currents
    (* 8    (length _joint_currents)) 4
    ;; float64[] _joint_positions
    (* 8    (length _joint_positions)) 4
    ;; float64[] _joint_speeds
    (* 8    (length _joint_speeds)) 4
    ;; float64[] _joint_pwms
    (* 8    (length _joint_pwms)) 4
    ;; float64[] _joint_temperatures
    (* 8    (length _joint_temperatures)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; string _joint_names
       (write-long (length _joint_names) s) (princ _joint_names s)
     ;; float64[] _joint_currents
     (write-long (length _joint_currents) s)
     (dotimes (i (length _joint_currents))
       (sys::poke (elt _joint_currents i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _joint_positions
     (write-long (length _joint_positions) s)
     (dotimes (i (length _joint_positions))
       (sys::poke (elt _joint_positions i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _joint_speeds
     (write-long (length _joint_speeds) s)
     (dotimes (i (length _joint_speeds))
       (sys::poke (elt _joint_speeds i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _joint_pwms
     (write-long (length _joint_pwms) s)
     (dotimes (i (length _joint_pwms))
       (sys::poke (elt _joint_pwms i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;; float64[] _joint_temperatures
     (write-long (length _joint_temperatures) s)
     (dotimes (i (length _joint_temperatures))
       (sys::poke (elt _joint_temperatures i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; string _joint_names
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _joint_names (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; float64[] _joint_currents
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_currents (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_currents i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _joint_positions
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_positions (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_positions i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _joint_speeds
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_speeds (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_speeds i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _joint_pwms
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_pwms (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_pwms i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;; float64[] _joint_temperatures
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_temperatures (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_temperatures i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get qarm_msgs::AllJointState :md5sum-) "e6bf3c011ce8da2c15205c6fc311e56e")
(setf (get qarm_msgs::AllJointState :datatype-) "qarm_msgs/AllJointState")
(setf (get qarm_msgs::AllJointState :definition-)
      "
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

")



(provide :qarm_msgs/AllJointState "e6bf3c011ce8da2c15205c6fc311e56e")


