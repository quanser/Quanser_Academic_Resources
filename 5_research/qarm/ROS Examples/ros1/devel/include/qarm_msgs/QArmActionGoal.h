// Generated by gencpp from file qarm_msgs/QArmActionGoal.msg
// DO NOT EDIT!


#ifndef QARM_MSGS_MESSAGE_QARMACTIONGOAL_H
#define QARM_MSGS_MESSAGE_QARMACTIONGOAL_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <std_msgs/Header.h>
#include <actionlib_msgs/GoalID.h>

namespace qarm_msgs
{
template <class ContainerAllocator>
struct QArmActionGoal_
{
  typedef QArmActionGoal_<ContainerAllocator> Type;

  QArmActionGoal_()
    : header()
    , goal_id()
    , task_space_position_and_gripper()  {
    }
  QArmActionGoal_(const ContainerAllocator& _alloc)
    : header(_alloc)
    , goal_id(_alloc)
    , task_space_position_and_gripper(_alloc)  {
  (void)_alloc;
    }



   typedef  ::std_msgs::Header_<ContainerAllocator>  _header_type;
  _header_type header;

   typedef  ::actionlib_msgs::GoalID_<ContainerAllocator>  _goal_id_type;
  _goal_id_type goal_id;

   typedef std::vector<double, typename ContainerAllocator::template rebind<double>::other >  _task_space_position_and_gripper_type;
  _task_space_position_and_gripper_type task_space_position_and_gripper;





  typedef boost::shared_ptr< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> const> ConstPtr;

}; // struct QArmActionGoal_

typedef ::qarm_msgs::QArmActionGoal_<std::allocator<void> > QArmActionGoal;

typedef boost::shared_ptr< ::qarm_msgs::QArmActionGoal > QArmActionGoalPtr;
typedef boost::shared_ptr< ::qarm_msgs::QArmActionGoal const> QArmActionGoalConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::qarm_msgs::QArmActionGoal_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::qarm_msgs::QArmActionGoal_<ContainerAllocator1> & lhs, const ::qarm_msgs::QArmActionGoal_<ContainerAllocator2> & rhs)
{
  return lhs.header == rhs.header &&
    lhs.goal_id == rhs.goal_id &&
    lhs.task_space_position_and_gripper == rhs.task_space_position_and_gripper;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::qarm_msgs::QArmActionGoal_<ContainerAllocator1> & lhs, const ::qarm_msgs::QArmActionGoal_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace qarm_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> const>
  : TrueType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "8b2615bf7d9cbd023ac805bbdd42fa97";
  }

  static const char* value(const ::qarm_msgs::QArmActionGoal_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x8b2615bf7d9cbd02ULL;
  static const uint64_t static_value2 = 0x3ac805bbdd42fa97ULL;
};

template<class ContainerAllocator>
struct DataType< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "qarm_msgs/QArmActionGoal";
  }

  static const char* value(const ::qarm_msgs::QArmActionGoal_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "Header header\n"
"\n"
"actionlib_msgs/GoalID goal_id\n"
"float64[] task_space_position_and_gripper\n"
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
;
  }

  static const char* value(const ::qarm_msgs::QArmActionGoal_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.header);
      stream.next(m.goal_id);
      stream.next(m.task_space_position_and_gripper);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct QArmActionGoal_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::qarm_msgs::QArmActionGoal_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::qarm_msgs::QArmActionGoal_<ContainerAllocator>& v)
  {
    s << indent << "header: ";
    s << std::endl;
    Printer< ::std_msgs::Header_<ContainerAllocator> >::stream(s, indent + "  ", v.header);
    s << indent << "goal_id: ";
    s << std::endl;
    Printer< ::actionlib_msgs::GoalID_<ContainerAllocator> >::stream(s, indent + "  ", v.goal_id);
    s << indent << "task_space_position_and_gripper[]" << std::endl;
    for (size_t i = 0; i < v.task_space_position_and_gripper.size(); ++i)
    {
      s << indent << "  task_space_position_and_gripper[" << i << "]: ";
      Printer<double>::stream(s, indent + "  ", v.task_space_position_and_gripper[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // QARM_MSGS_MESSAGE_QARMACTIONGOAL_H
