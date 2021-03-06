// Auto-generated. Do not edit!

// (in-package open_manipulator_msgs.srv)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

let JointPose = require('../msg/JointPose.js');

//-----------------------------------------------------------

class GetJointPoseRequest {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
    }
    else {
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetJointPoseRequest
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetJointPoseRequest
    let len;
    let data = new GetJointPoseRequest(null);
    return data;
  }

  static getMessageSize(object) {
    return 0;
  }

  static datatype() {
    // Returns string type for a service object
    return 'open_manipulator_msgs/GetJointPoseRequest';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'd41d8cd98f00b204e9800998ecf8427e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetJointPoseRequest(null);
    return resolved;
    }
};

class GetJointPoseResponse {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.position_ctrl_joint_pos = null;
    }
    else {
      if (initObj.hasOwnProperty('position_ctrl_joint_pos')) {
        this.position_ctrl_joint_pos = initObj.position_ctrl_joint_pos
      }
      else {
        this.position_ctrl_joint_pos = new JointPose();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GetJointPoseResponse
    // Serialize message field [position_ctrl_joint_pos]
    bufferOffset = JointPose.serialize(obj.position_ctrl_joint_pos, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GetJointPoseResponse
    let len;
    let data = new GetJointPoseResponse(null);
    // Deserialize message field [position_ctrl_joint_pos]
    data.position_ctrl_joint_pos = JointPose.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += JointPose.getMessageSize(object.position_ctrl_joint_pos);
    return length;
  }

  static datatype() {
    // Returns string type for a service object
    return 'open_manipulator_msgs/GetJointPoseResponse';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '7204b88d723dcb9dffcbfeacbf4044c2';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    JointPose position_ctrl_joint_pos
    
    
    ================================================================================
    MSG: open_manipulator_msgs/JointPose
    string[]   joint_name
    float64[]  position
    float64    move_time
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GetJointPoseResponse(null);
    if (msg.position_ctrl_joint_pos !== undefined) {
      resolved.position_ctrl_joint_pos = JointPose.Resolve(msg.position_ctrl_joint_pos)
    }
    else {
      resolved.position_ctrl_joint_pos = new JointPose()
    }

    return resolved;
    }
};

module.exports = {
  Request: GetJointPoseRequest,
  Response: GetJointPoseResponse,
  md5sum() { return '7204b88d723dcb9dffcbfeacbf4044c2'; },
  datatype() { return 'open_manipulator_msgs/GetJointPose'; }
};
