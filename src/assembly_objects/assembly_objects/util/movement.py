import time

from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from util.object_type import ObjectType

AK = ArmIK()

grab_pulse_ID_01 = {
    ObjectType.SMALL : 575,
    ObjectType.MEDIUM : 500,
    ObjectType.LARGE : 400
}

grab_pulse_ID_02 = {
    ObjectType.SMALL : 650,
    ObjectType.MEDIUM : 575,
    ObjectType.LARGE : 450
}

def initMove():
    Board.setBusServoPulse(1, 500 - 50, 300)
    Board.setBusServoPulse(2, 500, 500)
    result = AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)
    time.sleep(result[2]/1000) 

def open_claw():
    Board.setBusServoPulse(1, 200, 500)
    time.sleep(0.5)

def grab_the_object(ID, x, y, angle, rotation_direction, object_type):
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

    grab_pulse = 0 
    
    if (ID == 0):
        grab_pulse = grab_pulse_ID_01[object_type]
    else:
        grab_pulse = grab_pulse_ID_02[object_type]

    #close the claw
    Board.setBusServoPulse(1, grab_pulse, 500)
    time.sleep(0.5)

def go_to_waiting_position():
    # Go up again (waiting-position)
    result = AK.setPitchRangeMoving((0, 12.5, 10), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    # rotate the claw again
    Board.setBusServoPulse(2, 500, 500)
    time.sleep(0.8)

def go_to_assemble_position(x, y, z, angle):
    # Go into the right position
    result = AK.setPitchRangeMoving((x, y, z), angle, angle, 0)
    time.sleep(result[2]/1000) 
    print(result)

def go_to_upper_position():
    result = AK.setPitchRangeMoving((0, 12.5, 20), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

def assemble_objects(x, y, z, angle):
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

def move_back(x, z, angle):
    # move back to y = 25
    result = AK.setPitchRangeMoving((-x, 25, z - 6), angle, angle, 0)
    time.sleep(result[2]/1000) 
    print(result)

    # go to the init position again
    initMove()

def put_down_grabbed_object(x, y, angle, rotation_direction):
    # Go to the position of the object with z = 7
    result = AK.setPitchRangeMoving((x, y, 7), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

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

    open_claw()



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