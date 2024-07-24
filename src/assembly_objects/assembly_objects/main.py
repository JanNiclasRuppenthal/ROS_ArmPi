import sys
sys.path.append('/home/pi/ArmPi/')

import time

from threading import Thread

import rclpy

from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from robot.armpi import ArmPi
from robot.publish import create_publisher_node
from robot.subscribe import create_subscriber_node

AK = ArmIK()

def initMove():
    Board.setBusServoPulse(1, 500 - 50, 300)
    Board.setBusServoPulse(2, 500, 500)
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)

def read_all_arguments():
    ID = int(sys.argv[1])
    scenarioID = int(sys.argv[2])

    return ID, scenarioID

def grab_the_object():
    # Go to the position of the object with z = 7
    result = AK.setPitchRangeMoving((0, 12.5, 7), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    Board.setBusServoPulse(1, 200, 500)
    time.sleep(0.5)

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

def process_first_robot(ID):
    armpi = ArmPi(ID)

    initMove()
    time.sleep(2)

    rclpy.init()
    publisher = create_publisher_node(armpi)
    subscriber = create_subscriber_node(armpi)

    # start the subscriber node in a thread
    thread = Thread(target=subscriber.get_correct_message)
    thread.start()

    grab_the_object() #TODO: get the position of the object with the camera
    go_to_waiting_position(ID)


    
    # Go into the right position
    result = AK.setPitchRangeMoving((0, 28, 10), 10, 10, 0)
    time.sleep(result[2]/1000) 
    print(result)

    #TODO: Replace the coordinates with the estimated coordinates from the camera
    publisher.send_msgs(0.0, 28.0, 10.0, 10)


def process_second_robot(ID):
    armpi = ArmPi(ID)

    initMove()
    time.sleep(2)

    rclpy.init()
    publisher = create_publisher_node(armpi)
    subscriber = create_subscriber_node(armpi)

    # start the subscriber node in a thread
    thread = Thread(target=subscriber.get_correct_message)
    thread.start()

    grab_the_object()
    go_to_waiting_position(ID)

    #result = AK.setPitchRangeMoving((0, 28, 22), 12, 12, 0) oder doch besser 10?
    #time.sleep(result[2]/1000) 
    #print(result)



def main():

    ID, scenarioID = read_all_arguments()

    if ID == 0:
        process_first_robot(ID)
    else:
        process_second_robot(ID)



if __name__ == '__main__':
    main()