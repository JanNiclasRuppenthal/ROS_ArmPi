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
from position_angle import calculate_position_and_angle

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

def grab_the_object(ID, x, y, angle, rotation_direction):
    # Go to the position of the object with z = 7
    result = AK.setPitchRangeMoving((x, y, 7), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    open_claw()

    # calculate the difference from the computed pulse and 500
    servo2_angle_diff = abs(500 - getAngle(x, y, angle))
    
    # if it the object is right rotated the add the pulse to 500
    # else subtract the difference from 500
    servo2_angle_pulse = 500 + (rotation_direction * servo2_angle_diff)
    print(servo2_angle_pulse)
    Board.setBusServoPulse(2, servo2_angle_pulse, 500)
    time.sleep(0.8)

    # Go to the position of the object with z = 1
    result = AK.setPitchRangeMoving((x, y, 1), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    grab_pulse = 575 if (ID == 0) else 525
    #close the claw
    Board.setBusServoPulse(1, grab_pulse, 500)
    time.sleep(0.5)

def go_to_waiting_position(ID):
    # Go up again (waiting-position)
    # ID = 0 -> z = 10
    # ID = 1 -> z = 20
    result = AK.setPitchRangeMoving((0, 12.5, 10 + ID*10), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    # rotate the claw again
    Board.setBusServoPulse(2, 500, 500)
    time.sleep(0.8)

def put_down_assembled_object():
    # The goal position is the green field left to the robot
    goal_coord_x, goal_coord_y, goal_coord_z = (-15 + 0.5, 6 - 0.5,  1.5)

    result = AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, 12), 10, 10, -90) # ArmPi goes to the goal coordinates with z = 12
    time.sleep(result[2]/1000)
        
    #servo2_angle = getAngle(goal_coord_x, goal_coord_y, -90)
    #Board.setBusServoPulse(2, servo2_angle, 500)
    #time.sleep(0.5)

    AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, goal_coord_z + 3), 10, 10, -90, 500) # ArmPi goes down to z = goal_coord_z + 3
    time.sleep(0.5)
    
    AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, goal_coord_z), 10, 10, -90, 1000) # ArmPi is at the next coordinates
    time.sleep(0.8)

    open_claw()

    AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, 12), 10, 10, -90, 800)
    time.sleep(0.8)

def process_first_robot(armpi, ready_publisher, pos_publisher):
    x, y, angle, rotation_direction = calculate_position_and_angle()
    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction)
    go_to_waiting_position(armpi.get_ID())

    # Go into the right position
    result = AK.setPitchRangeMoving((x, y+12, 10), 10, 10, 0)
    time.sleep(result[2]/1000) 
    print(result)

    pos_publisher.send_msg(x, y+12, 10.0, 10)

    while (not armpi.get_ready_flag()):
        time.sleep(0.1)

    put_down_assembled_object()

    initMove()


def process_second_robot(armpi, ready_publisher, pos_publisher):
    x, y, angle, rotation_direction = calculate_position_and_angle()
    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction)
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

    # send to the next robot that it can proceed
    ready_publisher.send_msg()

def spin_executor(executor):
        executor.spin()


def main():
    #TODO scenarioID for horizontal or vertical
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

    # start the executor in a thread for spinning all subscriber nodes
    thread = Thread(target=spin_executor, args=(executor, ))
    thread.start()

    if ID == 0:
        process_first_robot(armpi, ready_publisher, pos_publisher)
    else:
        process_second_robot(armpi, ready_publisher, pos_publisher)



if __name__ == '__main__':
    main()