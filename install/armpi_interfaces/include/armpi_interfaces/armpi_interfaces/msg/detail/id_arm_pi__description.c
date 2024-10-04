// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from armpi_interfaces:msg/IDArmPi.idl
// generated code does not contain a copyright notice

#include "armpi_interfaces/msg/detail/id_arm_pi__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
const rosidl_type_hash_t *
armpi_interfaces__msg__IDArmPi__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0x0e, 0x22, 0xbd, 0xdd, 0x28, 0xe2, 0x3d, 0xee,
      0x56, 0x14, 0x20, 0x34, 0xba, 0x93, 0x7e, 0x70,
      0x8b, 0x04, 0x6b, 0xe1, 0xf8, 0x92, 0x79, 0xcd,
      0x55, 0xf6, 0xec, 0x6f, 0x51, 0xd4, 0xc8, 0x74,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char armpi_interfaces__msg__IDArmPi__TYPE_NAME[] = "armpi_interfaces/msg/IDArmPi";

// Define type names, field names, and default values
static char armpi_interfaces__msg__IDArmPi__FIELD_NAME__id[] = "id";

static rosidl_runtime_c__type_description__Field armpi_interfaces__msg__IDArmPi__FIELDS[] = {
  {
    {armpi_interfaces__msg__IDArmPi__FIELD_NAME__id, 2, 2},
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
armpi_interfaces__msg__IDArmPi__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {armpi_interfaces__msg__IDArmPi__TYPE_NAME, 28, 28},
      {armpi_interfaces__msg__IDArmPi__FIELDS, 1, 1},
    },
    {NULL, 0, 0},
  };
  if (!constructed) {
    constructed = true;
  }
  return &description;
}

static char toplevel_type_raw_source[] =
  "int64 id";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
armpi_interfaces__msg__IDArmPi__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {armpi_interfaces__msg__IDArmPi__TYPE_NAME, 28, 28},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 9, 9},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
armpi_interfaces__msg__IDArmPi__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *armpi_interfaces__msg__IDArmPi__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
