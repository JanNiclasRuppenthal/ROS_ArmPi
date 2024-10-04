// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from armpi_interfaces:msg/PositionWithAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "armpi_interfaces/msg/position_with_angle.h"


#ifndef ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__STRUCT_H_
#define ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

// Constants defined in the message

/// Struct defined in msg/PositionWithAngle in the package armpi_interfaces.
typedef struct armpi_interfaces__msg__PositionWithAngle
{
  int64_t id;
  double x;
  double y;
  double z;
  int64_t angle;
} armpi_interfaces__msg__PositionWithAngle;

// Struct for a sequence of armpi_interfaces__msg__PositionWithAngle.
typedef struct armpi_interfaces__msg__PositionWithAngle__Sequence
{
  armpi_interfaces__msg__PositionWithAngle * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} armpi_interfaces__msg__PositionWithAngle__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__STRUCT_H_
