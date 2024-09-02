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
from robot.publisher.assembly_queue_publisher import create_assembly_queue_publisher_node
from robot.subscriber.ready_subscriber import create_ready_subscriber_node
from robot.subscriber.done_subscriber import create_done_subscriber_node
from robot.subscriber.end_subscriber import create_end_subscriber_node
from robot.subscriber.position_subscriber import create_pos_subscriber_node
from robot.subscriber.assembly_queue_subscriber import create_assembly_queue_subscriber_node
from util.object_finder import ObjectFinder
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

def process_scenario(armpi, ready_publisher, done_publisher, finish_publisher, pos_publisher, assemble_publisher, executor):
    obj_finder = ObjectFinder()
    obj_finder.calculate_object_parameters()
    x, y = obj_finder.get_position()
    angle = obj_finder.get_angle()
    rotation_direction = obj_finder.get_rotation_direction()
    object_type = obj_finder.get_object_type()
    number_of_objects = obj_finder.get_number_of_objects()

    # found no object in the field
    if (x == -1 and y == -1):
        finish_publisher.send_msg()
        executor.execute_shutdown()
        return
    
    armpi.get_assemble_queue().add_id_object_type_value(armpi.get_ID(), object_type.value)
    armpi.set_object_type(object_type)
    armpi.set_number_of_objects(number_of_objects - 1) # decrement the number because we grabbed one object already
    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction, object_type)
    go_to_waiting_position()

    while True:
        assemble_publisher.send_msg()

        while not armpi.get_assemble_queue_flag():

            if armpi.get_finish_flag():
                end_scenario(executor, x, y, angle, rotation_direction)
                return

            assemble_publisher.send_msg()
            time.sleep(1)

        armpi.get_assemble_queue().calculate_assemble_queue()
        if not armpi.get_assemble_queue().test_duplicates_in_queue():
            break

        # The assemble queue contains duplicates
        if armpi.get_number_of_objects() > armpi.get_number_of_objects_next_robot():
            # put the object to the depot
            put_object_to_depot() #TODO: it would be better if the robot puts it down and grabs the next object
            return
        elif armpi.get_number_of_objects() > armpi.get_number_of_objects_next_robot():
            if armpi.get_ID() == 1: #TODO: If the robot has a higher ID
                # put the object to the depot
                put_object_to_depot()
                return
        else:
            armpi.set_assemble_queue_flag(False)


    armpi.set_assemble_queue_flag(False)
    
    if armpi.get_ID() == armpi.get_assemble_queue().first():
        (assemble_x, assemble_y, assemble_z, assemble_angle) = (x, 30, 10, 10)
        go_to_assemble_position(assemble_x, assemble_y, assemble_z, assemble_angle)
        pos_publisher.send_msg(float(assemble_x), float(assemble_y), float(assemble_z), assemble_angle)

        done_publisher.send_msg()

        while (not armpi.get_assemble_queue().empty()): # all robots are done
            time.sleep(0.1)

        put_down_assembled_object()
        initMove()

    else:
        go_to_upper_position()
        while (not armpi.get_ID() == armpi.get_assemble_queue().first()):
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
    assembly_queue_publisher = create_assembly_queue_publisher_node(armpi)
    ready_subscriber = create_ready_subscriber_node(armpi)
    done_subscriber = create_done_subscriber_node(armpi)
    end_subscriber = create_end_subscriber_node(armpi)
    pos_subscriber = create_pos_subscriber_node(armpi)
    assembly_queue_subscriber = create_assembly_queue_subscriber_node(armpi)

    publisher_nodes = [ready_publisher, done_publisher , end_publisher, pos_publisher, assembly_queue_publisher]
    subscriber_nodes = [ready_subscriber, done_subscriber, end_subscriber, pos_subscriber, assembly_queue_subscriber]
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
    assemble_publisher = publisher_nodes_list[4]

    executor = MultiExecutor(subscriber_nodes_list)

    # start the executor in a thread for spinning all subscriber nodes
    thread = Thread(target=executor.start_spinning, args=())
    thread.start()

    while (True):
        process_scenario(armpi, ready_publisher, done_publisher, finish_publisher, pos_publisher, assemble_publisher, executor)

        if executor.get_shutdown_status():
            for node in all_nodes_list:
                node.destroy_node()

            thread.join()
            break

if __name__ == '__main__':
    main()