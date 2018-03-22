// Generated by gencpp from file dynamixel_workbench_msgs/GetDynamixelInfoResponse.msg
// DO NOT EDIT!


#ifndef DYNAMIXEL_WORKBENCH_MSGS_MESSAGE_GETDYNAMIXELINFORESPONSE_H
#define DYNAMIXEL_WORKBENCH_MSGS_MESSAGE_GETDYNAMIXELINFORESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <dynamixel_workbench_msgs/DynamixelInfo.h>

namespace dynamixel_workbench_msgs
{
template <class ContainerAllocator>
struct GetDynamixelInfoResponse_
{
  typedef GetDynamixelInfoResponse_<ContainerAllocator> Type;

  GetDynamixelInfoResponse_()
    : dynamixel_info()  {
    }
  GetDynamixelInfoResponse_(const ContainerAllocator& _alloc)
    : dynamixel_info(_alloc)  {
  (void)_alloc;
    }



   typedef  ::dynamixel_workbench_msgs::DynamixelInfo_<ContainerAllocator>  _dynamixel_info_type;
  _dynamixel_info_type dynamixel_info;




  typedef boost::shared_ptr< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> const> ConstPtr;

}; // struct GetDynamixelInfoResponse_

typedef ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<std::allocator<void> > GetDynamixelInfoResponse;

typedef boost::shared_ptr< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse > GetDynamixelInfoResponsePtr;
typedef boost::shared_ptr< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse const> GetDynamixelInfoResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> >::stream(s, "", v);
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
struct IsFixedSize< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "5075be00278efc6e6ba91f48b43afb53";
  }

  static const char* value(const ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x5075be00278efc6eULL;
  static const uint64_t static_value2 = 0x6ba91f48b43afb53ULL;
};

template<class ContainerAllocator>
struct DataType< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "dynamixel_workbench_msgs/GetDynamixelInfoResponse";
  }

  static const char* value(const ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "\n\
DynamixelInfo dynamixel_info\n\
\n\
\n\
================================================================================\n\
MSG: dynamixel_workbench_msgs/DynamixelInfo\n\
# This message includes information of dynamixel's basic parameter\n\
\n\
DynamixelLoadInfo load_info\n\
\n\
string model_name\n\
uint16 model_number\n\
uint8 model_id\n\
\n\
\n\
================================================================================\n\
MSG: dynamixel_workbench_msgs/DynamixelLoadInfo\n\
# This message includes dynamixel's load information\n\
\n\
string device_name\n\
uint64 baud_rate\n\
float32 protocol_version\n\
";
  }

  static const char* value(const ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.dynamixel_info);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GetDynamixelInfoResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::dynamixel_workbench_msgs::GetDynamixelInfoResponse_<ContainerAllocator>& v)
  {
    s << indent << "dynamixel_info: ";
    s << std::endl;
    Printer< ::dynamixel_workbench_msgs::DynamixelInfo_<ContainerAllocator> >::stream(s, indent + "  ", v.dynamixel_info);
  }
};

} // namespace message_operations
} // namespace ros

#endif // DYNAMIXEL_WORKBENCH_MSGS_MESSAGE_GETDYNAMIXELINFORESPONSE_H
