// Generated by gencpp from file qarm_msgs/moveQArmFeedback.msg
// DO NOT EDIT!


#ifndef QARM_MSGS_MESSAGE_MOVEQARMFEEDBACK_H
#define QARM_MSGS_MESSAGE_MOVEQARMFEEDBACK_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <qarm_msgs/QArmActionFeedback.h>

namespace qarm_msgs
{
template <class ContainerAllocator>
struct moveQArmFeedback_
{
  typedef moveQArmFeedback_<ContainerAllocator> Type;

  moveQArmFeedback_()
    : qarm_action_feedback()  {
    }
  moveQArmFeedback_(const ContainerAllocator& _alloc)
    : qarm_action_feedback(_alloc)  {
  (void)_alloc;
    }



   typedef  ::qarm_msgs::QArmActionFeedback_<ContainerAllocator>  _qarm_action_feedback_type;
  _qarm_action_feedback_type qarm_action_feedback;





  typedef boost::shared_ptr< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> const> ConstPtr;

}; // struct moveQArmFeedback_

typedef ::qarm_msgs::moveQArmFeedback_<std::allocator<void> > moveQArmFeedback;

typedef boost::shared_ptr< ::qarm_msgs::moveQArmFeedback > moveQArmFeedbackPtr;
typedef boost::shared_ptr< ::qarm_msgs::moveQArmFeedback const> moveQArmFeedbackConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::qarm_msgs::moveQArmFeedback_<ContainerAllocator1> & lhs, const ::qarm_msgs::moveQArmFeedback_<ContainerAllocator2> & rhs)
{
  return lhs.qarm_action_feedback == rhs.qarm_action_feedback;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::qarm_msgs::moveQArmFeedback_<ContainerAllocator1> & lhs, const ::qarm_msgs::moveQArmFeedback_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace qarm_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "7e69a7e80ecd0036ac9e7999a607b129";
  }

  static const char* value(const ::qarm_msgs::moveQArmFeedback_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x7e69a7e80ecd0036ULL;
  static const uint64_t static_value2 = 0xac9e7999a607b129ULL;
};

template<class ContainerAllocator>
struct DataType< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "qarm_msgs/moveQArmFeedback";
  }

  static const char* value(const ::qarm_msgs::moveQArmFeedback_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"# feedback\n"
"qarm_msgs/QArmActionFeedback qarm_action_feedback\n"
"\n"
"================================================================================\n"
"MSG: qarm_msgs/QArmActionFeedback\n"
"Header header\n"
"\n"
"actionlib_msgs/GoalID goal_id\n"
"qarm_msgs/AllJointState ajs\n"
"================================================================================\n"
"MSG: std_msgs/Header\n"
"# Standard metadata for higher-level stamped data types.\n"
"# This is generally used to communicate timestamped data \n"
"# in a particular coordinate frame.\n"
"# \n"
"# sequence ID: consecutively increasing ID \n"
"uint32 seq\n"
"#Two-integer timestamp that is expressed as:\n"
"# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')\n"
"# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')\n"
"# time-handling sugar is provided by the client library\n"
"time stamp\n"
"#Frame this data is associated with\n"
"string frame_id\n"
"\n"
"================================================================================\n"
"MSG: actionlib_msgs/GoalID\n"
"# The stamp should store the time at which this goal was requested.\n"
"# It is used by an action server when it tries to preempt all\n"
"# goals that were requested before a certain time\n"
"time stamp\n"
"\n"
"# The id provides a way to associate feedback and\n"
"# result message with specific goal requests. The id\n"
"# specified must be unique.\n"
"string id\n"
"\n"
"\n"
"================================================================================\n"
"MSG: qarm_msgs/AllJointState\n"
"\n"
"std_msgs/Header header\n"
"\n"
"# Name\n"
"string joint_names\n"
"\n"
"# JointCurrent\n"
"float64[] joint_currents\n"
"\n"
"# JointPosition (rad)\n"
"float64[] joint_positions\n"
"\n"
"# JointSpeed (rad/s)\n"
"float64[] joint_speeds\n"
"\n"
"# JointPWM\n"
"float64[] joint_pwms\n"
"\n"
"# JointTemperature\n"
"float64[] joint_temperatures\n"
;
  }

  static const char* value(const ::qarm_msgs::moveQArmFeedback_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.qarm_action_feedback);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct moveQArmFeedback_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::qarm_msgs::moveQArmFeedback_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::qarm_msgs::moveQArmFeedback_<ContainerAllocator>& v)
  {
    s << indent << "qarm_action_feedback: ";
    s << std::endl;
    Printer< ::qarm_msgs::QArmActionFeedback_<ContainerAllocator> >::stream(s, indent + "  ", v.qarm_action_feedback);
  }
};

} // namespace message_operations
} // namespace ros

#endif // QARM_MSGS_MESSAGE_MOVEQARMFEEDBACK_H
