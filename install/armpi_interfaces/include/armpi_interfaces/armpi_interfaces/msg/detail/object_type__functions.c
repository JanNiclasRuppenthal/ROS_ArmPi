// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from armpi_interfaces:msg/ObjectType.idl
// generated code does not contain a copyright notice
#include "armpi_interfaces/msg/detail/object_type__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


bool
armpi_interfaces__msg__ObjectType__init(armpi_interfaces__msg__ObjectType * msg)
{
  if (!msg) {
    return false;
  }
  // id
  // type
  return true;
}

void
armpi_interfaces__msg__ObjectType__fini(armpi_interfaces__msg__ObjectType * msg)
{
  if (!msg) {
    return;
  }
  // id
  // type
}

bool
armpi_interfaces__msg__ObjectType__are_equal(const armpi_interfaces__msg__ObjectType * lhs, const armpi_interfaces__msg__ObjectType * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // id
  if (lhs->id != rhs->id) {
    return false;
  }
  // type
  if (lhs->type != rhs->type) {
    return false;
  }
  return true;
}

bool
armpi_interfaces__msg__ObjectType__copy(
  const armpi_interfaces__msg__ObjectType * input,
  armpi_interfaces__msg__ObjectType * output)
{
  if (!input || !output) {
    return false;
  }
  // id
  output->id = input->id;
  // type
  output->type = input->type;
  return true;
}

armpi_interfaces__msg__ObjectType *
armpi_interfaces__msg__ObjectType__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  armpi_interfaces__msg__ObjectType * msg = (armpi_interfaces__msg__ObjectType *)allocator.allocate(sizeof(armpi_interfaces__msg__ObjectType), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(armpi_interfaces__msg__ObjectType));
  bool success = armpi_interfaces__msg__ObjectType__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
armpi_interfaces__msg__ObjectType__destroy(armpi_interfaces__msg__ObjectType * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    armpi_interfaces__msg__ObjectType__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
armpi_interfaces__msg__ObjectType__Sequence__init(armpi_interfaces__msg__ObjectType__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  armpi_interfaces__msg__ObjectType * data = NULL;

  if (size) {
    data = (armpi_interfaces__msg__ObjectType *)allocator.zero_allocate(size, sizeof(armpi_interfaces__msg__ObjectType), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = armpi_interfaces__msg__ObjectType__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        armpi_interfaces__msg__ObjectType__fini(&data[i - 1]);
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
armpi_interfaces__msg__ObjectType__Sequence__fini(armpi_interfaces__msg__ObjectType__Sequence * array)
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
      armpi_interfaces__msg__ObjectType__fini(&array->data[i]);
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

armpi_interfaces__msg__ObjectType__Sequence *
armpi_interfaces__msg__ObjectType__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  armpi_interfaces__msg__ObjectType__Sequence * array = (armpi_interfaces__msg__ObjectType__Sequence *)allocator.allocate(sizeof(armpi_interfaces__msg__ObjectType__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = armpi_interfaces__msg__ObjectType__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
armpi_interfaces__msg__ObjectType__Sequence__destroy(armpi_interfaces__msg__ObjectType__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    armpi_interfaces__msg__ObjectType__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
armpi_interfaces__msg__ObjectType__Sequence__are_equal(const armpi_interfaces__msg__ObjectType__Sequence * lhs, const armpi_interfaces__msg__ObjectType__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!armpi_interfaces__msg__ObjectType__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
armpi_interfaces__msg__ObjectType__Sequence__copy(
  const armpi_interfaces__msg__ObjectType__Sequence * input,
  armpi_interfaces__msg__ObjectType__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(armpi_interfaces__msg__ObjectType);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    armpi_interfaces__msg__ObjectType * data =
      (armpi_interfaces__msg__ObjectType *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!armpi_interfaces__msg__ObjectType__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          armpi_interfaces__msg__ObjectType__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!armpi_interfaces__msg__ObjectType__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
