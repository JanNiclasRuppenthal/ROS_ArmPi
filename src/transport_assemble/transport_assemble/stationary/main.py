import sys
import time

import rclpy
from rclpy.executors import MultiThreadedExecutor

from robot.armpi import ArmPi
from robot.subscriber.grabbed_subscriber import create_grabbed_subscriber_node
from robot.publisher.holding_publisher import create_holding_publisher_node

from object_detection.stationary.pipe_detection import PipeDetection
from movement.stationary.pipes.grab import *

from threading import Thread

def read_all_arguments():
    ID = int(sys.argv[1])
    number_of_stationary_robots = int(sys.argv[2])
    return ID, number_of_stationary_robots

def process_scenario(armpi, holding_publisher):
    #TODO: Detect all pipes in the view
    pipe_detection = PipeDetection()
    pipe_detection.calculate_bottom_parameters()
    x, y = pipe_detection.get_position_of_ith_object(0)
    angle = pipe_detection.get_angle_of_ith_object(0)
    rotation_direction = pipe_detection.get_rotation_direction_of_ith_object(0)
    object_type = pipe_detection.get_object_type_of_ith_object(0)

    #TODO: Get the total number of objects in the view

    #TODO: Terminate scenario if there are no objects in the field
    
    #TODO: Test if one robot has already terminate the scenario
    
    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction, object_type)


    '''TODO:
        - Wait until every registerd robot grabbed an object.
        - If one robot terminates, then put down the object.
        - Calculate the order of the robots based on the size of the grabbed pipes.
        - Implement the detection of duplicates
    '''

    
    #TODO: Implement the assembly for the other robots
    
    #TODO: The robot has the bigger pipe
    if True:
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
        pass

    #TODO: I may need to reset some variable like assemble_queue and the object_id


#TODO: Use the package for the executor!
def spinning_executor(armpi):
    executor = MultiThreadedExecutor()
    executor.add_node(create_grabbed_subscriber_node(armpi))
    executor.spin()


def main():
    ID, number_of_stationary_robots = read_all_arguments()

    armpi = ArmPi(ID, number_of_stationary_robots)

    init_move()

    rclpy.init()

    #TODO: Create all the required publisher
    holding_publisher = create_holding_publisher_node(armpi)

    #TODO: start the executor with all the required subscriber
    executor_thread = Thread(target=spinning_executor, args=(armpi,))
    executor_thread.start()

    #while (True):
    process_scenario(armpi, holding_publisher)

        #TODO: Terminate the scenario if executor is shutdown


if __name__ == '__main__':
    main()