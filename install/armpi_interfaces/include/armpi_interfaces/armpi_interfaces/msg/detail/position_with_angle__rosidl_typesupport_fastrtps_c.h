// generated from rosidl_typesupport_fastrtps_c/resource/idl__rosidl_typesupport_fastrtps_c.h.em
// with input from armpi_interfaces:msg/PositionWithAngle.idl
// generated code does not contain a copyright notice
#ifndef ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
#define ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_


#include <stddef.h>
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "armpi_interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "armpi_interfaces/msg/detail/position_with_angle__struct.h"
#include "fastcdr/Cdr.h"

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_armpi_interfaces
bool cdr_serialize_armpi_interfaces__msg__PositionWithAngle(
  const armpi_interfaces__msg__PositionWithAngle * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_armpi_interfaces
bool cdr_deserialize_armpi_interfaces__msg__PositionWithAngle(
  eprosima::fastcdr::Cdr &,
  armpi_interfaces__msg__PositionWithAngle * ros_message);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_armpi_interfaces
size_t get_serialized_size_armpi_interfaces__msg__PositionWithAngle(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_armpi_interfaces
size_t max_serialized_size_armpi_interfaces__msg__PositionWithAngle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_armpi_interfaces
bool cdr_serialize_key_armpi_interfaces__msg__PositionWithAngle(
  const armpi_interfaces__msg__PositionWithAngle * ros_message,
  eprosima::fastcdr::Cdr & cdr);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_armpi_interfaces
size_t get_serialized_size_key_armpi_interfaces__msg__PositionWithAngle(
  const void * untyped_ros_message,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_armpi_interfaces
size_t max_serialized_size_key_armpi_interfaces__msg__PositionWithAngle(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_armpi_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, armpi_interfaces, msg, PositionWithAngle)();

#ifdef __cplusplus
}
#endif

#endif  // ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__ROSIDL_TYPESUPPORT_FASTRTPS_C_H_
