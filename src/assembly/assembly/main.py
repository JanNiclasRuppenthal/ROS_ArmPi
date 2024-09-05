import sys
import time
from threading import Thread

import rclpy

import rclpy.context
from robot.publish import create_publisher_node
from robot.finish_publisher import create_finish_publisher_node
from robot.subscribe import create_subscriber_node
from robot.finish_subscriber import create_finish_subscriber_node
from robot.armpi import ArmPi

from util.coordinates import get_coordinates
from util.deliver import initMove, deliver
from util.cam import Cam

def read_all_arguments():
    ID = int(sys.argv[1])
    last_robot = bool(int(sys.argv[2]))

    return ID, last_robot

def start_spinning(executor):
    executor.spin()

def main():
    ID, last_robot = read_all_arguments()
    armpi = ArmPi(ID, last_robot)
    first_start = ID == 0

    rclpy.init()
    publisher = create_publisher_node(armpi)
    finish_publisher = create_finish_publisher_node(armpi)
    subscriber = create_subscriber_node(armpi)
    finish_subscriber = create_finish_subscriber_node(armpi)

    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(subscriber)
    executor.add_node(finish_subscriber)

    thread = Thread(target=start_spinning, args=(executor, ))
    thread.start()

    cam = Cam()
    cam.open()

    initMove()
    time.sleep(2)

    while (True):
        if ((armpi.get_finish_flag() or ID == 0) and (-1, -1) == get_coordinates(cam)):
            #finish here
            finish_publisher.send_msgs()
            executor.shutdown()
            rclpy.shutdown()
            break

        if (armpi.get_delivery_flag() or first_start):
            armpi.set_delivery_flag(False)

            if (first_start):
                first_start = False
        
            world_X, world_Y = get_coordinates(cam)

            if (world_X == -1 and world_Y == -1):
                continue

            deliver(world_X, world_Y, last_robot)
            
            initMove()  # back to initial position
            time.sleep(1.5)

            #publish message
            publisher.send_msgs()

    cam.shutdown()

if __name__ == '__main__':
    main()