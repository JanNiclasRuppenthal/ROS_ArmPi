// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from armpi_interfaces:msg/PositionWithAngle.idl
// generated code does not contain a copyright notice
#include "armpi_interfaces/msg/detail/position_with_angle__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
armpi_interfaces__msg__PositionWithAngle__init(armpi_interfaces__msg__PositionWithAngle * msg)
{
  if (!msg) {
    return false;
  }
  // id
  // x
  // y
  // z
  // angle
  return true;
}

void
armpi_interfaces__msg__PositionWithAngle__fini(armpi_interfaces__msg__PositionWithAngle * msg)
{
  if (!msg) {
    return;
  }
  // id
  // x
  // y
  // z
  // angle
}

bool
armpi_interfaces__msg__PositionWithAngle__are_equal(const armpi_interfaces__msg__PositionWithAngle * lhs, const armpi_interfaces__msg__PositionWithAngle * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  // angle
  if (lhs->angle != rhs->angle) {
    return false;
  }
  return true;
}

bool
armpi_interfaces__msg__PositionWithAngle__copy(
  const armpi_interfaces__msg__PositionWithAngle * input,
  armpi_interfaces__msg__PositionWithAngle * output)
{
  if (!input || !output) {
    return false;
  }
  // id
  output->id = input->id;
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  // angle
  output->angle = input->angle;
  return true;
}

armpi_interfaces__msg__PositionWithAngle *
armpi_interfaces__msg__PositionWithAngle__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  armpi_interfaces__msg__PositionWithAngle * msg = (armpi_interfaces__msg__PositionWithAngle *)allocator.allocate(sizeof(armpi_interfaces__msg__PositionWithAngle), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(armpi_interfaces__msg__PositionWithAngle));
  bool success = armpi_interfaces__msg__PositionWithAngle__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
armpi_interfaces__msg__PositionWithAngle__destroy(armpi_interfaces__msg__PositionWithAngle * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    armpi_interfaces__msg__PositionWithAngle__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
armpi_interfaces__msg__PositionWithAngle__Sequence__init(armpi_interfaces__msg__PositionWithAngle__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  armpi_interfaces__msg__PositionWithAngle * data = NULL;

  if (size) {
    data = (armpi_interfaces__msg__PositionWithAngle *)allocator.zero_allocate(size, sizeof(armpi_interfaces__msg__PositionWithAngle), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = armpi_interfaces__msg__PositionWithAngle__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        armpi_interfaces__msg__PositionWithAngle__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
armpi_interfaces__msg__PositionWithAngle__Sequence__fini(armpi_interfaces__msg__PositionWithAngle__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      armpi_interfaces__msg__PositionWithAngle__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

armpi_interfaces__msg__PositionWithAngle__Sequence *
armpi_interfaces__msg__PositionWithAngle__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  armpi_interfaces__msg__PositionWithAngle__Sequence * array = (armpi_interfaces__msg__PositionWithAngle__Sequence *)allocator.allocate(sizeof(armpi_interfaces__msg__PositionWithAngle__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = armpi_interfaces__msg__PositionWithAngle__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
armpi_interfaces__msg__PositionWithAngle__Sequence__destroy(armpi_interfaces__msg__PositionWithAngle__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    armpi_interfaces__msg__PositionWithAngle__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
armpi_interfaces__msg__PositionWithAngle__Sequence__are_equal(const armpi_interfaces__msg__PositionWithAngle__Sequence * lhs, const armpi_interfaces__msg__PositionWithAngle__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!armpi_interfaces__msg__PositionWithAngle__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
armpi_interfaces__msg__PositionWithAngle__Sequence__copy(
  const armpi_interfaces__msg__PositionWithAngle__Sequence * input,
  armpi_interfaces__msg__PositionWithAngle__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(armpi_interfaces__msg__PositionWithAngle);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    armpi_interfaces__msg__PositionWithAngle * data =
      (armpi_interfaces__msg__PositionWithAngle *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!armpi_interfaces__msg__PositionWithAngle__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          armpi_interfaces__msg__PositionWithAngle__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!armpi_interfaces__msg__PositionWithAngle__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
