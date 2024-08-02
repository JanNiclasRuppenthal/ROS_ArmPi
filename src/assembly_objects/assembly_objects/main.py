import sys
sys.path.append('/home/pi/ArmPi/')

import time

from threading import Thread

import rclpy

from robot.armpi import ArmPi
from robot.publisher.ready_publisher import create_ready_publisher_node
from robot.publisher.finish_publisher import create_finish_publisher_node
from robot.publisher.position_publisher import create_pos_publisher_node
from robot.subscriber.ready_subscriber import create_ready_subscriber_node
from robot.subscriber.finish_subscriber import create_finish_subscriber_node
from robot.subscriber.position_subscriber import create_pos_subscriber_node
from util.position_angle import calculate_position_and_angle
from util.executor_subscriptions import MultiExecutor
from util.movement import *

rclpy.init()

def read_all_arguments():
    ID = int(sys.argv[1])
    scenarioID = int(sys.argv[2])
    return ID, scenarioID

def end_scenario(executor, x, y, angle, rotation_direction):
    put_down_grabbed_object(x, y, angle, rotation_direction)
    initMove()
    executor.execute_shutdown()

def process_first_robot(armpi, ready_publisher, finish_publisher, pos_publisher, executor):
    x, y, angle, rotation_direction = calculate_position_and_angle()

    # found no object in the field
    if (x == -1 and y == -1):
        finish_publisher.send_msg()
        executor.execute_shutdown()
        return

    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction)
    go_to_waiting_position(armpi.get_ID())

    # signal to the other robot that this robot is ready
    ready_publisher.send_msg()
    while (not armpi.get_ready_flag()):

        if armpi.get_finish_flag():
            end_scenario(executor, x, y, angle, rotation_direction)
            return

        ready_publisher.send_msg()
        time.sleep(1)
    
    armpi.set_ready_flag(False)

    (assemble_x, assemble_y, assemble_z, assemble_angle) = (x, 30, 10, 10)
    go_to_assemble_position(assemble_x, assemble_y, assemble_z, assemble_angle)
    pos_publisher.send_msg(float(assemble_x), float(assemble_y), float(assemble_z), assemble_angle)

    while (not armpi.get_ready_flag()):
        time.sleep(0.1)

    armpi.set_ready_flag(False)

    put_down_assembled_object()

    initMove()


def process_second_robot(armpi, ready_publisher, finish_publisher, pos_publisher, executor):
    x, y, angle, rotation_direction = calculate_position_and_angle()

    # found no object in the field
    if (x == -1 and y == -1):
        finish_publisher.send_msg()
        executor.execute_shutdown()
        return

    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction)
    go_to_waiting_position(armpi.get_ID())

    # signal to the other robot that this robot is ready
    ready_publisher.send_msg()
    while (not armpi.get_ready_flag()):

        if armpi.get_finish_flag():
            end_scenario(executor, x, y, angle, rotation_direction)
            return

        ready_publisher.send_msg()
        time.sleep(1)
    
    armpi.set_ready_flag(False)

    while (not armpi.get_got_position_flag()):
        time.sleep(0.1)

    armpi.set_got_position_flag(False)

    (x, y, z, angle) = armpi.get_position_with_angle()

    assemble_objects(x, y, z, angle)
    move_back(x, z, angle)

    # send to the next robot that it can proceed
    ready_publisher.send_msg()


def create_all_nodes(armpi):
    ready_publisher = create_ready_publisher_node(armpi)
    finish_publisher = create_finish_publisher_node(armpi)
    pos_publisher = create_pos_publisher_node(armpi)
    ready_subscriber = create_ready_subscriber_node(armpi)
    finish_subscriber = create_finish_subscriber_node(armpi)
    pos_subscriber = create_pos_subscriber_node(armpi)

    publisher_nodes = [ready_publisher, finish_publisher, pos_publisher]
    subscriber_nodes = [ready_subscriber, finish_subscriber, pos_subscriber]
    all_nodes = publisher_nodes + subscriber_nodes

    return publisher_nodes, subscriber_nodes, all_nodes


def main():
    #TODO scenarioID for horizontal or vertical
    ID, scenarioID = read_all_arguments()

    armpi = ArmPi(ID)

    initMove()

    publisher_nodes_list, subscriber_nodes_list, all_nodes_list = create_all_nodes(armpi)
    ready_publisher = publisher_nodes_list[0]
    finish_publisher = publisher_nodes_list[1]
    pos_publisher = publisher_nodes_list[2]

    executor = MultiExecutor(subscriber_nodes_list)

    # start the executor in a thread for spinning all subscriber nodes
    thread = Thread(target=executor.start_spinning, args=())
    thread.start()

    while (True):
        if ID == 0:
            process_first_robot(armpi, ready_publisher, finish_publisher, pos_publisher, executor)
        else:
            process_second_robot(armpi, ready_publisher, finish_publisher, pos_publisher, executor)

        if executor.get_shutdown_status():
            for node in all_nodes_list:
                node.destroy_node()

            thread.join()
            break



if __name__ == '__main__':
    #try:
    main()
        #raise Exception("Useless exception")
    #except Exception as e:
        #print(f"Catch my own Exception: {e}")