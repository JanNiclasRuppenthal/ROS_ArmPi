import rclpy
from rclpy.executors import MultiThreadedExecutor


from std_srvs.srv import Trigger

from visual_processing.srv import SetParam
from visual_processing.msg import Result
from armpi_pro_service_client.client import call_service

from robot.armpi import ArmPi

import time
import sys
from threading import Thread
import copy

rclpy.init()

from movement.mobile.pipes.grab import set_master_node_grabbing, grab_init_move, get_grabbing_node, detect_pipe, set_grab_robot_id
from movement.mobile.pipes.assembly import *
from movement.mobile.drive import set_allow_buzzer, set_armpi, set_master_node_driving, drive_init_move, start_to_drive, get_driving_node, reached_the_next_stationary_robot, drive_forward, drive_backward, rotate_90_deg_right, rotate_90_deg_left, park, set_id_list_for_driving, drive_away_from_robot
from robot.subscriber.holding_subscriber import create_holding_subscriber_node
from robot.subscriber.assembly_order_subscriber import create_assembly_order_subscriber_node
from robot.subscriber.assembly_step_subscriber import create_assembly_step_subscriber_node
from robot.subscriber.finish_subscriber import create_finish_subscriber_node

from common_executor.executor_subscriptions import MultiExecutor

node = rclpy.create_node('main_transport')

def read_argument():
    number_of_stationary_robots = int(sys.argv[1])
    beep = bool(int(sys.argv[2]))
    return number_of_stationary_robots, beep

def process_scenario(armpi, executor):

    while not armpi.get_assembly_order_status():

        print("Waiting")

        if armpi.get_finish_flag():
            print("Exit the visual_processing")
            call_service(node, Trigger, '/visual_processing/exit', Trigger.Request())
            print("I can park now")
            grab_init_move()
            park()
            executor.execute_shutdown()
            return
        
        time.sleep(0.5)

    armpi.set_assembly_order_status(False)

    set_id_list_for_driving(copy.deepcopy(armpi.get_IDList()))

    print("I got a list!")

    drive_init_move()
    start_to_drive()

    print("Driving")

    while not reached_the_next_stationary_robot():
        time.sleep(0.5)
    
    next_id = armpi.pop_IDList()
    set_grab_robot_id(next_id)

    # Grabbing the pipe
    grab_init_move()
    drive_forward(1)
    
    detect_pipe()

    print("Waiting until I can drive away.")
    while armpi.get_first_robot_hold_pipe():
        time.sleep(0.5)

    armpi.reset_first_robot_hold_pipe()

    print("Drive backwards and rotate!")

    #drive_backward(3.5)
    #rotate_90_deg_right()
    drive_away_from_robot(next_id)

    while not armpi.is_empty_IDList():

        drive_init_move()
        start_to_drive()

        next_id = armpi.pop_IDList()

        while not reached_the_next_stationary_robot():
            time.sleep(0.5)

        print("reached the next robot")

        assembly_init_move()
        drive_forward(1.2)

        #send message to stationary robot
        print("send message!")
        notify_stationary_robot_for_the_next_assembly_step(next_id)

        #wait for position
        while not got_position():
            time.sleep(0.5)

        print("Got position!")

        print("move arm up")
        # go from desired position up
        move_arm_up()

        notify_stationary_robot_for_the_next_assembly_step(1)

        print("now wait until stationary robot moved")
        # wait until robot reached (0, 20)

        while not armpi.get_permission_to_do_next_assembly_step():
            time.sleep(0.5)

        armpi.set_permission_to_do_next_assembly_step(False)

        print("move arm down")
        # arm goes down
        move_arm_down()

        print("open claw")
        # open claw
        open_claw()

        grab_init_move()

        notify_stationary_robot_for_the_next_assembly_step(next_id)

        # drive away
        #drive_backward(3.5)
        #rotate_90_deg_left()
        drive_away_from_robot(next_id)

    drive_init_move()
    start_to_drive()

    while not reached_the_next_stationary_robot():
        time.sleep(0.5)
        print("waiting for reaching kreuz")

def main():
    global node
    number_of_stationary_robots, beep = read_argument()
    armpi = ArmPi(0, number_of_stationary_robots)

    set_allow_buzzer(beep)
    set_armpi(armpi)

    list_subscriber_nodes = [
        get_driving_node(),
        get_grabbing_node(),
        get_assembly_node(),
        create_holding_subscriber_node(armpi),
        create_assembly_order_subscriber_node(armpi),
        create_assembly_step_subscriber_node(armpi),
        create_finish_subscriber_node(armpi)
    ]

    executor = MultiExecutor(list_subscriber_nodes)

    thread = Thread(target=executor.start_spinning, args=())
    thread.start()
  
    grab_init_move()
    
    set_master_node_driving(node)
    set_master_node_grabbing(node)

    call_service(node, Trigger, '/visual_processing/enter', Trigger.Request())

    while True:
        process_scenario(armpi, executor)

        if executor.get_shutdown_status():
            for node in list_subscriber_nodes:
                node.destroy_node()

            thread.join()
            break


if __name__ == '__main__':
    main()