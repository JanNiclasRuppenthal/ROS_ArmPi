// generated from rosidl_typesupport_introspection_cpp/resource/idl__type_support.cpp.em
// with input from armpi_interfaces:msg/AssembleQueue.idl
// generated code does not contain a copyright notice

#include "array"
#include "cstddef"
#include "string"
#include "vector"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_interface/macros.h"
#include "armpi_interfaces/msg/detail/assemble_queue__functions.h"
#include "armpi_interfaces/msg/detail/assemble_queue__struct.hpp"
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

void AssembleQueue_init_function(
  void * message_memory, rosidl_runtime_cpp::MessageInitialization _init)
{
  new (message_memory) armpi_interfaces::msg::AssembleQueue(_init);
}

void AssembleQueue_fini_function(void * message_memory)
{
  auto typed_message = static_cast<armpi_interfaces::msg::AssembleQueue *>(message_memory);
  typed_message->~AssembleQueue();
}

static const ::rosidl_typesupport_introspection_cpp::MessageMember AssembleQueue_message_member_array[3] = {
  {
    "id",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces::msg::AssembleQueue, id),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "type",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces::msg::AssembleQueue, type),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  },
  {
    "number_objects",  // name
    ::rosidl_typesupport_introspection_cpp::ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    nullptr,  // members of sub message
    false,  // is key
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces::msg::AssembleQueue, number_objects),  // bytes offset in struct
    nullptr,  // default value
    nullptr,  // size() function pointer
    nullptr,  // get_const(index) function pointer
    nullptr,  // get(index) function pointer
    nullptr,  // fetch(index, &value) function pointer
    nullptr,  // assign(index, value) function pointer
    nullptr  // resize(index) function pointer
  }
};

static const ::rosidl_typesupport_introspection_cpp::MessageMembers AssembleQueue_message_members = {
  "armpi_interfaces::msg",  // message namespace
  "AssembleQueue",  // message name
  3,  // number of fields
  sizeof(armpi_interfaces::msg::AssembleQueue),
  false,  // has_any_key_member_
  AssembleQueue_message_member_array,  // message members
  AssembleQueue_init_function,  // function to initialize message memory (memory has to be allocated)
  AssembleQueue_fini_function  // function to terminate message instance (will not free memory)
};

static const rosidl_message_type_support_t AssembleQueue_message_type_support_handle = {
  ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
  &AssembleQueue_message_members,
  get_message_typesupport_handle_function,
  &armpi_interfaces__msg__AssembleQueue__get_type_hash,
  &armpi_interfaces__msg__AssembleQueue__get_type_description,
  &armpi_interfaces__msg__AssembleQueue__get_type_description_sources,
};

}  // namespace rosidl_typesupport_introspection_cpp

}  // namespace msg

}  // namespace armpi_interfaces


namespace rosidl_typesupport_introspection_cpp
{

template<>
ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<armpi_interfaces::msg::AssembleQueue>()
{
  return &::armpi_interfaces::msg::rosidl_typesupport_introspection_cpp::AssembleQueue_message_type_support_handle;
}

}  // namespace rosidl_typesupport_introspection_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_INTROSPECTION_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, armpi_interfaces, msg, AssembleQueue)() {
  return &::armpi_interfaces::msg::rosidl_typesupport_introspection_cpp::AssembleQueue_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif
