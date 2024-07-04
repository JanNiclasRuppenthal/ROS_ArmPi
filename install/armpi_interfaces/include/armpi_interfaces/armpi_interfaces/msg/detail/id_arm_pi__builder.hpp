// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from armpi_interfaces:msg/IDArmPi.idl
// generated code does not contain a copyright notice

#ifndef ARMPI_INTERFACES__MSG__DETAIL__ID_ARM_PI__BUILDER_HPP_
#define ARMPI_INTERFACES__MSG__DETAIL__ID_ARM_PI__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "armpi_interfaces/msg/detail/id_arm_pi__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace armpi_interfaces
{

namespace msg
{

namespace builder
{

class Init_IDArmPi_id
{
public:
  Init_IDArmPi_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::armpi_interfaces::msg::IDArmPi id(::armpi_interfaces::msg::IDArmPi::_id_type arg)
  {
    msg_.id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::armpi_interfaces::msg::IDArmPi msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::armpi_interfaces::msg::IDArmPi>()
{
  return armpi_interfaces::msg::builder::Init_IDArmPi_id();
}

}  // namespace armpi_interfaces

#endif  // ARMPI_INTERFACES__MSG__DETAIL__ID_ARM_PI__BUILDER_HPP_
