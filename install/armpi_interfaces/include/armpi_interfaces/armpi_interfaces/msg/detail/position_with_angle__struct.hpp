// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from armpi_interfaces:msg/PositionWithAngle.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "armpi_interfaces/msg/position_with_angle.hpp"


#ifndef ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__STRUCT_HPP_
#define ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__armpi_interfaces__msg__PositionWithAngle __attribute__((deprecated))
#else
# define DEPRECATED__armpi_interfaces__msg__PositionWithAngle __declspec(deprecated)
#endif

namespace armpi_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct PositionWithAngle_
{
  using Type = PositionWithAngle_<ContainerAllocator>;

  explicit PositionWithAngle_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0ll;
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
      this->angle = 0ll;
    }
  }

  explicit PositionWithAngle_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->id = 0ll;
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
      this->angle = 0ll;
    }
  }

  // field types and members
  using _id_type =
    int64_t;
  _id_type id;
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _z_type =
    double;
  _z_type z;
  using _angle_type =
    int64_t;
  _angle_type angle;

  // setters for named parameter idiom
  Type & set__id(
    const int64_t & _arg)
  {
    this->id = _arg;
    return *this;
  }
  Type & set__x(
    const double & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const double & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const double & _arg)
  {
    this->z = _arg;
    return *this;
  }
  Type & set__angle(
    const int64_t & _arg)
  {
    this->angle = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator> *;
  using ConstRawPtr =
    const armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__armpi_interfaces__msg__PositionWithAngle
    std::shared_ptr<armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__armpi_interfaces__msg__PositionWithAngle
    std::shared_ptr<armpi_interfaces::msg::PositionWithAngle_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const PositionWithAngle_ & other) const
  {
    if (this->id != other.id) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    if (this->angle != other.angle) {
      return false;
    }
    return true;
  }
  bool operator!=(const PositionWithAngle_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct PositionWithAngle_

// alias to use template instance with default allocator
using PositionWithAngle =
  armpi_interfaces::msg::PositionWithAngle_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace armpi_interfaces

#endif  // ARMPI_INTERFACES__MSG__DETAIL__POSITION_WITH_ANGLE__STRUCT_HPP_
