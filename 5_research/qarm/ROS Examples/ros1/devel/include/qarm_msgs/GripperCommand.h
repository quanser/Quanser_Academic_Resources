// Generated by gencpp from file qarm_msgs/GripperCommand.msg
// DO NOT EDIT!


#ifndef QARM_MSGS_MESSAGE_GRIPPERCOMMAND_H
#define QARM_MSGS_MESSAGE_GRIPPERCOMMAND_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace qarm_msgs
{
template <class ContainerAllocator>
struct GripperCommand_
{
  typedef GripperCommand_<ContainerAllocator> Type;

  GripperCommand_()
    : gripper_command(0.0)  {
    }
  GripperCommand_(const ContainerAllocator& _alloc)
    : gripper_command(0.0)  {
  (void)_alloc;
    }



   typedef double _gripper_command_type;
  _gripper_command_type gripper_command;





  typedef boost::shared_ptr< ::qarm_msgs::GripperCommand_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::qarm_msgs::GripperCommand_<ContainerAllocator> const> ConstPtr;

}; // struct GripperCommand_

typedef ::qarm_msgs::GripperCommand_<std::allocator<void> > GripperCommand;

typedef boost::shared_ptr< ::qarm_msgs::GripperCommand > GripperCommandPtr;
typedef boost::shared_ptr< ::qarm_msgs::GripperCommand const> GripperCommandConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::qarm_msgs::GripperCommand_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::qarm_msgs::GripperCommand_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::qarm_msgs::GripperCommand_<ContainerAllocator1> & lhs, const ::qarm_msgs::GripperCommand_<ContainerAllocator2> & rhs)
{
  return lhs.gripper_command == rhs.gripper_command;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::qarm_msgs::GripperCommand_<ContainerAllocator1> & lhs, const ::qarm_msgs::GripperCommand_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace qarm_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::qarm_msgs::GripperCommand_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::qarm_msgs::GripperCommand_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::qarm_msgs::GripperCommand_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::qarm_msgs::GripperCommand_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::qarm_msgs::GripperCommand_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::qarm_msgs::GripperCommand_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::qarm_msgs::GripperCommand_<ContainerAllocator> >
{
  static const char* value()
  {
    return "a6ae6f959759a14d8596011d33fb4140";
  }

  static const char* value(const ::qarm_msgs::GripperCommand_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xa6ae6f959759a14dULL;
  static const uint64_t static_value2 = 0x8596011d33fb4140ULL;
};

template<class ContainerAllocator>
struct DataType< ::qarm_msgs::GripperCommand_<ContainerAllocator> >
{
  static const char* value()
  {
    return "qarm_msgs/GripperCommand";
  }

  static const char* value(const ::qarm_msgs::GripperCommand_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::qarm_msgs::GripperCommand_<ContainerAllocator> >
{
  static const char* value()
  {
    return "\n"
"# Gripper 0 - 1\n"
"# O is fully open, 1 is fully closed\n"
"\n"
"float64 gripper_command\n"
;
  }

  static const char* value(const ::qarm_msgs::GripperCommand_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::qarm_msgs::GripperCommand_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.gripper_command);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GripperCommand_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::qarm_msgs::GripperCommand_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::qarm_msgs::GripperCommand_<ContainerAllocator>& v)
  {
    s << indent << "gripper_command: ";
    Printer<double>::stream(s, indent + "  ", v.gripper_command);
  }
};

} // namespace message_operations
} // namespace ros

#endif // QARM_MSGS_MESSAGE_GRIPPERCOMMAND_H
