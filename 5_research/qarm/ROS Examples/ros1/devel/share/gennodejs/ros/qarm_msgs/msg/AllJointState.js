// Auto-generated. Do not edit!

// (in-package qarm_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let std_msgs = _finder('std_msgs');

//-----------------------------------------------------------

class AllJointState {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.header = null;
      this.joint_names = null;
      this.joint_currents = null;
      this.joint_positions = null;
      this.joint_speeds = null;
      this.joint_pwms = null;
      this.joint_temperatures = null;
    }
    else {
      if (initObj.hasOwnProperty('header')) {
        this.header = initObj.header
      }
      else {
        this.header = new std_msgs.msg.Header();
      }
      if (initObj.hasOwnProperty('joint_names')) {
        this.joint_names = initObj.joint_names
      }
      else {
        this.joint_names = '';
      }
      if (initObj.hasOwnProperty('joint_currents')) {
        this.joint_currents = initObj.joint_currents
      }
      else {
        this.joint_currents = [];
      }
      if (initObj.hasOwnProperty('joint_positions')) {
        this.joint_positions = initObj.joint_positions
      }
      else {
        this.joint_positions = [];
      }
      if (initObj.hasOwnProperty('joint_speeds')) {
        this.joint_speeds = initObj.joint_speeds
      }
      else {
        this.joint_speeds = [];
      }
      if (initObj.hasOwnProperty('joint_pwms')) {
        this.joint_pwms = initObj.joint_pwms
      }
      else {
        this.joint_pwms = [];
      }
      if (initObj.hasOwnProperty('joint_temperatures')) {
        this.joint_temperatures = initObj.joint_temperatures
      }
      else {
        this.joint_temperatures = [];
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type AllJointState
    // Serialize message field [header]
    bufferOffset = std_msgs.msg.Header.serialize(obj.header, buffer, bufferOffset);
    // Serialize message field [joint_names]
    bufferOffset = _serializer.string(obj.joint_names, buffer, bufferOffset);
    // Serialize message field [joint_currents]
    bufferOffset = _arraySerializer.float64(obj.joint_currents, buffer, bufferOffset, null);
    // Serialize message field [joint_positions]
    bufferOffset = _arraySerializer.float64(obj.joint_positions, buffer, bufferOffset, null);
    // Serialize message field [joint_speeds]
    bufferOffset = _arraySerializer.float64(obj.joint_speeds, buffer, bufferOffset, null);
    // Serialize message field [joint_pwms]
    bufferOffset = _arraySerializer.float64(obj.joint_pwms, buffer, bufferOffset, null);
    // Serialize message field [joint_temperatures]
    bufferOffset = _arraySerializer.float64(obj.joint_temperatures, buffer, bufferOffset, null);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type AllJointState
    let len;
    let data = new AllJointState(null);
    // Deserialize message field [header]
    data.header = std_msgs.msg.Header.deserialize(buffer, bufferOffset);
    // Deserialize message field [joint_names]
    data.joint_names = _deserializer.string(buffer, bufferOffset);
    // Deserialize message field [joint_currents]
    data.joint_currents = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [joint_positions]
    data.joint_positions = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [joint_speeds]
    data.joint_speeds = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [joint_pwms]
    data.joint_pwms = _arrayDeserializer.float64(buffer, bufferOffset, null)
    // Deserialize message field [joint_temperatures]
    data.joint_temperatures = _arrayDeserializer.float64(buffer, bufferOffset, null)
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += std_msgs.msg.Header.getMessageSize(object.header);
    length += object.joint_names.length;
    length += 8 * object.joint_currents.length;
    length += 8 * object.joint_positions.length;
    length += 8 * object.joint_speeds.length;
    length += 8 * object.joint_pwms.length;
    length += 8 * object.joint_temperatures.length;
    return length + 24;
  }

  static datatype() {
    // Returns string type for a message object
    return 'qarm_msgs/AllJointState';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e6bf3c011ce8da2c15205c6fc311e56e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    
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
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new AllJointState(null);
    if (msg.header !== undefined) {
      resolved.header = std_msgs.msg.Header.Resolve(msg.header)
    }
    else {
      resolved.header = new std_msgs.msg.Header()
    }

    if (msg.joint_names !== undefined) {
      resolved.joint_names = msg.joint_names;
    }
    else {
      resolved.joint_names = ''
    }

    if (msg.joint_currents !== undefined) {
      resolved.joint_currents = msg.joint_currents;
    }
    else {
      resolved.joint_currents = []
    }

    if (msg.joint_positions !== undefined) {
      resolved.joint_positions = msg.joint_positions;
    }
    else {
      resolved.joint_positions = []
    }

    if (msg.joint_speeds !== undefined) {
      resolved.joint_speeds = msg.joint_speeds;
    }
    else {
      resolved.joint_speeds = []
    }

    if (msg.joint_pwms !== undefined) {
      resolved.joint_pwms = msg.joint_pwms;
    }
    else {
      resolved.joint_pwms = []
    }

    if (msg.joint_temperatures !== undefined) {
      resolved.joint_temperatures = msg.joint_temperatures;
    }
    else {
      resolved.joint_temperatures = []
    }

    return resolved;
    }
};

module.exports = AllJointState;
