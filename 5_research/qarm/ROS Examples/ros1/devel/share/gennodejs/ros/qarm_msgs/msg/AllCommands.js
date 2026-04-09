// Auto-generated. Do not edit!

// (in-package qarm_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let JointCommand = require('./JointCommand.js');
let GripperCommand = require('./GripperCommand.js');
let LEDCommand = require('./LEDCommand.js');
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class AllCommands {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.jointcommand = null;
      this.grippercommand = null;
      this.ledcommand = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('jointcommand')) {
        this.jointcommand = initObj.jointcommand
      }
      else {
        this.jointcommand = new JointCommand();
      }
      if (initObj.hasOwnProperty('grippercommand')) {
        this.grippercommand = initObj.grippercommand
      }
      else {
        this.grippercommand = new GripperCommand();
      }
      if (initObj.hasOwnProperty('ledcommand')) {
        this.ledcommand = initObj.ledcommand
      }
      else {
        this.ledcommand = new LEDCommand();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type AllCommands
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [jointcommand]
    bufferOffset = JointCommand.serialize(obj.jointcommand, buffer, bufferOffset);
    // Serialize message field [grippercommand]
    bufferOffset = GripperCommand.serialize(obj.grippercommand, buffer, bufferOffset);
    // Serialize message field [ledcommand]
    bufferOffset = LEDCommand.serialize(obj.ledcommand, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type AllCommands
    let len;
    let data = new AllCommands(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [jointcommand]
    data.jointcommand = JointCommand.deserialize(buffer, bufferOffset);
    // Deserialize message field [grippercommand]
    data.grippercommand = GripperCommand.deserialize(buffer, bufferOffset);
    // Deserialize message field [ledcommand]
    data.ledcommand = LEDCommand.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += JointCommand.getMessageSize(object.jointcommand);
    length += LEDCommand.getMessageSize(object.ledcommand);
    return length + 8;
  }

  static datatype() {
    // Returns string type for a message object
    return 'qarm_msgs/AllCommands';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'f0d189c98e3eb187f5c6801c66a284fe';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
    std_msgs/Header header
    
    qarm_msgs/JointCommand jointcommand
    qarm_msgs/GripperCommand grippercommand
    qarm_msgs/LEDCommand ledcommand
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
    
    ================================================================================
    MSG: qarm_msgs/JointCommand
    
    # all values are in rad
    
    float64[] joint_command
    ================================================================================
    MSG: qarm_msgs/GripperCommand
    
    # Gripper 0 - 1
    # O is fully open, 1 is fully closed
    
    float64 gripper_command
    ================================================================================
    MSG: qarm_msgs/LEDCommand
    
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
    const resolved = new AllCommands(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.jointcommand !== undefined) {
      resolved.jointcommand = JointCommand.Resolve(msg.jointcommand)
    }
    else {
      resolved.jointcommand = new JointCommand()
    }

    if (msg.grippercommand !== undefined) {
      resolved.grippercommand = GripperCommand.Resolve(msg.grippercommand)
    }
    else {
      resolved.grippercommand = new GripperCommand()
    }

    if (msg.ledcommand !== undefined) {
      resolved.ledcommand = LEDCommand.Resolve(msg.ledcommand)
    }
    else {
      resolved.ledcommand = new LEDCommand()
    }

    return resolved;
    }
};

module.exports = AllCommands;
