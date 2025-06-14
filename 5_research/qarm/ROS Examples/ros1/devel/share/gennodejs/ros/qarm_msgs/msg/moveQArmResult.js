// Auto-generated. Do not edit!

// (in-package qarm_msgs.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;
let QArmActionResult = require('./QArmActionResult.js');

//-----------------------------------------------------------

class moveQArmResult {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.qarm_action_result = null;
    }
    else {
      if (initObj.hasOwnProperty('qarm_action_result')) {
        this.qarm_action_result = initObj.qarm_action_result
      }
      else {
        this.qarm_action_result = new QArmActionResult();
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type moveQArmResult
    // Serialize message field [qarm_action_result]
    bufferOffset = QArmActionResult.serialize(obj.qarm_action_result, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type moveQArmResult
    let len;
    let data = new moveQArmResult(null);
    // Deserialize message field [qarm_action_result]
    data.qarm_action_result = QArmActionResult.deserialize(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    let length = 0;
    length += QArmActionResult.getMessageSize(object.qarm_action_result);
    return length;
  }

  static datatype() {
    // Returns string type for a message object
    return 'qarm_msgs/moveQArmResult';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '4cd8ec53d650973e9e7c5da9f8d65ecb';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    # ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======
    # result
    qarm_msgs/QArmActionResult qarm_action_result
    
    ================================================================================
    MSG: qarm_msgs/QArmActionResult
    Header header
    
    actionlib_msgs/GoalStatus status
    # int32 ready_for_next_goal
    string result
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
    MSG: actionlib_msgs/GoalStatus
    GoalID goal_id
    uint8 status
    uint8 PENDING         = 0   # The goal has yet to be processed by the action server
    uint8 ACTIVE          = 1   # The goal is currently being processed by the action server
    uint8 PREEMPTED       = 2   # The goal received a cancel request after it started executing
                                #   and has since completed its execution (Terminal State)
    uint8 SUCCEEDED       = 3   # The goal was achieved successfully by the action server (Terminal State)
    uint8 ABORTED         = 4   # The goal was aborted during execution by the action server due
                                #    to some failure (Terminal State)
    uint8 REJECTED        = 5   # The goal was rejected by the action server without being processed,
                                #    because the goal was unattainable or invalid (Terminal State)
    uint8 PREEMPTING      = 6   # The goal received a cancel request after it started executing
                                #    and has not yet completed execution
    uint8 RECALLING       = 7   # The goal received a cancel request before it started executing,
                                #    but the action server has not yet confirmed that the goal is canceled
    uint8 RECALLED        = 8   # The goal received a cancel request before it started executing
                                #    and was successfully cancelled (Terminal State)
    uint8 LOST            = 9   # An action client can determine that a goal is LOST. This should not be
                                #    sent over the wire by an action server
    
    #Allow for the user to associate a string with GoalStatus for debugging
    string text
    
    
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
    const resolved = new moveQArmResult(null);
    if (msg.qarm_action_result !== undefined) {
      resolved.qarm_action_result = QArmActionResult.Resolve(msg.qarm_action_result)
    }
    else {
      resolved.qarm_action_result = new QArmActionResult()
    }

    return resolved;
    }
};

module.exports = moveQArmResult;
