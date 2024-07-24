import sys

import rclpy.executors
sys.path.append('/home/pi/ArmPi/')

import time

from threading import Thread

import rclpy

from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from robot.armpi import ArmPi
from robot.publish import create_ready_publisher_node, create_pos_publisher_node
from robot.subscribe import create_ready_subscriber_node, create_pos_subscriber_node

AK = ArmIK()

def initMove():
    Board.setBusServoPulse(1, 500 - 50, 300)
    Board.setBusServoPulse(2, 500, 500)
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)

def read_all_arguments():
    ID = int(sys.argv[1])
    scenarioID = int(sys.argv[2])

    return ID, scenarioID

def open_claw():
    Board.setBusServoPulse(1, 200, 500)
    time.sleep(0.5)

def grab_the_object():
    # Go to the position of the object with z = 7
    result = AK.setPitchRangeMoving((0, 12.5, 7), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    open_claw()

    # Go to the position of the object with z = 1
    result = AK.setPitchRangeMoving((0, 12.5, 1), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    #close the claw
    Board.setBusServoPulse(1, 575, 500)
    time.sleep(0.5)

def go_to_waiting_position(ID):
    # Go up again (waiting-position)
    # ID = 0 -> z = 10
    # ID = 1 -> z = 20
    result = AK.setPitchRangeMoving((0, 12.5, 10 + ID*10), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

def process_first_robot(armpi, ready_publisher, pos_publisher):
    grab_the_object() #TODO: get the position of the object with the camera
    go_to_waiting_position(armpi.get_ID())

    # Go into the right position
    result = AK.setPitchRangeMoving((0, 28, 10), 10, 10, 0)
    time.sleep(result[2]/1000) 
    print(result)

    #TODO: Replace the coordinates with the estimated coordinates from the camera
    pos_publisher.send_msg(0.0, 28.0, 10.0, 10)

    while (not armpi.get_ready_flag()):
        time.sleep(0.1)

    print("Do something")


def process_second_robot(armpi, ready_publisher, pos_publisher):
    grab_the_object()
    go_to_waiting_position(armpi.get_ID())

    while (not armpi.get_got_position_flag()):
        time.sleep(0.1)

    (x, y, z, angle) = armpi.get_position_with_angle()
    
    # set the z value a little bit higher so there is no contact between these two objects
    z += 12
    result = AK.setPitchRangeMoving((x, y, z), angle, angle, 0)
    time.sleep(result[2]/1000) 
    print(result)

    time.sleep(1)

    result = AK.setPitchRangeMoving((x, y, z - 6), angle, angle, 0)
    time.sleep(result[2]/1000) 
    print(result)

    open_claw()

    # go to the init position again
    initMove()


    #TODO: Send message to another robot
    ready_publisher.send_msg()



def main():

    ID, scenarioID = read_all_arguments()

    armpi = ArmPi(ID)

    initMove()
    time.sleep(2)

    rclpy.init()
    ready_publisher = create_ready_publisher_node(armpi)
    pos_publisher = create_pos_publisher_node(armpi)
    ready_subscriber = create_ready_subscriber_node(armpi)
    pos_subscriber = create_pos_subscriber_node(armpi)

    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(ready_subscriber)
    executor.add_node(pos_subscriber)

    # start all the subscriber node in a thread
    thread_ready = Thread(target=ready_subscriber.get_correct_message)
    thread_ready.start()

    if ID == 0:
        process_first_robot(armpi, ready_publisher, pos_publisher)
    else:
        process_second_robot(armpi, ready_publisher, pos_publisher)



if __name__ == '__main__':
    main()