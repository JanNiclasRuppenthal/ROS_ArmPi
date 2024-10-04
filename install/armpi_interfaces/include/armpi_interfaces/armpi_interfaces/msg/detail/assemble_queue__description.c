// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from armpi_interfaces:msg/AssembleQueue.idl
// generated code does not contain a copyright notice

#include "armpi_interfaces/msg/detail/assemble_queue__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
const rosidl_type_hash_t *
armpi_interfaces__msg__AssembleQueue__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x4f, 0x97, 0x9f, 0x93, 0xde, 0xe6, 0x81, 0x97,
      0xed, 0x55, 0x35, 0xa9, 0x1f, 0x86, 0xfa, 0xf0,
      0x5b, 0xe0, 0xd1, 0xa7, 0xff, 0xf9, 0x06, 0x13,
      0x7f, 0x4a, 0x48, 0xdd, 0xa5, 0x92, 0x21, 0xec,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char armpi_interfaces__msg__AssembleQueue__TYPE_NAME[] = "armpi_interfaces/msg/AssembleQueue";

// Define type names, field names, and default values
static char armpi_interfaces__msg__AssembleQueue__FIELD_NAME__id[] = "id";
static char armpi_interfaces__msg__AssembleQueue__FIELD_NAME__type[] = "type";
static char armpi_interfaces__msg__AssembleQueue__FIELD_NAME__number_objects[] = "number_objects";

static rosidl_runtime_c__type_description__Field armpi_interfaces__msg__AssembleQueue__FIELDS[] = {
  {
    {armpi_interfaces__msg__AssembleQueue__FIELD_NAME__id, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {armpi_interfaces__msg__AssembleQueue__FIELD_NAME__type, 4, 4},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {armpi_interfaces__msg__AssembleQueue__FIELD_NAME__number_objects, 14, 14},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
};

const rosidl_runtime_c__type_description__TypeDescription *
armpi_interfaces__msg__AssembleQueue__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {armpi_interfaces__msg__AssembleQueue__TYPE_NAME, 34, 34},
      {armpi_interfaces__msg__AssembleQueue__FIELDS, 3, 3},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "int64 id\n"
  "int64 type\n"
  "int64 number_objects";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
armpi_interfaces__msg__AssembleQueue__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {armpi_interfaces__msg__AssembleQueue__TYPE_NAME, 34, 34},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 40, 40},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
armpi_interfaces__msg__AssembleQueue__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *armpi_interfaces__msg__AssembleQueue__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
