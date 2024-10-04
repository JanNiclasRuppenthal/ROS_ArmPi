// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from armpi_interfaces:msg/PositionWithAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "armpi_interfaces/msg/position_with_angle.h"


#ifndef ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__FUNCTIONS_H_
#define ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_runtime_c/type_description/type_description__struct.h"
#include "rosidl_runtime_c/type_description/type_source__struct.h"
#include "rosidl_runtime_c/type_hash.h"
#include "rosidl_runtime_c/visibility_control.h"
#include "armpi_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "armpi_interfaces/msg/detail/position_with_angle__struct.h"

/// Initialize msg/PositionWithAngle message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * armpi_interfaces__msg__PositionWithAngle
 * )) before or use
 * armpi_interfaces__msg__PositionWithAngle__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
bool
armpi_interfaces__msg__PositionWithAngle__init(armpi_interfaces__msg__PositionWithAngle * msg);

/// Finalize msg/PositionWithAngle message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
void
armpi_interfaces__msg__PositionWithAngle__fini(armpi_interfaces__msg__PositionWithAngle * msg);

/// Create msg/PositionWithAngle message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * armpi_interfaces__msg__PositionWithAngle__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
armpi_interfaces__msg__PositionWithAngle *
armpi_interfaces__msg__PositionWithAngle__create(void);

/// Destroy msg/PositionWithAngle message.
/**
 * It calls
 * armpi_interfaces__msg__PositionWithAngle__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
void
armpi_interfaces__msg__PositionWithAngle__destroy(armpi_interfaces__msg__PositionWithAngle * msg);

/// Check for msg/PositionWithAngle message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
bool
armpi_interfaces__msg__PositionWithAngle__are_equal(const armpi_interfaces__msg__PositionWithAngle * lhs, const armpi_interfaces__msg__PositionWithAngle * rhs);

/// Copy a msg/PositionWithAngle message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
bool
armpi_interfaces__msg__PositionWithAngle__copy(
  const armpi_interfaces__msg__PositionWithAngle * input,
  armpi_interfaces__msg__PositionWithAngle * output);

/// Retrieve pointer to the hash of the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
const rosidl_type_hash_t *
armpi_interfaces__msg__PositionWithAngle__get_type_hash(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
const rosidl_runtime_c__type_description__TypeDescription *
armpi_interfaces__msg__PositionWithAngle__get_type_description(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the single raw source text that defined this type.
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
const rosidl_runtime_c__type_description__TypeSource *
armpi_interfaces__msg__PositionWithAngle__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support);

/// Retrieve pointer to the recursive raw sources that defined the description of this type.
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
const rosidl_runtime_c__type_description__TypeSource__Sequence *
armpi_interfaces__msg__PositionWithAngle__get_type_description_sources(
  const rosidl_message_type_support_t * type_support);

/// Initialize array of msg/PositionWithAngle messages.
/**
 * It allocates the memory for the number of elements and calls
 * armpi_interfaces__msg__PositionWithAngle__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
bool
armpi_interfaces__msg__PositionWithAngle__Sequence__init(armpi_interfaces__msg__PositionWithAngle__Sequence * array, size_t size);

/// Finalize array of msg/PositionWithAngle messages.
/**
 * It calls
 * armpi_interfaces__msg__PositionWithAngle__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
void
armpi_interfaces__msg__PositionWithAngle__Sequence__fini(armpi_interfaces__msg__PositionWithAngle__Sequence * array);

/// Create array of msg/PositionWithAngle messages.
/**
 * It allocates the memory for the array and calls
 * armpi_interfaces__msg__PositionWithAngle__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
armpi_interfaces__msg__PositionWithAngle__Sequence *
armpi_interfaces__msg__PositionWithAngle__Sequence__create(size_t size);

/// Destroy array of msg/PositionWithAngle messages.
/**
 * It calls
 * armpi_interfaces__msg__PositionWithAngle__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
void
armpi_interfaces__msg__PositionWithAngle__Sequence__destroy(armpi_interfaces__msg__PositionWithAngle__Sequence * array);

/// Check for msg/PositionWithAngle message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
bool
armpi_interfaces__msg__PositionWithAngle__Sequence__are_equal(const armpi_interfaces__msg__PositionWithAngle__Sequence * lhs, const armpi_interfaces__msg__PositionWithAngle__Sequence * rhs);

/// Copy an array of msg/PositionWithAngle messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
bool
armpi_interfaces__msg__PositionWithAngle__Sequence__copy(
  const armpi_interfaces__msg__PositionWithAngle__Sequence * input,
  armpi_interfaces__msg__PositionWithAngle__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__FUNCTIONS_H_
