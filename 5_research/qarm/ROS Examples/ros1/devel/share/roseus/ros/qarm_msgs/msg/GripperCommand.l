;; Auto-generated. Do not edit!


(when (boundp 'qarm_msgs::GripperCommand)
  (if (not (find-package "QARM_MSGS"))
    (make-package "QARM_MSGS"))
  (shadow 'GripperCommand (find-package "QARM_MSGS")))
(unless (find-package "QARM_MSGS::GRIPPERCOMMAND")
  (make-package "QARM_MSGS::GRIPPERCOMMAND"))

(in-package "ROS")
;;//! \htmlinclude GripperCommand.msg.html


(defclass qarm_msgs::GripperCommand
  :super ros::object
  :slots (_gripper_command ))

(defmethod qarm_msgs::GripperCommand
  (:init
   (&key
    ((:gripper_command __gripper_command) 0.0)
    )
   (send-super :init)
   (setq _gripper_command (float __gripper_command))
   self)
  (:gripper_command
   (&optional __gripper_command)
   (if __gripper_command (setq _gripper_command __gripper_command)) _gripper_command)
  (:serialization-length
   ()
   (+
    ;; float64 _gripper_command
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _gripper_command
       (sys::poke _gripper_command (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _gripper_command
     (setq _gripper_command (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get qarm_msgs::GripperCommand :md5sum-) "a6ae6f959759a14d8596011d33fb4140")
(setf (get qarm_msgs::GripperCommand :datatype-) "qarm_msgs/GripperCommand")
(setf (get qarm_msgs::GripperCommand :definition-)
      "
# Gripper 0 - 1
# O is fully open, 1 is fully closed

float64 gripper_command
")



(provide :qarm_msgs/GripperCommand "a6ae6f959759a14d8596011d33fb4140")


