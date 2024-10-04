// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from armpi_interfaces:msg/PositionWithAngle.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "armpi_interfaces/msg/detail/position_with_angle__functions.h"
#include "armpi_interfaces/msg/detail/position_with_angle__struct.hpp"
#include "rosidl_typesupport_introspection_cpp/field_types.hpp"
#include "rosidl_typesupport_introspection_cpp/identifier.hpp"
#include "rosidl_typesupport_introspection_cpp/message_introspection.hpp"
#include "rosidl_typesupport_introspection_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_introspection_cpp/visibility_control.h"

namespace armpi_interfaces
{

namespace msg
{

namespace rosidl_typesupport_introspection_cpp
{

void PositionWithAngle_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) armpi_interfaces::msg::PositionWithAngle(_init);
}

void PositionWithAngle_fini_function(void * message_memory)
{
  auto typed_message = static_cast<armpi_interfaces::msg::PositionWithAngle *>(message_memory);
  typed_message->~PositionWithAngle();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember PositionWithAngle_message_member_array[5] = {
  {
    "id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces::msg::PositionWithAngle, id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "x",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces::msg::PositionWithAngle, x),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "y",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces::msg::PositionWithAngle, y),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "z",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces::msg::PositionWithAngle, z),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "angle",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces::msg::PositionWithAngle, angle),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers PositionWithAngle_message_members = {
  "armpi_interfaces::msg",  // message namespace
  "PositionWithAngle",  // message name
  5,  // number of fields
  sizeof(armpi_interfaces::msg::PositionWithAngle),
  false,  // has_any_key_member_
  PositionWithAngle_message_member_array,  // message members
  PositionWithAngle_init_function,  // function to initialize message memory (memory has to be allocated)
  PositionWithAngle_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t PositionWithAngle_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &PositionWithAngle_message_members,
  get_message_typesupport_handle_function,
  &armpi_interfaces__msg__PositionWithAngle__get_type_hash,
  &armpi_interfaces__msg__PositionWithAngle__get_type_description,
  &armpi_interfaces__msg__PositionWithAngle__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace armpi_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<armpi_interfaces::msg::PositionWithAngle>()
{
  return &::armpi_interfaces::msg::rosidl_typesupport_introspection_cpp::PositionWithAngle_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, armpi_interfaces, msg, PositionWithAngle)() {
  return &::armpi_interfaces::msg::rosidl_typesupport_introspection_cpp::PositionWithAngle_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
