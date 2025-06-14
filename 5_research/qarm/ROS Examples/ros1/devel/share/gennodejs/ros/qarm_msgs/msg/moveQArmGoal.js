// Auto-generated. Do not edit!

// (in-package qarm_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let QArmActionGoal = require('./QArmActionGoal.js');

//-----------------------------------------------------------

class moveQArmGoal {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.qarm_action_goal = null;
    }
    else {
      if (initObj.hasOwnProperty('qarm_action_goal')) {
        this.qarm_action_goal = initObj.qarm_action_goal
      }
      else {
        this.qarm_action_goal = new QArmActionGoal();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type moveQArmGoal
    // Serialize message field [qarm_action_goal]
    bufferOffset = QArmActionGoal.serialize(obj.qarm_action_goal, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type moveQArmGoal
    let len;
    let data = new moveQArmGoal(null);
    // Deserialize message field [qarm_action_goal]
    data.qarm_action_goal = QArmActionGoal.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += QArmActionGoal.getMessageSize(object.qarm_action_goal);
    return length;
  }

  static datatype() {
    // Returns string type for a message object
    return 'qarm_msgs/moveQArmGoal';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return 'e20b3cc33cfad8c835bf4d09f0f0006e';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
    # goal
    qarm_msgs/QArmActionGoal qarm_action_goal
    
    ================================================================================
    MSG: qarm_msgs/QArmActionGoal
    Header header
    
    actionlib_msgs/GoalID goal_id
    float64[] task_space_position_and_gripper
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
    MSG: actionlib_msgs/GoalID
    # The stamp should store the time at which this goal was requested.
    # It is used by an action server when it tries to preempt all
    # goals that were requested before a certain time
    time stamp
    
    # The id provides a way to associate feedback and
    # result message with specific goal requests. The id
    # specified must be unique.
    string id
    
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new moveQArmGoal(null);
    if (msg.qarm_action_goal !== undefined) {
      resolved.qarm_action_goal = QArmActionGoal.Resolve(msg.qarm_action_goal)
    }
    else {
      resolved.qarm_action_goal = new QArmActionGoal()
    }

    return resolved;
    }
};

module.exports = moveQArmGoal;
