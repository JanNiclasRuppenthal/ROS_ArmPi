import rclpy
from rclpy.executors import MultiThreadedExecutor


from std_srvs.srv import Trigger

from visual_processing.srv import SetParam
from armpi_pro_service_client.client import call_service

from robot.armpi import ArmPi

import time
from threading import Thread

rclpy.init()

from movement.mobile.pipes.grab import init_move, get_movement_node
from robot.subscriber.holding_subscriber import create_pos_subscriber_node

node = rclpy.create_node('main_transport')

def process_scenario(armpi):
    #TODO: Wait until the ArmPi Pro received the order of the stationary robots

    #TODO: Drive to the first robot 

    # Grabbing the pipe
    req = SetParam.Request()
    req.type = 'transport_scenario'
    call_service(node, SetParam, '/visual_processing/set_running', req)

    print("Waiting until I can drive away.")
    while armpi.get_first_robot_hold_pipe():
        time.sleep(0.5)

    armpi.reset_first_robot_hold_pipe()

    #TODO: Drive backwards
    print("Drive backwards!")

    #TODO: Drive to the next robot



def spinning_executor(armpi):
    print("Spinning")
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    executor.add_node(get_movement_node())
    executor.add_node(create_pos_subscriber_node(armpi))
    executor.spin()

def main():
    armpi = ArmPi(0)
    call_service(node, Trigger, '/visual_processing/enter', Trigger.Request())

    executor_thread = Thread(target=spinning_executor, args=(armpi,))
    executor_thread.start()
  
    init_move()
    time.sleep(4)

    process_scenario(armpi)



if __name__ == '__main__':
    main()