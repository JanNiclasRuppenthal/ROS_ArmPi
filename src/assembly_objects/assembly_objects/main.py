import sys

import rclpy.executors
sys.path.append('/home/pi/ArmPi/')

import time

from threading import Thread

import rclpy

from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from robot.armpi import ArmPi
from robot.publish import create_ready_publisher_node, create_finish_publisher_node, create_pos_publisher_node
from robot.subscribe import create_ready_subscriber_node, create_finish_subscriber_node, create_pos_subscriber_node
from position_angle import calculate_position_and_angle

AK = ArmIK()
rclpy.init()
executor = rclpy.executors.MultiThreadedExecutor()
shutdown_status = False

def initMove():
    Board.setBusServoPulse(1, 500 - 50, 300)
    Board.setBusServoPulse(2, 500, 500)
    result = AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)
    time.sleep(result[2]/1000) 

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
    result = AK.setPitchRangeMoving((x, y, 1), -90, -90, 0, 600)
    time.sleep(result[2]/1000) 
    print(result)

    grab_pulse = 575 if ID == 0 else 450
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

    AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, goal_coord_z + 3), 10, 10, -90, 500) # ArmPi goes down to z = goal_coord_z + 3
    time.sleep(0.5)
    
    AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, goal_coord_z), 10, 10, -90, 1000) # ArmPi is at the next coordinates
    time.sleep(0.8)

    open_claw()

    AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, 12), 10, 10, -90, 800)
    time.sleep(0.8)

def process_first_robot(armpi, ready_publisher, finish_publisher, pos_publisher):
    global shutdown_status
    x, y, angle, rotation_direction = calculate_position_and_angle()

    # found no object in the field
    if (x == -1 and y == -1):
        finish_publisher.send_msg()
        executor.shutdown()
        shutdown_status = True
        return

    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction)
    go_to_waiting_position(armpi.get_ID())

    # signal to the other robot that this robot is ready
    ready_publisher.send_msg()
    while (not armpi.get_ready_flag()):

        if armpi.get_finish_flag():
            put_down_assembled_object()
            initMove()
            executor.shutdown()
            shutdown_status = True
            return

        ready_publisher.send_msg()
        time.sleep(1)
    
    armpi.set_ready_flag(False)

    # Go into the right position
    result = AK.setPitchRangeMoving((x, 30, 10), 10, 10, 0)
    time.sleep(result[2]/1000) 
    print(result)

    pos_publisher.send_msg(x, 30.0, 10.0, 10)

    while (not armpi.get_ready_flag()):
        time.sleep(0.1)

    armpi.set_ready_flag(False)

    put_down_assembled_object()

    initMove()


def process_second_robot(armpi, ready_publisher, finish_publisher, pos_publisher):
    global shutdown_status
    x, y, angle, rotation_direction = calculate_position_and_angle()

    # found no object in the field
    if (x == -1 and y == -1):
        finish_publisher.send_msg()
        executor.shutdown()
        shutdown_status = True
        return

    grab_the_object(armpi.get_ID(), x, y, angle, rotation_direction)
    go_to_waiting_position(armpi.get_ID())

    # signal to the other robot that this robot is ready
    ready_publisher.send_msg()
    while (not armpi.get_ready_flag()):

        if armpi.get_finish_flag():
            put_down_assembled_object()
            initMove()
            executor.shutdown()
            shutdown_status = True
            return

        ready_publisher.send_msg()
        time.sleep(1)
    
    armpi.set_ready_flag(False)

    while (not armpi.get_got_position_flag()):
        time.sleep(0.1)

    armpi.set_got_position_flag(False)

    (x, y, z, angle) = armpi.get_position_with_angle()
    
    # set the z value a little bit higher so there is no contact between these two objects
    z += 12

    # we need to mirror the x coordinate
    # because both robots face each other
    result = AK.setPitchRangeMoving((-x, y, z), angle, angle, 0)
    time.sleep(result[2]/1000) 
    print(result)

    time.sleep(1)

    result = AK.setPitchRangeMoving((-x, y, z - 6), angle, angle, 0)
    time.sleep(result[2]/1000) 
    print(result)

    open_claw()

    # move back to y = 25
    result = AK.setPitchRangeMoving((-x, 25, z - 6), angle, angle, 0)
    time.sleep(result[2]/1000) 
    print(result)

    # go to the init position again
    initMove()

    # send to the next robot that it can proceed
    ready_publisher.send_msg()

def spin_executor(executor, ready_subscriber, finish_subscriber, pos_subscriber):
    executor.add_node(ready_subscriber)
    executor.add_node(finish_subscriber)
    executor.add_node(pos_subscriber)

    executor.spin()

    try:
        #shutdown nodes an rclpy contex
        if ready_subscriber:
            ready_subscriber.destroy_node()
        if finish_subscriber:
            finish_subscriber.destroy_node()
        if pos_subscriber:
            pos_subscriber.destroy_node()
        rclpy.shutdown()
    except Exception as e:
        print("Here after shutdown")


def main():
    global shutdown_status
    #TODO scenarioID for horizontal or vertical
    ID, scenarioID = read_all_arguments()

    armpi = ArmPi(ID)

    initMove()

    ready_publisher = create_ready_publisher_node(armpi)
    finish_publisher = create_finish_publisher_node(armpi)
    pos_publisher = create_pos_publisher_node(armpi)
    ready_subscriber = create_ready_subscriber_node(armpi)
    finish_subscriber = create_finish_subscriber_node(armpi)
    pos_subscriber = create_pos_subscriber_node(armpi)


    # start the executor in a thread for spinning all subscriber nodes
    thread = Thread(target=spin_executor, args=(executor, ready_subscriber, finish_subscriber, pos_subscriber, ))
    thread.start()

    while (True):
        if ID == 0:
            process_first_robot(armpi, ready_publisher, finish_publisher, pos_publisher)
        else:
            process_second_robot(armpi, ready_publisher, finish_publisher, pos_publisher)

        if shutdown_status:
            thread.join()
            break



if __name__ == '__main__':
    #try:
    main()
        #raise Exception("Useless exception")
    #except Exception as e:
        #print(f"Catch my own Exception: {e}")