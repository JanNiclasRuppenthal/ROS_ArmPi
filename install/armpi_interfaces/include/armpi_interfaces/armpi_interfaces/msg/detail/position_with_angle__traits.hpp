// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from armpi_interfaces:msg/PositionWithAngle.idl
// generated code does not contain a copyright notice

#ifndef ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__TRAITS_HPP_
#define ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "armpi_interfaces/msg/detail/position_with_angle__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace armpi_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const PositionWithAngle & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << ", ";
  }

  // member: angle
  {
    out << "angle: ";
    rosidl_generator_traits::value_to_yaml(msg.angle, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const PositionWithAngle & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << "\n";
  }

  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }

  // member: angle
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "angle: ";
    rosidl_generator_traits::value_to_yaml(msg.angle, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const PositionWithAngle & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace armpi_interfaces

namespace rosidl_generator_traits
{

[[deprecated("use armpi_interfaces::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const armpi_interfaces::msg::PositionWithAngle & msg,
  std::ostream & out, size_t indentation = 0)
{
  armpi_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use armpi_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const armpi_interfaces::msg::PositionWithAngle & msg)
{
  return armpi_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<armpi_interfaces::msg::PositionWithAngle>()
{
  return "armpi_interfaces::msg::PositionWithAngle";
}

template<>
inline const char * name<armpi_interfaces::msg::PositionWithAngle>()
{
  return "armpi_interfaces/msg/PositionWithAngle";
}

template<>
struct has_fixed_size<armpi_interfaces::msg::PositionWithAngle>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<armpi_interfaces::msg::PositionWithAngle>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<armpi_interfaces::msg::PositionWithAngle>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__TRAITS_HPP_
