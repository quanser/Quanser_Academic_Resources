;; Auto-generated. Do not edit!


(when (boundp 'qarm_msgs::JointCommand)
  (if (not (find-package "QARM_MSGS"))
    (make-package "QARM_MSGS"))
  (shadow 'JointCommand (find-package "QARM_MSGS")))
(unless (find-package "QARM_MSGS::JOINTCOMMAND")
  (make-package "QARM_MSGS::JOINTCOMMAND"))

(in-package "ROS")
;;//! \htmlinclude JointCommand.msg.html


(defclass qarm_msgs::JointCommand
  :super ros::object
  :slots (_joint_command ))

(defmethod qarm_msgs::JointCommand
  (:init
   (&key
    ((:joint_command __joint_command) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _joint_command __joint_command)
   self)
  (:joint_command
   (&optional __joint_command)
   (if __joint_command (setq _joint_command __joint_command)) _joint_command)
  (:serialization-length
   ()
   (+
    ;; float64[] _joint_command
    (* 8    (length _joint_command)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _joint_command
     (write-long (length _joint_command) s)
     (dotimes (i (length _joint_command))
       (sys::poke (elt _joint_command i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _joint_command
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _joint_command (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _joint_command i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get qarm_msgs::JointCommand :md5sum-) "ec5e070dc87da308c7a805432c97fa9c")
(setf (get qarm_msgs::JointCommand :datatype-) "qarm_msgs/JointCommand")
(setf (get qarm_msgs::JointCommand :definition-)
      "
# all values are in rad

float64[] joint_command
")



(provide :qarm_msgs/JointCommand "ec5e070dc87da308c7a805432c97fa9c")


