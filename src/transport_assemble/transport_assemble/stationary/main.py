import sys
import time

import rclpy
from rclpy.executors import MultiThreadedExecutor

from robot.armpi import ArmPi
from robot.subscriber.grabbed_subscriber import create_grabbed_subscriber_node
from robot.subscriber.assemble_queue_subscriber import create_assemble_queue_subscriber_node
from robot.subscriber.assembly_step_subscriber	 import create_assembly_step_subscriber_node
from robot.subscriber.finish_subscriber import create_finish_subscriber_node
from robot.subscriber.assembly_queue_notify_subscriber import create_notify_subscriber_node
from robot.publisher.assembly_position_publisher import create_assembly_position_publisher_node
from robot.publisher.holding_publisher import create_holding_publisher_node
from robot.publisher.assemble_queue_publisher import create_assemble_queue_publisher_node
from robot.publisher.assembly_order_publisher import create_assembly_order_publisher_node
from robot.publisher.assembly_step_publisher import create_assembly_step_publisher_node
from robot.publisher.finish_publisher import create_finish_publisher_node

from object_detection.stationary.pipe_detection import PipeDetection
from object_detection.stationary.yellow_grabber_detection import GrabberDetection
from movement.stationary.pipes.grab import *

from common_executor.executor_subscriptions import MultiExecutor


from threading import Thread

pipe_nr = 0

def read_all_arguments():
    ID = int(sys.argv[1])
    number_of_stationary_robots = int(sys.argv[2])
    return ID, number_of_stationary_robots

def determine_differece_for_movement(x, y):
    return x, y - 20

def convert_coordinates_from_cm_to_m(x, y):
    return x / 100, y / 100

def end_scenario(executor, x, y, angle, rotation_direction, object_type):
    put_down_grabbed_object(x, y, angle, rotation_direction, object_type)
    init_move()
    executor.execute_shutdown()


def process_scenario(armpi, assembly_queue_publisher, holding_publisher, assembly_position_publisher, assembly_order_publisher, assembly_step_publisher, finish_publisher, executor):
    global pipe_nr

    if armpi.get_finish_flag():
        executor.execute_shutdown()
        return

    pipe_detection = PipeDetection()
    pipe_detection.calculate_middle_parameters()
    x, y = pipe_detection.get_position_of_ith_object(pipe_nr)
    angle = pipe_detection.get_angle_of_ith_object(pipe_nr)
    rotation_direction = pipe_detection.get_rotation_direction_of_ith_object(pipe_nr)
    object_type = pipe_detection.get_object_type_of_ith_object(pipe_nr)
    number_of_objects = pipe_detection.get_number_of_objects()

    if x == -1 and y == -1:
        finish_publisher.send_msg()
        executor.execute_shutdown()
        return
    
    if armpi.get_finish_flag():
        executor.execute_shutdown()
        return
    
    armpi.set_object_type(object_type)
    armpi.set_number_of_objects(number_of_objects - 1 - pipe_nr) # decrement the number because we grabbed one object already
    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction, object_type)
    go_to_waiting_position()

    #TODO: Write this in an another workspace package
    while True:
        assembly_queue_publisher.send_msg()

        while armpi.get_assemble_queue().count() != armpi.get_number_of_stationary_robots():

            if armpi.get_finish_flag():
                end_scenario(executor, x, y, angle, rotation_direction, object_type)
                return          

            assembly_queue_publisher.send_msg()
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
            init_move()
            pipe_nr += 1
            return
    
    if armpi.get_ID() == armpi.get_assemble_queue().first():
    
        order_queue = armpi.get_assemble_queue().get_queue()

        while not armpi.did_transporter_received_list():
            assembly_order_publisher.send_msg(order_queue)
            time.sleep(0.5)
    
        armpi.set_transporter_received_list(False)

        go_to_delivery_position(armpi.get_ID())

        print("Wait until I can let go the pipe")
        while not armpi.need_to_let_go_pipe():
            time.sleep(0.5)

        time.sleep(2)

        armpi.set_letting_go_pipe(False)

        open_claw()

        print("ArmPi Pro can now drive away and my Job is done!")
        holding_publisher.send_msg()

        move_back_from_delivery_position(armpi.get_ID())
        move_down_from_delivery_position()
        init_move()

    else:

        while not armpi.did_transporter_received_list():
            time.sleep(0.5)
    
        armpi.set_transporter_received_list(False)

        rotate_away_from_camera()

        # wait until armpi pro reached camera

        print("now wait")
        while not armpi.get_permission_to_do_next_assembly_step():
            time.sleep(0.5)

        armpi.set_permission_to_do_next_assembly_step(False)

        grabber_detection = GrabberDetection()
        x, y = grabber_detection.calculate_middle_between_grabber()

        x, y = determine_differece_for_movement(x, y)
        x, y = convert_coordinates_from_cm_to_m(x, y)
        assembly_position_publisher.send_msg(x, y)

        print("Wait until ArmPi Pro moved its arm")
        # wait until ArmPi Pro moved its grabber away
        while not armpi.get_permission_to_do_next_assembly_step():
            time.sleep(0.5)

        armpi.set_permission_to_do_next_assembly_step(False)
    
        # go to assembly position (0, 20)
        move_to_origin(19)

        # notify ArmPi Pro
        assembly_step_publisher.send_msg()

        # wait until ArmPi Pro opened its claw and drove away
        while not armpi.get_permission_to_do_next_assembly_step():
            time.sleep(0.5)

        armpi.set_permission_to_do_next_assembly_step(False)

        # put the assembled object down
        put_down_assembled_object(object_type)

        init_move()

    #TODO: I may need to reset some variable like assemble_queue and the pipe_nr
    armpi.get_assemble_queue().reset()
    pipe_nr = 0


def main():
    ID, number_of_stationary_robots = read_all_arguments()

    armpi = ArmPi(ID, number_of_stationary_robots)

    init_move()

    rclpy.init()

    list_publisher_nodes = [
        create_assemble_queue_publisher_node(armpi),
        create_holding_publisher_node(armpi),
        create_assembly_position_publisher_node(armpi),
        create_assembly_order_publisher_node(armpi),
        create_assembly_step_publisher_node(armpi),
        create_finish_publisher_node(armpi)
    ]

    assembly_queue_publisher = list_publisher_nodes[0]
    holding_publisher = list_publisher_nodes[1]
    assembly_position_publisher = list_publisher_nodes[2]
    assembly_order_publisher = list_publisher_nodes[3]
    assembly_step_publisher = list_publisher_nodes[4]
    finish_publisher = list_publisher_nodes[5]

    list_subscriber_nodes = [
        create_grabbed_subscriber_node(armpi),
        create_notify_subscriber_node(armpi),
        create_assemble_queue_subscriber_node(armpi),
        create_assembly_step_subscriber_node(armpi),
        create_finish_subscriber_node(armpi)
    ]

    list_all_nodes = list_publisher_nodes + list_subscriber_nodes

    # start the executor in a thread for spinning all subscriber nodes
    executor = MultiExecutor(list_subscriber_nodes)

    thread = Thread(target=executor.start_spinning, args=())
    thread.start()


    while (True):
        process_scenario(armpi, assembly_queue_publisher, holding_publisher, assembly_position_publisher, assembly_order_publisher, assembly_step_publisher, finish_publisher, executor)

        if executor.get_shutdown_status():
            for node in list_all_nodes:
                node.destroy_node()

            thread.join()
            break


if __name__ == '__main__':
    main()