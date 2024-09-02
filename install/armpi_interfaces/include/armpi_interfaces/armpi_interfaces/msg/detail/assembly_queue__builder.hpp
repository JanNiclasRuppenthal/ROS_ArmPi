// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from armpi_interfaces:msg/AssemblyQueue.idl
// generated code does not contain a copyright notice

#ifndef ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLY_QUEUE__BUILDER_HPP_
#define ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLY_QUEUE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "armpi_interfaces/msg/detail/assembly_queue__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace armpi_interfaces
{

namespace msg
{

namespace builder
{

class Init_AssemblyQueue_number_objects
{
public:
  explicit Init_AssemblyQueue_number_objects(::armpi_interfaces::msg::AssemblyQueue & msg)
  : msg_(msg)
  {}
  ::armpi_interfaces::msg::AssemblyQueue number_objects(::armpi_interfaces::msg::AssemblyQueue::_number_objects_type arg)
  {
    msg_.number_objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::armpi_interfaces::msg::AssemblyQueue msg_;
};

class Init_AssemblyQueue_type
{
public:
  explicit Init_AssemblyQueue_type(::armpi_interfaces::msg::AssemblyQueue & msg)
  : msg_(msg)
  {}
  Init_AssemblyQueue_number_objects type(::armpi_interfaces::msg::AssemblyQueue::_type_type arg)
  {
    msg_.type = std::move(arg);
    return Init_AssemblyQueue_number_objects(msg_);
  }

private:
  ::armpi_interfaces::msg::AssemblyQueue msg_;
};

class Init_AssemblyQueue_id
{
public:
  Init_AssemblyQueue_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AssemblyQueue_type id(::armpi_interfaces::msg::AssemblyQueue::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_AssemblyQueue_type(msg_);
  }

private:
  ::armpi_interfaces::msg::AssemblyQueue msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::armpi_interfaces::msg::AssemblyQueue>()
{
  return armpi_interfaces::msg::builder::Init_AssemblyQueue_id();
}

}  // namespace armpi_interfaces

#endif  // ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLY_QUEUE__BUILDER_HPP_
