// generated from rosidl_generator_c/resource/idl__description.c.em
// with input from armpi_interfaces:msg/PositionWithAngle.idl
// generated code does not contain a copyright notice

#include "armpi_interfaces/msg/detail/position_with_angle__functions.h"

ROSIDL_GENERATOR_C_PUBLIC_armpi_interfaces
const rosidl_type_hash_t *
armpi_interfaces__msg__PositionWithAngle__get_type_hash(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_type_hash_t hash = {1, {
      0xd3, 0xf9, 0x38, 0x05, 0xc1, 0x71, 0x28, 0x33,
      0x1b, 0x44, 0x8b, 0xa9, 0x0e, 0x42, 0xd4, 0x47,
      0xf7, 0xfd, 0x61, 0xed, 0xee, 0x60, 0x55, 0x56,
      0xc0, 0x3d, 0x3d, 0xfe, 0xce, 0xca, 0x61, 0x34,
    }};
  return &hash;
}

#include <assert.h>
#include <string.h>

// Include directives for referenced types

// Hashes for external referenced types
#ifndef NDEBUG
#endif

static char armpi_interfaces__msg__PositionWithAngle__TYPE_NAME[] = "armpi_interfaces/msg/PositionWithAngle";

// Define type names, field names, and default values
static char armpi_interfaces__msg__PositionWithAngle__FIELD_NAME__id[] = "id";
static char armpi_interfaces__msg__PositionWithAngle__FIELD_NAME__x[] = "x";
static char armpi_interfaces__msg__PositionWithAngle__FIELD_NAME__y[] = "y";
static char armpi_interfaces__msg__PositionWithAngle__FIELD_NAME__z[] = "z";
static char armpi_interfaces__msg__PositionWithAngle__FIELD_NAME__angle[] = "angle";

static rosidl_runtime_c__type_description__Field armpi_interfaces__msg__PositionWithAngle__FIELDS[] = {
  {
    {armpi_interfaces__msg__PositionWithAngle__FIELD_NAME__id, 2, 2},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_INT64,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {armpi_interfaces__msg__PositionWithAngle__FIELD_NAME__x, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {armpi_interfaces__msg__PositionWithAngle__FIELD_NAME__y, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {armpi_interfaces__msg__PositionWithAngle__FIELD_NAME__z, 1, 1},
    {
      rosidl_runtime_c__type_description__FieldType__FIELD_TYPE_DOUBLE,
      0,
      0,
      {NULL, 0, 0},
    },
    {NULL, 0, 0},
  },
  {
    {armpi_interfaces__msg__PositionWithAngle__FIELD_NAME__angle, 5, 5},
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
armpi_interfaces__msg__PositionWithAngle__get_type_description(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static bool constructed = false;
  static const rosidl_runtime_c__type_description__TypeDescription description = {
    {
      {armpi_interfaces__msg__PositionWithAngle__TYPE_NAME, 38, 38},
      {armpi_interfaces__msg__PositionWithAngle__FIELDS, 5, 5},
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
  "float64 x\n"
  "float64 y\n"
  "float64 z\n"
  "int64 angle";

static char msg_encoding[] = "msg";

// Define all individual source functions

const rosidl_runtime_c__type_description__TypeSource *
armpi_interfaces__msg__PositionWithAngle__get_individual_type_description_source(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static const rosidl_runtime_c__type_description__TypeSource source = {
    {armpi_interfaces__msg__PositionWithAngle__TYPE_NAME, 38, 38},
    {msg_encoding, 3, 3},
    {toplevel_type_raw_source, 50, 50},
  };
  return &source;
}

const rosidl_runtime_c__type_description__TypeSource__Sequence *
armpi_interfaces__msg__PositionWithAngle__get_type_description_sources(
  const rosidl_message_type_support_t * type_support)
{
  (void)type_support;
  static rosidl_runtime_c__type_description__TypeSource sources[1];
  static const rosidl_runtime_c__type_description__TypeSource__Sequence source_sequence = {sources, 1, 1};
  static bool constructed = false;
  if (!constructed) {
    sources[0] = *armpi_interfaces__msg__PositionWithAngle__get_individual_type_description_source(NULL),
    constructed = true;
  }
  return &source_sequence;
}
