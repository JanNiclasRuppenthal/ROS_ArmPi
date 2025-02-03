import rclpy


from std_srvs.srv import Trigger

from armpi_pro_service_client.client import call_service

from .robot.armpi import ArmPi

import time
import sys
from threading import Thread
import copy

rclpy.init()

from movement.mobile.pipes.grab import set_master_node_grabbing, grab_init_move, get_grabbing_node, detect_pipe, set_grab_robot_id
from movement.mobile.pipes.assembly import *
from movement.mobile.drive import set_allow_buzzer, set_armpi, set_master_node_driving, drive_init_move, start_to_drive, get_driving_node, reached_the_next_stationary_robot, drive_forward, drive_backward, rotate_90_deg_right, rotate_90_deg_left, park, set_id_list_for_driving, drive_away_from_robot, rotate_180_deg
from .robot.subscriber.holding_subscriber import create_holding_subscriber_node
from .robot.subscriber.assembly_order_subscriber import create_assembly_order_subscriber_node
from .robot.subscriber.assembly_step_subscriber import create_assembly_step_subscriber_node
from .robot.subscriber.finish_subscriber import create_finish_subscriber_node
from .robot.publisher.assembly_queue_notify_publisher import create_notify_publisher_node

from common.executor.executor_subscriptions import MultiExecutor

node = rclpy.create_node('main_transport')
last_id = -1

def read_argument():
    number_of_stationary_robots = int(sys.argv[1])
    beep = bool(int(sys.argv[2]))
    return number_of_stationary_robots, beep

def process_scenario(armpi, executor, notify_publisher):
    global last_id

    while not armpi.get_assembly_order_status():

        if armpi.get_finish_flag():
            notify_publisher.send_msg()
            print("Exit the visual_processing")
            call_service(node, Trigger, '/visual_processing/exit', Trigger.Request())
            print("I can park now")

            if last_id != -1:
                grab_init_move()
                park()
            
            executor.execute_shutdown()
            return
        
        time.sleep(0.5)

    print("I got a list!")

    armpi.set_assembly_order_status(False)
    set_id_list_for_driving(copy.deepcopy(armpi.get_IDList()))

    next_id = armpi.pop_IDList()
    notify_publisher.send_msg()

    if next_id == last_id:
        print("Rotate 180 degrees!")
        rotate_180_deg()

    if (last_id == -1):
        drive_init_move()
    
    start_to_drive()

    print("Driving")

    while not reached_the_next_stationary_robot():
        time.sleep(0.5)
    
    set_grab_robot_id(next_id)

    grab_init_move()
    drive_forward(1)
    
    detect_pipe()

    print("Waiting until I can drive away.")
    while armpi.get_first_robot_hold_pipe():
        time.sleep(0.5)

    armpi.reset_first_robot_hold_pipe()

    print("Drive backwards and rotate!")

    drive_away_from_robot(next_id)

    while not armpi.is_empty_IDList():

        drive_init_move()
        start_to_drive()

        next_id = armpi.pop_IDList()

        while not reached_the_next_stationary_robot():
            time.sleep(0.5)

        print("reached the next robot")

        assembly_init_move()
        drive_forward(1.3)

        print("send message!")
        notify_stationary_robot_for_the_next_assembly_step(next_id)

        #wait for position
        while not got_position():
            time.sleep(0.5)

        print("Got position!")

        print("move arm up")
        move_arm_up()

        notify_stationary_robot_for_the_next_assembly_step(next_id)

        print("now wait until stationary robot moved")
        # wait until robot reached (0, 20)
        while not armpi.get_permission_to_do_next_assembly_step():
            time.sleep(0.5)

        armpi.set_permission_to_do_next_assembly_step(False)

        print("move arm down")
        move_arm_down()

        print("open claw")
        open_claw()

        grab_init_move()

        notify_stationary_robot_for_the_next_assembly_step(next_id)

        drive_away_from_robot(next_id)

        last_id = next_id

    drive_init_move()
    start_to_drive()

    while not reached_the_next_stationary_robot():
        time.sleep(0.5)

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

    notify_publisher = create_notify_publisher_node(armpi)

    list_publisher_nodes = [
        notify_publisher
    ]

    executor = MultiExecutor(list_subscriber_nodes)

    thread = Thread(target=executor.start_spinning, args=())
    thread.start()
  
    grab_init_move()
    
    set_master_node_driving(node)
    set_master_node_grabbing(node)

    call_service(node, Trigger, '/visual_processing/enter', Trigger.Request())

    while True:
        process_scenario(armpi, executor, notify_publisher)

        if executor.get_shutdown_status():
            for node in list_subscriber_nodes + list_publisher_nodes:
                node.destroy_node()

            thread.join()
            break


if __name__ == '__main__':
    main()