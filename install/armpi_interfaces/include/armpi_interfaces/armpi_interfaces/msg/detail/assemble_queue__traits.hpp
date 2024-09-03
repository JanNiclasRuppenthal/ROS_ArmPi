// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from armpi_interfaces:msg/AssembleQueue.idl
// generated code does not contain a copyright notice

#ifndef ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__TRAITS_HPP_
#define ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "armpi_interfaces/msg/detail/assemble_queue__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace armpi_interfaces
{

namespace msg
{

inline void to_flow_style_yaml(
  const AssembleQueue & msg,
  std::ostream & out)
{
  out << "{";
  // member: id
  {
    out << "id: ";
    rosidl_generator_traits::value_to_yaml(msg.id, out);
    out << ", ";
  }

  // member: type
  {
    out << "type: ";
    rosidl_generator_traits::value_to_yaml(msg.type, out);
    out << ", ";
  }

  // member: number_objects
  {
    out << "number_objects: ";
    rosidl_generator_traits::value_to_yaml(msg.number_objects, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const AssembleQueue & msg,
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

  // member: type
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "type: ";
    rosidl_generator_traits::value_to_yaml(msg.type, out);
    out << "\n";
  }

  // member: number_objects
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "number_objects: ";
    rosidl_generator_traits::value_to_yaml(msg.number_objects, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const AssembleQueue & msg, bool use_flow_style = false)
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
  const armpi_interfaces::msg::AssembleQueue & msg,
  std::ostream & out, size_t indentation = 0)
{
  armpi_interfaces::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use armpi_interfaces::msg::to_yaml() instead")]]
inline std::string to_yaml(const armpi_interfaces::msg::AssembleQueue & msg)
{
  return armpi_interfaces::msg::to_yaml(msg);
}

template<>
inline const char * data_type<armpi_interfaces::msg::AssembleQueue>()
{
  return "armpi_interfaces::msg::AssembleQueue";
}

template<>
inline const char * name<armpi_interfaces::msg::AssembleQueue>()
{
  return "armpi_interfaces/msg/AssembleQueue";
}

template<>
struct has_fixed_size<armpi_interfaces::msg::AssembleQueue>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<armpi_interfaces::msg::AssembleQueue>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<armpi_interfaces::msg::AssembleQueue>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__TRAITS_HPP_
