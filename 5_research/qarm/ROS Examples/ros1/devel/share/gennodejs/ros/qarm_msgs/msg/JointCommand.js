// Auto-generated. Do not edit!

// (in-package qarm_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class JointCommand {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.joint_command = null;
    }
    else {
      if (initObj.hasOwnProperty('joint_command')) {
        this.joint_command = initObj.joint_command
      }
      else {
        this.joint_command = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type JointCommand
    // Serialize message field [joint_command]
    bufferOffset = _arraySerializer.float64(obj.joint_command, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type JointCommand
    let len;
    let data = new JointCommand(null);
    // Deserialize message field [joint_command]
    data.joint_command = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.joint_command.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'qarm_msgs/JointCommand';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'ec5e070dc87da308c7a805432c97fa9c';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    # all values are in rad
    
    float64[] joint_command
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new JointCommand(null);
    if (msg.joint_command !== undefined) {
      resolved.joint_command = msg.joint_command;
    }
    else {
      resolved.joint_command = []
    }

    return resolved;
    }
};

module.exports = JointCommand;
