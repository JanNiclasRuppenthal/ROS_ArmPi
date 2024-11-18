# TODO: Implement all the necessary methods for driving and following the lines
import rclpy

from chassis_control.msg import SetVelocity

import time

node = rclpy.create_node('driving_node')
set_velocity = node.create_publisher(SetVelocity, '/chassis_control/set_velocity', 1)

TWO_AND_HALF_SECONDS = 2.5

def __create_set_velocity_message(velocity, direction, angular):
    set_velocity_message = SetVelocity()
    set_velocity_message.velocity = velocity
    set_velocity_message.direction = direction
    set_velocity_message.angular = angular
    return set_velocity_message

def __stop_armpi_pro():
    stop_message = __create_set_velocity_message(0.0, 0.0, 0.0)
    set_velocity.publish(stop_message)
    time.sleep(0.5)

def drive_backwards(duration_in_s):
    backwards_message = __create_set_velocity_message(100.0, -90.0, 0.0)
    set_velocity.publish(backwards_message) 

    time.sleep(duration_in_s)

    __stop_armpi_pro()


def rotate_right():
    backwards_message = __create_set_velocity_message(0.0, 90.0, -0.45)
    set_velocity.publish(backwards_message) 

    time.sleep(TWO_AND_HALF_SECONDS)

    __stop_armpi_pro()

def rotate_left():
    backwards_message = __create_set_velocity_message(0.0, 90.0, 0.45)
    set_velocity.publish(backwards_message) 

    time.sleep(TWO_SECONDS)

    __stop_armpi_pro()


def follow_lines(msg):
    pass