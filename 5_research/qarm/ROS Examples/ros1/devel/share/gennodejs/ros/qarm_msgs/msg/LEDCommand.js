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

class LEDCommand {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.RGB = null;
    }
    else {
      if (initObj.hasOwnProperty('RGB')) {
        this.RGB = initObj.RGB
      }
      else {
        this.RGB = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type LEDCommand
    // Serialize message field [RGB]
    bufferOffset = _arraySerializer.float64(obj.RGB, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type LEDCommand
    let len;
    let data = new LEDCommand(null);
    // Deserialize message field [RGB]
    data.RGB = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += 8 * object.RGB.length;
    return length + 4;
  }

  static datatype() {
    // Returns string type for a message object
    return 'qarm_msgs/LEDCommand';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f723af9a2be20e93588f85bf623cd8b4';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    # RGB values are scaled from 0 - 255 to 0 - 1 in this msg
    # so 0 is 0, 1 is 255, 0.5 is 127, etc
    # It should be an arrary of three elements like [1, 0, 0]
    
    float64[] RGB
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new LEDCommand(null);
    if (msg.RGB !== undefined) {
      resolved.RGB = msg.RGB;
    }
    else {
      resolved.RGB = []
    }

    return resolved;
    }
};

module.exports = LEDCommand;
