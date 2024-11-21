import rclpy

from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from armpi_pro_kinematics import ik_transform
from armpi_pro import bus_servo_control
from armpi_pro_service_client.client import call_service

from armpi_interfaces.msg import IDArmPi
from armpi_interfaces.msg import Position2D

import time
from threading import Thread


enable_rotation = True

ik = ik_transform.ArmIK()

# TODO: Maybe I need to save the nodes somewhere
node = rclpy.create_node('assembly_armpi_pro')
joints_pub = node.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)
ready_for_assembly_sub = node.create_publisher(IDArmPi, 'ready_for_assembly', 1)

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

def notify_next_stationary_robot(ID):
    id_armpi_message = IDArmPi()
    id_armpi_message.id = ID 
    ready_for_assembly_sub.publish(id_armpi_message)
    node.get_logger().info(f"Send IDArmPi Message to {id_armpi_message.id}")

def got_position():
    return position != None

def save_position(position2D_message):
    global position
    position = position2D_message.x, position2D_message.y



determined_position_sub = node.create_subscription(Position2D, 'determined_position', save_position, 1)