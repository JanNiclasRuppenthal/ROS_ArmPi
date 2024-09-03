// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from armpi_interfaces:msg/ObjectType.idl
// generated code does not contain a copyright notice

#ifndef ARMPI_INTERFACES__MSG__DETAIL__OBJECT_TYPE__STRUCT_H_
#define ARMPI_INTERFACES__MSG__DETAIL__OBJECT_TYPE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/ObjectType in the package armpi_interfaces.
typedef struct armpi_interfaces__msg__ObjectType
{
  int64_t id;
  int64_t type;
} armpi_interfaces__msg__ObjectType;

// Struct for a sequence of armpi_interfaces__msg__ObjectType.
typedef struct armpi_interfaces__msg__ObjectType__Sequence
{
  armpi_interfaces__msg__ObjectType * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} armpi_interfaces__msg__ObjectType__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARMPI_INTERFACES__MSG__DETAIL__OBJECT_TYPE__STRUCT_H_
