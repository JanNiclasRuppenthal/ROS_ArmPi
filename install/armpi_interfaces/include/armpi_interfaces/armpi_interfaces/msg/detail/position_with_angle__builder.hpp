// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from armpi_interfaces:msg/PositionWithAngle.idl
// generated code does not contain a copyright notice

#ifndef ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__BUILDER_HPP_
#define ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "armpi_interfaces/msg/detail/position_with_angle__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace armpi_interfaces
{

namespace msg
{

namespace builder
{

class Init_PositionWithAngle_angle
{
public:
  explicit Init_PositionWithAngle_angle(::armpi_interfaces::msg::PositionWithAngle & msg)
  : msg_(msg)
  {}
  ::armpi_interfaces::msg::PositionWithAngle angle(::armpi_interfaces::msg::PositionWithAngle::_angle_type arg)
  {
    msg_.angle = std::move(arg);
    return std::move(msg_);
  }

private:
  ::armpi_interfaces::msg::PositionWithAngle msg_;
};

class Init_PositionWithAngle_z
{
public:
  explicit Init_PositionWithAngle_z(::armpi_interfaces::msg::PositionWithAngle & msg)
  : msg_(msg)
  {}
  Init_PositionWithAngle_angle z(::armpi_interfaces::msg::PositionWithAngle::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_PositionWithAngle_angle(msg_);
  }

private:
  ::armpi_interfaces::msg::PositionWithAngle msg_;
};

class Init_PositionWithAngle_y
{
public:
  explicit Init_PositionWithAngle_y(::armpi_interfaces::msg::PositionWithAngle & msg)
  : msg_(msg)
  {}
  Init_PositionWithAngle_z y(::armpi_interfaces::msg::PositionWithAngle::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_PositionWithAngle_z(msg_);
  }

private:
  ::armpi_interfaces::msg::PositionWithAngle msg_;
};

class Init_PositionWithAngle_x
{
public:
  explicit Init_PositionWithAngle_x(::armpi_interfaces::msg::PositionWithAngle & msg)
  : msg_(msg)
  {}
  Init_PositionWithAngle_y x(::armpi_interfaces::msg::PositionWithAngle::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_PositionWithAngle_y(msg_);
  }

private:
  ::armpi_interfaces::msg::PositionWithAngle msg_;
};

class Init_PositionWithAngle_id
{
public:
  Init_PositionWithAngle_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_PositionWithAngle_x id(::armpi_interfaces::msg::PositionWithAngle::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_PositionWithAngle_x(msg_);
  }

private:
  ::armpi_interfaces::msg::PositionWithAngle msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::armpi_interfaces::msg::PositionWithAngle>()
{
  return armpi_interfaces::msg::builder::Init_PositionWithAngle_id();
}

}  // namespace armpi_interfaces

#endif  // ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__BUILDER_HPP_
