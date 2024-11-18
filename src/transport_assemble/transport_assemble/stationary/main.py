import sys
import time

import rclpy
from rclpy.executors import MultiThreadedExecutor

from robot.armpi import ArmPi
from robot.subscriber.grabbed_subscriber import create_grabbed_subscriber_node
from robot.subscriber.assemble_queue_subscriber import create_assemble_queue_subscriber_node
from robot.publisher.holding_publisher import create_holding_publisher_node
from robot.publisher.assemble_queue_publisher import create_assemble_queue_publisher_node

from object_detection.stationary.pipe_detection import PipeDetection
from movement.stationary.pipes.grab import *

from threading import Thread

pipe_nr = 0

def read_all_arguments():
    ID = int(sys.argv[1])
    number_of_stationary_robots = int(sys.argv[2])
    return ID, number_of_stationary_robots

def process_scenario(armpi, assemble_publisher, holding_publisher):
    global pipe_nr

    pipe_detection = PipeDetection()
    pipe_detection.calculate_bottom_parameters()
    x, y = pipe_detection.get_position_of_ith_object(pipe_nr)
    angle = pipe_detection.get_angle_of_ith_object(pipe_nr)
    rotation_direction = pipe_detection.get_rotation_direction_of_ith_object(pipe_nr)
    object_type = pipe_detection.get_object_type_of_ith_object(pipe_nr)
    number_of_objects = pipe_detection.get_number_of_objects()

    #TODO: Terminate scenario if there are no objects in the field
    
    #TODO: Test if one robot has already terminate the scenario
    
    armpi.set_object_type(object_type)
    armpi.set_number_of_objects(number_of_objects - 1 - pipe_nr) # decrement the number because we grabbed one object already
    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction, object_type)


    '''TODO:
        - Wait until every registerd robot grabbed an object.
        - If one robot terminates, then put down the object.
        - Calculate the order of the robots based on the size of the grabbed pipes.
        - Implement the detection of duplicates
    '''

    while True:
        assemble_publisher.send_msg()

        while armpi.get_assemble_queue().count() != armpi.get_number_of_stationary_robots():

            '''TODO: End scenario here!
            if armpi.get_finish_flag():
                end_scenario(executor, x, y, angle, rotation_direction, object_type)
                return
            '''


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
            init_move()
            object_id += 1
            return
    
    #TODO: The robot has the bigger pipe
    if armpi.get_ID() == armpi.get_assemble_queue().first():
        #TODO: Send the assemble Queue to the ArmPi Pro!
        go_to_delivery_position()

        print("Wait until I can let go the pipe")
        while not armpi.need_to_let_go_pipe():
            time.sleep(0.5)

        time.sleep(2)

        armpi.set_letting_go_pipe(False)

        open_claw()
        move_down_from_delivery_position()
        init_move()

        print("ArmPi Pro can now drive away and my Job is done!")
        holding_publisher.send_msg()
    else:
        #TODO: Implement the assembly for the other robots

        pass

    #TODO: I may need to reset some variable like assemble_queue and the object_id
    armpi.get_assemble_queue().reset()
    pipe_nr = 0


#TODO: Use the package for the executor!
def spinning_executor(armpi):
    executor = MultiThreadedExecutor()
    executor.add_node(create_grabbed_subscriber_node(armpi))
    executor.add_node(create_assemble_queue_subscriber_node(armpi))
    executor.spin()


def main():
    ID, number_of_stationary_robots = read_all_arguments()

    armpi = ArmPi(ID, number_of_stationary_robots)

    init_move()

    rclpy.init()

    #TODO: Create all the required publisher
    assemble_publisher = create_assemble_queue_publisher_node(armpi)
    holding_publisher = create_holding_publisher_node(armpi)

    #TODO: start the executor with all the required subscriber
    executor_thread = Thread(target=spinning_executor, args=(armpi,))
    executor_thread.start()

    #while (True):
    process_scenario(armpi, assemble_publisher, holding_publisher)

        #TODO: Terminate the scenario if executor is shutdown


if __name__ == '__main__':
    main()