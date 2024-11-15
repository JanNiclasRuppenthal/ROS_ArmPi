import sys
import time
from threading import Thread

import rclpy

import rclpy.context
from robot.publisher.delivery_publisher import create_delivery_publisher_node
from robot.publisher.finish_publisher import create_finish_publisher_node
from robot.subscriber.delivery_subscriber import create_delivery_subscriber_node
from robot.subscriber.finish_subscriber import create_finish_subscriber_node
from robot.armpi import ArmPi
from common_executor.executor_subscriptions import MultiExecutor
from movement.stationary.cubes.coordinates import get_coordinates
from movement.stationary.cubes.deliver import init_move, deliver

from util.cam import Cam

def read_all_arguments():
    ID = int(sys.argv[1])
    last_robot = bool(int(sys.argv[2]))

    return ID, last_robot

def main():
    ID, last_robot = read_all_arguments()
    armpi = ArmPi(ID, last_robot)
    first_start = ID == 0

    rclpy.init()
    delivery_publisher = create_delivery_publisher_node(armpi)
    finish_publisher = create_finish_publisher_node(armpi)
    delivery_subscriber = create_delivery_subscriber_node(armpi)
    finish_subscriber = create_finish_subscriber_node(armpi)

    subscriber_nodes = [delivery_subscriber, finish_subscriber]
    executor = MultiExecutor(subscriber_nodes)

    thread = Thread(target=executor.start_spinning)
    thread.start()

    cam = Cam()
    cam.open()

    init_move()
    time.sleep(2)

    while (True):
        if ((armpi.get_finish_flag() or ID == 0) and (-1, -1) == get_coordinates(cam)):
            #finish here
            finish_publisher.send_msgs()
            executor.execute_shutdown()
            cam.shutdown()
            break

        if (armpi.get_delivery_flag() or first_start):

            if (first_start):
                first_start = False
        
            world_X, world_Y = get_coordinates(cam)

            if (world_X != -1 and world_Y != -1):
                deliver(world_X, world_Y, last_robot)
                
                init_move()  # back to initial position
                time.sleep(1.5)

                #publish message
                delivery_publisher.send_msgs()
                armpi.set_delivery_flag(False)

if __name__ == '__main__':
    main()