// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from armpi_interfaces:msg/AssembleQueue.idl
// generated code does not contain a copyright notice

#ifndef ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__STRUCT_H_
#define ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in msg/AssembleQueue in the package armpi_interfaces.
typedef struct armpi_interfaces__msg__AssembleQueue
{
  int64_t id;
  int64_t type;
  int64_t number_objects;
} armpi_interfaces__msg__AssembleQueue;

// Struct for a sequence of armpi_interfaces__msg__AssembleQueue.
typedef struct armpi_interfaces__msg__AssembleQueue__Sequence
{
  armpi_interfaces__msg__AssembleQueue * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} armpi_interfaces__msg__AssembleQueue__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__STRUCT_H_
