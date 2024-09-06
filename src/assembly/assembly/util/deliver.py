import sys
sys.path.append('/home/pi/ArmPi/')
import time
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
import math

from util.coordinates import get_detected_color, get_rotation_angle

AK = ArmIK()

size = (640, 480)
servo1 = 500
__x_cord = -30
__coordinates = {
        'red':   (__x_cord + 0.5, 12 - 0.5, 1.5),
        'green': (__x_cord + 0.5, 6 - 0.5,  1.5),
        'blue':  (__x_cord + 0.5, 0 - 0.5,  1.5)
    }

__coordinates_last = {
        'red':   (-15 + 0.5, 12 - 0.5, 1.5),
        'green': (-15 + 0.5, 6 - 0.5,  1.5),
        'blue':  (-15 + 0.5, 0 - 0.5,  1.5)
    }

__count_placed_colored_cubes = {
    'red':   0,
    'green': 0,
    'blue':  0
}

def initMove():
    Board.setBusServoPulse(1, servo1 - 50, 300)
    Board.setBusServoPulse(2, 500, 500)
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)

def __convert_angle_to_pulse(x, y, angle):
    # We need to declare that the y-Axis has a degree of zero degreees and not 90 degrees
    # Because of that we need to subtract 90 to the result of atan2
    angle_from_origin_to_object = 90 - round(math.degrees(math.atan2(y, abs(x))), 1)

    # If the object has a positive x coordinate, then the servo needs to decrement its pulse
    # so that the arm is aligned with the x-axis
    if x > 0:
        angle_from_origin_to_object = -angle_from_origin_to_object

    angle_right = angle 
    angle_left = angle - 90

    if abs(angle_right) < abs(angle_left):
        rotation_angle = abs(angle_right)
        rotation_direction = 1
    else:
        rotation_angle = abs(angle_left)
        rotation_direction = -1

    calculated_angle = (angle_from_origin_to_object + rotation_direction * rotation_angle)
    pulse = int(500 + calculated_angle * (1000 / 240))
    return pulse

def deliver(world_X, world_Y, last_robot):

    detected_color = get_detected_color()

    # placement coordinate
    '''
    placement coordinate:
    normal: (-15 + 0.5, y, 1.5)
    -35.2 = 35.7 + 0.5 is unreachable 
    '''
    goal_coordinates = __coordinates if (not last_robot) else __coordinates_last
    goal_coord_x, goal_coord_y, goal_coord_z = goal_coordinates[detected_color]

    if (last_robot):
        goal_coord_z += __count_placed_colored_cubes[detected_color] * 2.5
        
    # Remove to target postion, high is 6 cm, through return result to judge whether it can reach the specified location 
    # if the running time is not given，it is automatically calculated and returned by the result

    result = AK.setPitchRangeMoving((world_X, world_Y, 7), -90, -90, 0)  
    if result != False:
        time.sleep(result[2]/1000) # if it can reach to specified location, then get running time 

        Board.setBusServoPulse(1, servo1 - 280, 500)  # claw open
        servo2_pulse = __convert_angle_to_pulse(world_X, world_Y, get_rotation_angle())
        Board.setBusServoPulse(2, servo2_pulse, 500) # rotate the second servo
        time.sleep(0.5)
        
        AK.setPitchRangeMoving((world_X, world_Y, 1.5), -90, -90, 0, 1000) # ArmPi goes to the position of the detected cube
        time.sleep(1.5)

        Board.setBusServoPulse(1, servo1, 500)  # claw colsed
        time.sleep(0.8)

        Board.setBusServoPulse(2, 500, 500)
        AK.setPitchRangeMoving((world_X, world_Y, 12), -90, -90, 0, 1000)  # ArmPi Robot arm up
        time.sleep(1)

        result = AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, 12), -90, -90, 0) # ArmPi goes to the goal coordinates with z = 12
        time.sleep(result[2]/1000)
            
        servo2_angle = __convert_angle_to_pulse(goal_coord_x, goal_coord_y, -90)
        Board.setBusServoPulse(2, servo2_angle, 500)
        time.sleep(0.5)

        AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, goal_coord_z + 3), -90, -90, 0, 500) # ArmPi goes down to z = goal_coord_z + 3
        time.sleep(0.5)
        
        AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, goal_coord_z), -90, -90, 0, 1000) # ArmPi is at the next coordinates
        time.sleep(0.8)

        Board.setBusServoPulse(1, servo1 - 200, 500)  # gripper open，put down object 
        time.sleep(0.8)

        AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, 12), -90, -90, 0, 800)
        time.sleep(0.8)

        __count_placed_colored_cubes[detected_color] += 1
    else:
        print("Could not reach the coordinates %s" % str(world_X, world_Y))