// Generated by gencpp from file dynamixel_workbench_msgs/JointCommandRequest.msg
// DO NOT EDIT!


#ifndef DYNAMIXEL_WORKBENCH_MSGS_MESSAGE_JOINTCOMMANDREQUEST_H
#define DYNAMIXEL_WORKBENCH_MSGS_MESSAGE_JOINTCOMMANDREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace dynamixel_workbench_msgs
{
template <class ContainerAllocator>
struct JointCommandRequest_
{
  typedef JointCommandRequest_<ContainerAllocator> Type;

  JointCommandRequest_()
    : unit()
    , id(0)
    , goal_position(0.0)  {
    }
  JointCommandRequest_(const ContainerAllocator& _alloc)
    : unit(_alloc)
    , id(0)
    , goal_position(0.0)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _unit_type;
  _unit_type unit;

   typedef uint8_t _id_type;
  _id_type id;

   typedef float _goal_position_type;
  _goal_position_type goal_position;




  typedef boost::shared_ptr< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> const> ConstPtr;

}; // struct JointCommandRequest_

typedef ::dynamixel_workbench_msgs::JointCommandRequest_<std::allocator<void> > JointCommandRequest;

typedef boost::shared_ptr< ::dynamixel_workbench_msgs::JointCommandRequest > JointCommandRequestPtr;
typedef boost::shared_ptr< ::dynamixel_workbench_msgs::JointCommandRequest const> JointCommandRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace dynamixel_workbench_msgs

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'std_msgs': ['/opt/ros/kinetic/share/std_msgs/cmake/../msg'], 'dynamixel_workbench_msgs': ['/home/rasmus/catkin_ws/src/dynamixel-workbench-msgs/dynamixel_workbench_msgs/msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "77a5bbe566163c061339dcfde205a47d";
  }

  static const char* value(const ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x77a5bbe566163c06ULL;
  static const uint64_t static_value2 = 0x1339dcfde205a47dULL;
};

template<class ContainerAllocator>
struct DataType< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "dynamixel_workbench_msgs/JointCommandRequest";
  }

  static const char* value(const ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "\n\
\n\
string unit\n\
uint8 id\n\
float32 goal_position\n\
";
  }

  static const char* value(const ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.unit);
      stream.next(m.id);
      stream.next(m.goal_position);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct JointCommandRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::dynamixel_workbench_msgs::JointCommandRequest_<ContainerAllocator>& v)
  {
    s << indent << "unit: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.unit);
    s << indent << "id: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.id);
    s << indent << "goal_position: ";
    Printer<float>::stream(s, indent + "  ", v.goal_position);
  }
};

} // namespace message_operations
} // namespace ros

#endif // DYNAMIXEL_WORKBENCH_MSGS_MESSAGE_JOINTCOMMANDREQUEST_H
