import time

from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from object_detection.object_type import ObjectType
import math

AK = ArmIK()

#TODO: Differentiate between grabbing and assembling

grab_pulse_ID_0 = {
    ObjectType.SMALL : 600,
    ObjectType.MEDIUM : 500,
    ObjectType.LARGE : 400
}

grab_pulse_ID_1 = {
    ObjectType.SMALL : 650,
    ObjectType.MEDIUM : 575,
    ObjectType.LARGE : 450
}

def init_move():
    Board.setBusServoPulse(1, 500 - 50, 300)
    Board.setBusServoPulse(2, 500, 500)
    result = AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)
    time.sleep(result[2]/1000) 

def open_claw():
    Board.setBusServoPulse(1, 100, 500)
    time.sleep(0.5)

def __get_z_coordinate(object_type):
    result = 0
    if object_type == ObjectType.SMALL:
        result = 1.2
    else:
        result = 1.5
    
    return result

def __determine_pulse(ID, object_type):
    result = 0 
    
    if (ID == 0):
        result = grab_pulse_ID_0[object_type]
    else:
        result = grab_pulse_ID_1[object_type]

    return result

def __convert_angle_to_pulse(x, y, angle, rotation_direction):
    # We need to declare that the y-Axis has a degree of zero degreees and not 90 degrees
    # Because of that we need to subtract 90 to the result of atan2
    angle_from_origin_to_object = 90 - round(math.degrees(math.atan2(y, abs(x))), 1)

    # If the object has a positive x coordinate, then the servo needs to decrement its pulse
    # so that the arm is aligned with the x-axis
    if x > 0:
        angle_from_origin_to_object = -angle_from_origin_to_object

    calculated_angle = (angle_from_origin_to_object + rotation_direction * angle)
    pulse = int(500 + calculated_angle * (1000 / 240))
    return pulse

def grab_the_object(ID, x, y, angle, rotation_direction, object_type):
    # Go to the position of the object with z = 7
    result = AK.setPitchRangeMoving((x, y, 7), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    open_claw()

    Board.setBusServoPulse(2, __convert_angle_to_pulse(x, y, angle, rotation_direction), 500)
    time.sleep(0.8)

    # Go to the position of the object
    z = __get_z_coordinate(object_type)
    
    result = AK.setPitchRangeMoving((x, y, z), -90, -90, 0, 600)
    time.sleep(result[2]/1000) 
    print(result)

    grab_pulse = __determine_pulse(ID, object_type)

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

def go_to_delivery_position(id):
    height = 0
    if id == 0:
        height = 28
    elif id == 1:
        height = 26.5
    print(f"To height: {height}")
    result = AK.setPitchRangeMoving((0, 20, height), 5, 5, 15)
    time.sleep(result[2]/1000)
    print(result)

    # rotate the claw again
    Board.setBusServoPulse(2, 500, 500)
    time.sleep(0.8)

def move_back_from_delivery_position(id):
    height = 0
    if id == 0:
        height = 28
    elif id == 1:
        height = 26.5
    print(f"From height: {height}")
    result = AK.setPitchRangeMoving((0, 18, height), 5, 5, 15)
    time.sleep(result[2]/1000)
    print(result)

def move_down_from_delivery_position():
    result = AK.setPitchRangeMoving((0, 18, 20), 5, 5, 15)
    time.sleep(result[2]/1000)
    print(result)

def rotate_away_from_camera():
    Board.setBusServoPulse(6, 875, 800)
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

def move_back_to_y_25(x, z, angle):
    result = AK.setPitchRangeMoving((-x, 25, z - 6), angle, angle, 0)
    time.sleep(result[2]/1000) 
    print(result)

    # go to the init position again
    init_move()

def move_to_origin(height):
    result = AK.setPitchRangeMoving((0, 20, height), 10, 10, 20)
    time.sleep(result[2]/1000) 
    print(result)

def put_down_grabbed_object(x, y, angle, rotation_direction, object_type):
    # Go to the position of the object with z = 7
    result = AK.setPitchRangeMoving((x, y, 7), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    Board.setBusServoPulse(2, __convert_angle_to_pulse(x, y, angle, rotation_direction), 500)
    time.sleep(0.8)

    # Go to the position of the object
    z = __get_z_coordinate(object_type)

    result = AK.setPitchRangeMoving((x, y, z), -90, -90, 0, 600)
    time.sleep(result[2]/1000) 
    print(result)

    open_claw()

def __put_object_at(x, y, z, object_type):
    result = AK.setPitchRangeMoving((x, y, 12), 10, 10, -90) # ArmPi goes to the goal coordinates with z = 12
    time.sleep(result[2]/1000)

    AK.setPitchRangeMoving((x, y, z + 3), 10, 10, -90, 500) # ArmPi goes down to z = goal_coord_z + 3
    time.sleep(0.5)

    z = __get_z_coordinate(object_type)
    
    AK.setPitchRangeMoving((x, y, z), 10, 10, -90, 1000) # ArmPi is at the next coordinates
    time.sleep(0.8)

    open_claw()

    AK.setPitchRangeMoving((x, y, 12), 10, 10, -90, 800)
    time.sleep(0.8)

def put_down_assembled_object(object_type):
    # The goal position is the green field left to the robot
    goal_coord_x, goal_coord_y, goal_coord_z = (-15 + 0.5, 6 - 0.5,  1.5)
    __put_object_at(goal_coord_x, goal_coord_y, goal_coord_z, object_type)