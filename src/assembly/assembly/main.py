import sys
import time
from threading import Thread

import rclpy

import rclpy.context
from robot.publish import create_publisher_node
from robot.subscribe import start_subscriber_node, destroy_subscriber_node

from util.coordinates import get_coordinates
from util.deliver import initMove, deliver

def read_all_arguments():
    ID = int(sys.argv[1])
    last_robot = bool(sys.argv[2])

    return ID, last_robot


def main():
    ID, last_robot = read_all_arguments()
    first_start = ID == 0


    rclpy.init()
    publisher = create_publisher_node(ID, last_robot)
    # start the subscriber node in a thread
    #thread = Thread(target=start_subscriber_node)
    #thread.start()

    initMove()
    time.sleep(2)

    #wait until you get message
    
    world_X, world_Y = get_coordinates()
    deliver(world_X, world_Y, last_robot)
    
    initMove()  # back to initial position
    time.sleep(1.5)

    #publish message
    publisher.send_msgs()

    #destroy_subscriber_node()


if __name__ == '__main__':
    main()
