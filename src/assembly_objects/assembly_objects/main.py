import sys
sys.path.append('/home/pi/ArmPi/')

import time

from threading import Thread

import rclpy

from robot.armpi import ArmPi
from robot.publisher.ready_publisher import create_ready_publisher_node
from robot.publisher.done_publisher import create_done_publisher_node
from robot.publisher.end_publisher import create_end_publisher_node
from robot.publisher.position_publisher import create_pos_publisher_node
from robot.publisher.object_type_publisher import create_object_type_publisher_node
from robot.subscriber.ready_subscriber import create_ready_subscriber_node
from robot.subscriber.done_subscriber import create_done_subscriber_node
from robot.subscriber.end_subscriber import create_end_subscriber_node
from robot.subscriber.position_subscriber import create_pos_subscriber_node
from robot.subscriber.object_type_subscriber import create_object_type_subscriber_node
from util.position_angle import calculate_position_and_angle
from util.executor_subscriptions import MultiExecutor
from util.movement import *

rclpy.init()

def read_all_arguments():
    ID = int(sys.argv[1])
    number_of_robots = int(sys.argv[2])
    return ID, number_of_robots

def end_scenario(executor, x, y, angle, rotation_direction):
    put_down_grabbed_object(x, y, angle, rotation_direction)
    initMove()
    executor.execute_shutdown()

'''
def process_first_robot(armpi, ready_publisher, done_publisher, finish_publisher, pos_publisher, obj_publisher, executor):
    x, y, angle, rotation_direction, object_type = calculate_position_and_angle()

    # found no object in the field
    if (x == -1 and y == -1):
        finish_publisher.send_msg()
        executor.execute_shutdown()
        return

    armpi.set_object_type(object_type)
    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction)
    go_to_waiting_position(armpi.get_ID())

    # wait until every other robot has grabbed the object and is ready
    while (not armpi.get_ready_flag()):

        # end scenario if one robot could not find an object in its view
        if armpi.get_finish_flag():
            end_scenario(executor, x, y, angle, rotation_direction)
            return

        time.sleep(0.1)

    ready_publisher.send_msg()
    armpi.set_ready_flag(False)

    (assemble_x, assemble_y, assemble_z, assemble_angle) = (x, 30, 10, 10)
    go_to_assemble_position(assemble_x, assemble_y, assemble_z, assemble_angle)
    pos_publisher.send_msg(float(assemble_x), float(assemble_y), float(assemble_z), assemble_angle)
    done_publisher.send_msg()

    while (not armpi.get_done_flag()): # all robots are done
        time.sleep(0.1)

    armpi.set_done_flag(False)
    put_down_assembled_object()
    initMove()


def process_other_robot(armpi, ready_publisher, done_publisher, finish_publisher, executor):
    x, y, angle, rotation_direction, object_type = calculate_position_and_angle()

    # found no object in the field
    if (x == -1 and y == -1):
        finish_publisher.send_msg()
        executor.execute_shutdown()
        return

    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction)
    go_to_waiting_position(armpi.get_ID())

    # signal to the first robot that this robot is ready
    # and wait until the first robot is ready
    ready_publisher.send_msg()
    while (not armpi.get_ready_flag()):

        if armpi.get_finish_flag():
            end_scenario(executor, x, y, angle, rotation_direction)
            return

        ready_publisher.send_msg()
        time.sleep(1)
    
    armpi.set_ready_flag(False)

    while (not armpi.get_done_flag()):
        time.sleep(0.1)

    armpi.set_done_flag(False)

    (x, y, z, angle) = armpi.get_position_with_angle()

    # set the z value a little bit higher so there is no contact between these two objects
    z += 12
    assemble_objects(x, y, z, angle)
    move_back(x, z, angle)

    # send to the next robot that it can proceed
    done_publisher.send_msg()
'''


def process_scenario(armpi, ready_publisher, done_publisher, finish_publisher, pos_publisher, obj_publisher, executor):
    x, y, angle, rotation_direction, object_type = calculate_position_and_angle()

    # found no object in the field
    if (x == -1 and y == -1):
        finish_publisher.send_msg()
        executor.execute_shutdown()
        return

    armpi.set_object_type(object_type)
    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction, object_type)
    go_to_waiting_position()

    while True:
        obj_publisher.send_msg()

        while not armpi.get_object_type_flag():

            if armpi.get_finish_flag():
                end_scenario(executor, x, y, angle, rotation_direction)
                return

            obj_publisher.send_msg()
            time.sleep(1)

        if object_type != armpi.get_object_type_other_robot():
            break

        #TODO: implement the logic if the two types are the same

    armpi.set_object_type_flag(False)
    
    if object_type.value < armpi.get_object_type_other_robot().value:
        (assemble_x, assemble_y, assemble_z, assemble_angle) = (x, 30, 10, 10)
        go_to_assemble_position(assemble_x, assemble_y, assemble_z, assemble_angle)
        pos_publisher.send_msg(float(assemble_x), float(assemble_y), float(assemble_z), assemble_angle)

        done_publisher.send_msg()

        while (not armpi.get_done_flag()): # all robots are done
            time.sleep(0.1)

        armpi.set_done_flag(False)
        put_down_assembled_object()
        initMove()

    else:
        go_to_upper_position()
        while (not armpi.get_done_flag()):
            time.sleep(0.1)

        armpi.set_done_flag(False)

        (x, y, z, angle) = armpi.get_position_with_angle()

        # set the z value a little bit higher so there is no contact between these two objects
        z += 12
        assemble_objects(x, y, z, angle)
        move_back(x, z, angle)

        # send to the next robot that it can proceed
        done_publisher.send_msg()


def create_all_nodes(armpi):
    ready_publisher = create_ready_publisher_node(armpi)
    done_publisher = create_done_publisher_node(armpi)
    end_publisher = create_end_publisher_node(armpi)
    pos_publisher = create_pos_publisher_node(armpi)
    object_type_publisher = create_object_type_publisher_node(armpi)
    ready_subscriber = create_ready_subscriber_node(armpi)
    done_subscriber = create_done_subscriber_node(armpi)
    end_subscriber = create_end_subscriber_node(armpi)
    pos_subscriber = create_pos_subscriber_node(armpi)
    object_type_subscriber = create_object_type_subscriber_node(armpi)

    publisher_nodes = [ready_publisher, done_publisher , end_publisher, pos_publisher, object_type_publisher]
    subscriber_nodes = [ready_subscriber, done_subscriber, end_subscriber, pos_subscriber, object_type_subscriber]
    all_nodes = publisher_nodes + subscriber_nodes

    return publisher_nodes, subscriber_nodes, all_nodes


def main():
    ID, number_of_robots = read_all_arguments()

    armpi = ArmPi(ID, number_of_robots)

    initMove()

    publisher_nodes_list, subscriber_nodes_list, all_nodes_list = create_all_nodes(armpi)
    ready_publisher = publisher_nodes_list[0]
    done_publisher = publisher_nodes_list[1]
    finish_publisher = publisher_nodes_list[2]
    pos_publisher = publisher_nodes_list[3]
    obj_publisher = publisher_nodes_list[4]

    executor = MultiExecutor(subscriber_nodes_list)

    # start the executor in a thread for spinning all subscriber nodes
    thread = Thread(target=executor.start_spinning, args=())
    thread.start()

    while (True):
        '''
        if ID == 0:
            process_first_robot(armpi, ready_publisher, done_publisher, finish_publisher, pos_publisher, obj_publisher, executor)
        else:
            process_other_robot(armpi, ready_publisher, done_publisher, finish_publisher, executor) 
        '''
        

        process_scenario(armpi, ready_publisher, done_publisher, finish_publisher, pos_publisher, obj_publisher, executor)

        if executor.get_shutdown_status():
            for node in all_nodes_list:
                node.destroy_node()

            thread.join()
            break

if __name__ == '__main__':
    main()