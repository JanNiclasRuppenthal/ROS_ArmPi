// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from armpi_interfaces:msg/IDArmPi.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "armpi_interfaces/msg/id_arm_pi.hpp"


#ifndef ARMPI_INTERFACES__MSG__DETAIL__ID_ARM_PI__TRAITS_HPP_
#define ARMPI_INTERFACES__MSG__DETAIL__ID_ARM_PI__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "armpi_interfaces/msg/detail/id_arm_pi__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace armpi_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const IDArmPi & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const IDArmPi & msg,
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
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const IDArmPi & msg, bool use_flow_style = false)
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
  const armpi_interfaces::msg::IDArmPi & msg,
  std::ostream & out, size_t indentation = 0)
{
  armpi_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use armpi_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const armpi_interfaces::msg::IDArmPi & msg)
{
  return armpi_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<armpi_interfaces::msg::IDArmPi>()
{
  return "armpi_interfaces::msg::IDArmPi";
}

template<>
inline const char * name<armpi_interfaces::msg::IDArmPi>()
{
  return "armpi_interfaces/msg/IDArmPi";
}

template<>
struct has_fixed_size<armpi_interfaces::msg::IDArmPi>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<armpi_interfaces::msg::IDArmPi>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<armpi_interfaces::msg::IDArmPi>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ARMPI_INTERFACES__MSG__DETAIL__ID_ARM_PI__TRAITS_HPP_
