;; Auto-generated. Do not edit!


(when (boundp 'qarm_msgs::LEDCommand)
  (if (not (find-package "QARM_MSGS"))
    (make-package "QARM_MSGS"))
  (shadow 'LEDCommand (find-package "QARM_MSGS")))
(unless (find-package "QARM_MSGS::LEDCOMMAND")
  (make-package "QARM_MSGS::LEDCOMMAND"))

(in-package "ROS")
;;//! \htmlinclude LEDCommand.msg.html


(defclass qarm_msgs::LEDCommand
  :super ros::object
  :slots (_RGB ))

(defmethod qarm_msgs::LEDCommand
  (:init
   (&key
    ((:RGB __RGB) (make-array 0 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _RGB __RGB)
   self)
  (:RGB
   (&optional __RGB)
   (if __RGB (setq _RGB __RGB)) _RGB)
  (:serialization-length
   ()
   (+
    ;; float64[] _RGB
    (* 8    (length _RGB)) 4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64[] _RGB
     (write-long (length _RGB) s)
     (dotimes (i (length _RGB))
       (sys::poke (elt _RGB i) (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64[] _RGB
   (let (n)
     (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4)
     (setq _RGB (instantiate float-vector n))
     (dotimes (i n)
     (setf (elt _RGB i) (sys::peek buf ptr- :double)) (incf ptr- 8)
     ))
   ;;
   self)
  )

(setf (get qarm_msgs::LEDCommand :md5sum-) "f723af9a2be20e93588f85bf623cd8b4")
(setf (get qarm_msgs::LEDCommand :datatype-) "qarm_msgs/LEDCommand")
(setf (get qarm_msgs::LEDCommand :definition-)
      "
# RGB values are scaled from 0 - 255 to 0 - 1 in this msg
# so 0 is 0, 1 is 255, 0.5 is 127, etc
# It should be an arrary of three elements like [1, 0, 0]

float64[] RGB
")



(provide :qarm_msgs/LEDCommand "f723af9a2be20e93588f85bf623cd8b4")


