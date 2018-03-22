; Auto-generated. Do not edit!


(cl:in-package open_manipulator_msgs-srv)


;//! \htmlinclude GetJointPose-request.msg.html

(cl:defclass <GetJointPose-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass GetJointPose-request (<GetJointPose-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetJointPose-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetJointPose-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name open_manipulator_msgs-srv:<GetJointPose-request> is deprecated: use open_manipulator_msgs-srv:GetJointPose-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetJointPose-request>) ostream)
  "Serializes a message object of type '<GetJointPose-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetJointPose-request>) istream)
  "Deserializes a message object of type '<GetJointPose-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetJointPose-request>)))
  "Returns string type for a service object of type '<GetJointPose-request>"
  "open_manipulator_msgs/GetJointPoseRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointPose-request)))
  "Returns string type for a service object of type 'GetJointPose-request"
  "open_manipulator_msgs/GetJointPoseRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetJointPose-request>)))
  "Returns md5sum for a message object of type '<GetJointPose-request>"
  "7204b88d723dcb9dffcbfeacbf4044c2")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetJointPose-request)))
  "Returns md5sum for a message object of type 'GetJointPose-request"
  "7204b88d723dcb9dffcbfeacbf4044c2")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetJointPose-request>)))
  "Returns full string definition for message of type '<GetJointPose-request>"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetJointPose-request)))
  "Returns full string definition for message of type 'GetJointPose-request"
  (cl:format cl:nil "~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetJointPose-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetJointPose-request>))
  "Converts a ROS message object to a list"
  (cl:list 'GetJointPose-request
))
;//! \htmlinclude GetJointPose-response.msg.html

(cl:defclass <GetJointPose-response> (roslisp-msg-protocol:ros-message)
  ((position_ctrl_joint_pos
    :reader position_ctrl_joint_pos
    :initarg :position_ctrl_joint_pos
    :type open_manipulator_msgs-msg:JointPose
    :initform (cl:make-instance 'open_manipulator_msgs-msg:JointPose)))
)

(cl:defclass GetJointPose-response (<GetJointPose-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <GetJointPose-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'GetJointPose-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name open_manipulator_msgs-srv:<GetJointPose-response> is deprecated: use open_manipulator_msgs-srv:GetJointPose-response instead.")))

(cl:ensure-generic-function 'position_ctrl_joint_pos-val :lambda-list '(m))
(cl:defmethod position_ctrl_joint_pos-val ((m <GetJointPose-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader open_manipulator_msgs-srv:position_ctrl_joint_pos-val is deprecated.  Use open_manipulator_msgs-srv:position_ctrl_joint_pos instead.")
  (position_ctrl_joint_pos m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <GetJointPose-response>) ostream)
  "Serializes a message object of type '<GetJointPose-response>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'position_ctrl_joint_pos) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <GetJointPose-response>) istream)
  "Deserializes a message object of type '<GetJointPose-response>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'position_ctrl_joint_pos) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<GetJointPose-response>)))
  "Returns string type for a service object of type '<GetJointPose-response>"
  "open_manipulator_msgs/GetJointPoseResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointPose-response)))
  "Returns string type for a service object of type 'GetJointPose-response"
  "open_manipulator_msgs/GetJointPoseResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<GetJointPose-response>)))
  "Returns md5sum for a message object of type '<GetJointPose-response>"
  "7204b88d723dcb9dffcbfeacbf4044c2")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'GetJointPose-response)))
  "Returns md5sum for a message object of type 'GetJointPose-response"
  "7204b88d723dcb9dffcbfeacbf4044c2")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<GetJointPose-response>)))
  "Returns full string definition for message of type '<GetJointPose-response>"
  (cl:format cl:nil "JointPose position_ctrl_joint_pos~%~%~%================================================================================~%MSG: open_manipulator_msgs/JointPose~%string[]   joint_name~%float64[]  position~%float64    move_time~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'GetJointPose-response)))
  "Returns full string definition for message of type 'GetJointPose-response"
  (cl:format cl:nil "JointPose position_ctrl_joint_pos~%~%~%================================================================================~%MSG: open_manipulator_msgs/JointPose~%string[]   joint_name~%float64[]  position~%float64    move_time~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <GetJointPose-response>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'position_ctrl_joint_pos))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <GetJointPose-response>))
  "Converts a ROS message object to a list"
  (cl:list 'GetJointPose-response
    (cl:cons ':position_ctrl_joint_pos (position_ctrl_joint_pos msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'GetJointPose)))
  'GetJointPose-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'GetJointPose)))
  'GetJointPose-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'GetJointPose)))
  "Returns string type for a service object of type '<GetJointPose>"
  "open_manipulator_msgs/GetJointPose")