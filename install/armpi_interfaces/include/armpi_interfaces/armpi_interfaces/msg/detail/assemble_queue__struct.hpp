// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from armpi_interfaces:msg/AssembleQueue.idl
// generated code does not contain a copyright notice

#ifndef ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__STRUCT_HPP_
#define ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__armpi_interfaces__msg__AssembleQueue __attribute__((deprecated))
#else
# define DEPRECATED__armpi_interfaces__msg__AssembleQueue __declspec(deprecated)
#endif

namespace armpi_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct AssembleQueue_
{
  using Type = AssembleQueue_<ContainerAllocator>;

  explicit AssembleQueue_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0ll;
      this->type = 0ll;
      this->number_objects = 0ll;
    }
  }

  explicit AssembleQueue_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0ll;
      this->type = 0ll;
      this->number_objects = 0ll;
    }
  }

  // field types and members
  using _id_type =
    int64_t;
  _id_type id;
  using _type_type =
    int64_t;
  _type_type type;
  using _number_objects_type =
    int64_t;
  _number_objects_type number_objects;

  // setters for named parameter idiom
  Type & set__id(
    const int64_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__type(
    const int64_t & _arg)
  {
    this->type = _arg;
    return *this;
  }
  Type & set__number_objects(
    const int64_t & _arg)
  {
    this->number_objects = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    armpi_interfaces::msg::AssembleQueue_<ContainerAllocator> *;
  using ConstRawPtr =
    const armpi_interfaces::msg::AssembleQueue_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<armpi_interfaces::msg::AssembleQueue_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<armpi_interfaces::msg::AssembleQueue_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      armpi_interfaces::msg::AssembleQueue_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<armpi_interfaces::msg::AssembleQueue_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      armpi_interfaces::msg::AssembleQueue_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<armpi_interfaces::msg::AssembleQueue_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<armpi_interfaces::msg::AssembleQueue_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<armpi_interfaces::msg::AssembleQueue_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__armpi_interfaces__msg__AssembleQueue
    std::shared_ptr<armpi_interfaces::msg::AssembleQueue_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__armpi_interfaces__msg__AssembleQueue
    std::shared_ptr<armpi_interfaces::msg::AssembleQueue_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const AssembleQueue_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    if (this->type != other.type) {
      return false;
    }
    if (this->number_objects != other.number_objects) {
      return false;
    }
    return true;
  }
  bool operator!=(const AssembleQueue_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct AssembleQueue_

// alias to use template instance with default allocator
using AssembleQueue =
  armpi_interfaces::msg::AssembleQueue_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace armpi_interfaces

#endif  // ARMPI_INTERFACES__MSG__DETAIL__ASSEMBLE_QUEUE__STRUCT_HPP_
