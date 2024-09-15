import sys
import time

from threading import Thread

import rclpy

from robot.armpi import ArmPi
from robot.publisher.done_publisher import create_done_publisher_node
from robot.publisher.finish_publisher import create_finish_publisher_node
from robot.publisher.position_publisher import create_pos_publisher_node
from robot.publisher.assemble_queue_publisher import create_assemble_queue_publisher_node
from robot.subscriber.done_subscriber import create_done_subscriber_node
from robot.subscriber.finish_subscriber import create_finish_subscriber_node
from robot.subscriber.position_subscriber import create_pos_subscriber_node
from robot.subscriber.assemble_queue_subscriber import create_assemble_queue_subscriber_node
from util.object_finder import ObjectFinder
from util.executor_subscriptions import MultiExecutor
from util.movement import *

rclpy.init()
object_id = 0

def read_all_arguments():
    ID = int(sys.argv[1])
    number_of_robots = int(sys.argv[2])
    return ID, number_of_robots

def end_scenario(executor, x, y, angle, rotation_direction, object_type):
    put_down_grabbed_object(x, y, angle, rotation_direction, object_type)
    initMove()
    executor.execute_shutdown()

def process_scenario(armpi, done_publisher, finish_publisher, pos_publisher, assemble_publisher, executor):
    global object_id
    obj_finder = ObjectFinder()
    obj_finder.calculate_object_parameters()
    x, y = obj_finder.get_position_of_ith_object(object_id)
    angle = obj_finder.get_angle_of_ith_object(object_id)
    rotation_direction = obj_finder.get_rotation_direction_of_ith_object(object_id)
    object_type = obj_finder.get_object_type_of_ith_object(object_id)
    number_of_objects = obj_finder.get_number_of_objects()

    # found no object in the field
    if (x == -1 and y == -1):
        finish_publisher.send_msg()
        executor.execute_shutdown()
        return
    
    # If one robot had already send a finish message
    if armpi.get_finish_flag():
        executor.execute_shutdown()
    
    armpi.set_object_type(object_type)
    armpi.set_number_of_objects(number_of_objects - 1 - object_id) # decrement the number because we grabbed one object already
    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction, object_type)
    go_to_waiting_position()

    while True:
        assemble_publisher.send_msg()

        while armpi.get_assemble_queue().count() != armpi.get_number_of_robots():

            if armpi.get_finish_flag():
                end_scenario(executor, x, y, angle, rotation_direction, object_type)
                return

            assemble_publisher.send_msg()
            time.sleep(1)

        armpi.get_assemble_queue().calculate_assemble_queue()
        if not armpi.get_assemble_queue().test_duplicates_in_queue():
            break


        armpi.set_assemble_queue_flag(False)
        dict_duplicates = armpi.get_assemble_queue().get_dict_with_duplicates()

        put_down_object = False
        for obj_type in ObjectType:
            if len(dict_duplicates[obj_type.value]) == 0:
                   continue
            
            '''
            Skip the first robot because is has the lowest number of objects in its view 
            and the lowest ID
            '''
            dict_duplicates[obj_type.value].pop(0)

            for id in [id for (id, num_obj) in dict_duplicates[obj_type.value]]:
                if id == armpi.get_ID():
                    put_down_object = True

        armpi.get_assemble_queue().reset()
        if put_down_object:
            put_down_grabbed_object(x, y, angle, rotation_direction, object_type)
            initMove()
            object_id += 1
            return

    
    if armpi.get_ID() == armpi.get_assemble_queue().first():
        (assemble_x, assemble_y, assemble_z, assemble_angle) = (x, 30, 10, 10)
        go_to_assemble_position(assemble_x, assemble_y, assemble_z, assemble_angle)
        pos_publisher.send_msg(float(assemble_x), float(assemble_y), float(assemble_z), assemble_angle)

        done_publisher.send_msg()

        while (not armpi.get_assemble_queue().empty()): # all robots are done
            time.sleep(0.1)

        put_down_assembled_object(object_type)
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

    armpi.get_assemble_queue().reset()
    object_id = 0


def create_all_nodes(armpi):
    done_publisher = create_done_publisher_node(armpi)
    finish_publisher = create_finish_publisher_node(armpi)
    pos_publisher = create_pos_publisher_node(armpi)
    assembly_queue_publisher = create_assemble_queue_publisher_node(armpi)
    done_subscriber = create_done_subscriber_node(armpi)
    finish_subscriber = create_finish_subscriber_node(armpi)
    pos_subscriber = create_pos_subscriber_node(armpi)
    assembly_queue_subscriber = create_assemble_queue_subscriber_node(armpi)

    publisher_nodes = [done_publisher , finish_publisher, pos_publisher, assembly_queue_publisher]
    subscriber_nodes = [done_subscriber, finish_subscriber, pos_subscriber, assembly_queue_subscriber]
    all_nodes = publisher_nodes + subscriber_nodes

    return publisher_nodes, subscriber_nodes, all_nodes


def main():
    ID, number_of_robots = read_all_arguments()

    armpi = ArmPi(ID, number_of_robots)

    initMove()

    publisher_nodes_list, subscriber_nodes_list, all_nodes_list = create_all_nodes(armpi)
    done_publisher = publisher_nodes_list[0]
    finish_publisher = publisher_nodes_list[1]
    pos_publisher = publisher_nodes_list[2]
    assemble_publisher = publisher_nodes_list[3]

    executor = MultiExecutor(subscriber_nodes_list)

    # start the executor in a thread for spinning all subscriber nodes
    thread = Thread(target=executor.start_spinning, args=())
    thread.start()

    while (True):
        process_scenario(armpi, done_publisher, finish_publisher, pos_publisher, assemble_publisher, executor)

        if executor.get_shutdown_status():
            for node in all_nodes_list:
                node.destroy_node()

            thread.join()
            break

if __name__ == '__main__':
    main()