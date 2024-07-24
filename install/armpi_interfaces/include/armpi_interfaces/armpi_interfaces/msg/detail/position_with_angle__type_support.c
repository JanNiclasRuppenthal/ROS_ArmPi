// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from armpi_interfaces:msg/PositionWithAngle.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "armpi_interfaces/msg/detail/position_with_angle__rosidl_typesupport_introspection_c.h"
#include "armpi_interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "armpi_interfaces/msg/detail/position_with_angle__functions.h"
#include "armpi_interfaces/msg/detail/position_with_angle__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  armpi_interfaces__msg__PositionWithAngle__init(message_memory);
}

void armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_fini_function(void * message_memory)
{
  armpi_interfaces__msg__PositionWithAngle__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_message_member_array[5] = {
  {
    "id",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces__msg__PositionWithAngle, id),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces__msg__PositionWithAngle, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces__msg__PositionWithAngle, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces__msg__PositionWithAngle, z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "angle",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT64,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(armpi_interfaces__msg__PositionWithAngle, angle),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_message_members = {
  "armpi_interfaces__msg",  // message namespace
  "PositionWithAngle",  // message name
  5,  // number of fields
  sizeof(armpi_interfaces__msg__PositionWithAngle),
  armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_message_member_array,  // message members
  armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_init_function,  // function to initialize message memory (memory has to be allocated)
  armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_message_type_support_handle = {
  0,
  &armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_armpi_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, armpi_interfaces, msg, PositionWithAngle)() {
  if (!armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_message_type_support_handle.typesupport_identifier) {
    armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &armpi_interfaces__msg__PositionWithAngle__rosidl_typesupport_introspection_c__PositionWithAngle_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
