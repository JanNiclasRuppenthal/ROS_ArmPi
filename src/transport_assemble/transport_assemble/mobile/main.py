import rclpy
from rclpy.executors import MultiThreadedExecutor


from std_srvs.srv import Trigger

from visual_processing.srv import SetParam
from armpi_pro_service_client.client import call_service

from robot.armpi import ArmPi

import time
from threading import Thread

rclpy.init()

from movement.mobile.pipes.grab import grab_init_move, get_grabbing_node
from movement.mobile.drive import drive_init_move, get_driving_node, reached_the_next_stationary_robot, drive_forward, drive_backward, rotate_90_deg_right, rotate_90_deg_left
from robot.subscriber.holding_subscriber import create_holding_subscriber_node

node = rclpy.create_node('main_transport')

def process_scenario(armpi):
    #TODO: Wait until the ArmPi Pro received the order of the stationary robots

    #TODO: Drive to the first robot
    drive_init_move()
    req = SetParam.Request()
    req.type = 'line'
    req.color = 'frogtape'
    call_service(node, SetParam, '/visual_processing/set_running', req)

    #TODO: Wait until ArmPi Pro reached the end of a line
    while not reached_the_next_stationary_robot():
        time.sleep(0.5)

    # Grabbing the pipe
    grab_init_move()
    drive_forward(1)
    
    req = SetParam.Request()
    req.type = 'rectangle_detection'
    call_service(node, SetParam, '/visual_processing/set_running', req)

    print("Waiting until I can drive away.")
    while armpi.get_first_robot_hold_pipe():
        time.sleep(0.5)

    armpi.reset_first_robot_hold_pipe()

    #TODO: Drive backwards
    print("Drive backwards and rotate!")

    drive_backward(3)
    rotate_90_deg_right()

    #TODO: Drive to the next robot



def spinning_executor(armpi):
    print("Spinning")
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.add_node(get_driving_node())
    executor.add_node(get_grabbing_node())
    executor.add_node(create_holding_subscriber_node(armpi))
    executor.spin()

def main():
    armpi = ArmPi(0)

    executor_thread = Thread(target=spinning_executor, args=(armpi,))
    executor_thread.start()
  
    grab_init_move()
    call_service(node, Trigger, '/visual_processing/enter', Trigger.Request())

    process_scenario(armpi)



if __name__ == '__main__':
    main()