// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from armpi_interfaces:msg/AssembleQueue.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "armpi_interfaces/msg/assemble_queue.hpp"


#ifndef ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__BUILDER_HPP_
#define ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "armpi_interfaces/msg/detail/assemble_queue__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace armpi_interfaces
{

namespace msg
{

namespace builder
{

class Init_AssembleQueue_number_objects
{
public:
  explicit Init_AssembleQueue_number_objects(::armpi_interfaces::msg::AssembleQueue & msg)
  : msg_(msg)
  {}
  ::armpi_interfaces::msg::AssembleQueue number_objects(::armpi_interfaces::msg::AssembleQueue::_number_objects_type arg)
  {
    msg_.number_objects = std::move(arg);
    return std::move(msg_);
  }

private:
  ::armpi_interfaces::msg::AssembleQueue msg_;
};

class Init_AssembleQueue_type
{
public:
  explicit Init_AssembleQueue_type(::armpi_interfaces::msg::AssembleQueue & msg)
  : msg_(msg)
  {}
  Init_AssembleQueue_number_objects type(::armpi_interfaces::msg::AssembleQueue::_type_type arg)
  {
    msg_.type = std::move(arg);
    return Init_AssembleQueue_number_objects(msg_);
  }

private:
  ::armpi_interfaces::msg::AssembleQueue msg_;
};

class Init_AssembleQueue_id
{
public:
  Init_AssembleQueue_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_AssembleQueue_type id(::armpi_interfaces::msg::AssembleQueue::_id_type arg)
  {
    msg_.id = std::move(arg);
    return Init_AssembleQueue_type(msg_);
  }

private:
  ::armpi_interfaces::msg::AssembleQueue msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::armpi_interfaces::msg::AssembleQueue>()
{
  return armpi_interfaces::msg::builder::Init_AssembleQueue_id();
}

}  // namespace armpi_interfaces

#endif  // ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__BUILDER_HPP_
