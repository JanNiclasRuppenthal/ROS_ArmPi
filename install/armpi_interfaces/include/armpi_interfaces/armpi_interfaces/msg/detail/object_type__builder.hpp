// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from armpi_interfaces:msg/ObjectType.idl
// generated code does not contain a copyright notice

#ifndef ARMPI_INTERFACES__MSG__DETAIL__OBJECT_TYPE__BUILDER_HPP_
#define ARMPI_INTERFACES__MSG__DETAIL__OBJECT_TYPE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "armpi_interfaces/msg/detail/object_type__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace armpi_interfaces
{

namespace msg
{

namespace builder
{

class Init_ObjectType_type
{
public:
  explicit Init_ObjectType_type(::armpi_interfaces::msg::ObjectType & msg)
  : msg_(msg)
  {}
  ::armpi_interfaces::msg::ObjectType type(::armpi_interfaces::msg::ObjectType::_type_type arg)
  {
    msg_.type = std::move(arg);
    return std::move(msg_);
  }

private:
  ::armpi_interfaces::msg::ObjectType msg_;
};

class Init_ObjectType_id
{
public:
  Init_ObjectType_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_ObjectType_type id(::armpi_interfaces::msg::ObjectType::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_ObjectType_type(msg_);
  }

private:
  ::armpi_interfaces::msg::ObjectType msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::armpi_interfaces::msg::ObjectType>()
{
  return armpi_interfaces::msg::builder::Init_ObjectType_id();
}

}  // namespace armpi_interfaces

#endif  // ARMPI_INTERFACES__MSG__DETAIL__OBJECT_TYPE__BUILDER_HPP_
