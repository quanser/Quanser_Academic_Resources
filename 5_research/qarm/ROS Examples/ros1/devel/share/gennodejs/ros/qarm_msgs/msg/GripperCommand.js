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

class GripperCommand {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.gripper_command = null;
    }
    else {
      if (initObj.hasOwnProperty('gripper_command')) {
        this.gripper_command = initObj.gripper_command
      }
      else {
        this.gripper_command = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type GripperCommand
    // Serialize message field [gripper_command]
    bufferOffset = _serializer.float64(obj.gripper_command, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type GripperCommand
    let len;
    let data = new GripperCommand(null);
    // Deserialize message field [gripper_command]
    data.gripper_command = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'qarm_msgs/GripperCommand';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'a6ae6f959759a14d8596011d33fb4140';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    # Gripper 0 - 1
    # O is fully open, 1 is fully closed
    
    float64 gripper_command
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new GripperCommand(null);
    if (msg.gripper_command !== undefined) {
      resolved.gripper_command = msg.gripper_command;
    }
    else {
      resolved.gripper_command = 0.0
    }

    return resolved;
    }
};

module.exports = GripperCommand;
