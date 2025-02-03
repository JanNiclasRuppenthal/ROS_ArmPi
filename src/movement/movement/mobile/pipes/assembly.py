import rclpy

from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from armpi_pro_kinematics import ik_transform
from armpi_pro import bus_servo_control
from armpi_pro_service_client.client import call_service

from id_interface.msg import IDArmPi
from position_interface.msg import Position2D

import time
from threading import Thread


enable_rotation = True

ik = ik_transform.ArmIK()

# TODO: Maybe I need to save the nodes somewhere
node = rclpy.create_node('assembly_armpi_pro')
joints_pub = node.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)
next_assembly_step_publisher = node.create_publisher(IDArmPi, 'assembly_step/stationary', 1)

position = None

def get_assembly_node():
    return node


def assembly_init_move():
    time.sleep(0.5)
    target = ik.setPitchRanges((0, 0.24, 0.12), -90, -92, -88) 
    if target:
        print(target)
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 1.5, ((2, 500), (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']),(6, servo_data['servo6'])))
        time.sleep(2)

def notify_stationary_robot_for_the_next_assembly_step(ID):
    id_armpi_message = IDArmPi()
    id_armpi_message.id = ID 
    next_assembly_step_publisher.publish(id_armpi_message)
    node.get_logger().info(f"Send IDArmPi Message to {id_armpi_message.id}")

def got_position():
    return position != None

def save_position(position2D_message):
    global position
    position = position2D_message.x, position2D_message.y

def move_arm_up():
    global position

    if position[0] > 0:
        x_pos = 0 + position[0] if 0 + position[0] <= 0.03 else 0.03
    else:
        x_pos = 0 + position[0] if 0 + position[0] >= -0.03 else -0.03

    if position[1] > 0:
        y_pos = 0.22 + position[1] if 0.22 + position[1] <= 0.24 else 0.24
    else:
        y_pos = 0.22 + position[1] if 0.22 + position[1] >= 0.20 else 0.20

    print(f"Positions: ({x_pos}, {y_pos})")

    time.sleep(0.5)
    target = ik.setPitchRanges((x_pos, y_pos-0.01, 0.24), -90, -92, -88) # or you can use the position (0, 0.22)
    if target:
        print(target)
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 1.5, ((2, 500), (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']),(6, servo_data['servo6'])))
        time.sleep(2)
    else:
        print("could not move arm up")


def move_arm_down():
    global position

    if position[0] > 0:
        x_pos = 0 + position[0] if 0 + position[0] <= 0.03 else 0.03
    else:
        x_pos = 0 + position[0] if 0 + position[0] >= -0.03 else -0.03

    if position[1] > 0:
        y_pos = 0.22 + position[1] if 0.22 + position[1] <= 0.24 else 0.24
    else:
        y_pos = 0.22 + position[1] if 0.22 + position[1] >= 0.20 else 0.20

    print(f"Positions: ({x_pos}, {y_pos})")

    time.sleep(0.5)
    target = ik.setPitchRanges((x_pos, y_pos-0.01, 0.18), -90, -92, -88) # or you can use the position (0, 0.22)
    if target:
        print(target)
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 1.5, ((2, 500), (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']),(6, servo_data['servo6'])))
        time.sleep(2)
    else:
        print("could not move arm down")


def open_claw():
    time.sleep(0.5)
    bus_servo_control.set_servos(joints_pub, 1.5, ((1, 50),))
    time.sleep(1.5)


determined_position_sub = node.create_subscription(Position2D, 'assembly_position_publisher', save_position, 1)