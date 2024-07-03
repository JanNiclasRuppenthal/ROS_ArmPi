import sys
sys.path.append('/home/pi/ArmPi/')
import time
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board

AK = ArmIK()

size = (640, 480)
rotation_angle = 0
unreachable = False
servo1 = 500

def initMove():
    Board.setBusServoPulse(1, servo1 - 50, 300)
    Board.setBusServoPulse(2, 500, 500)
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)

def deliver(world_X, world_Y, last_robot=False):
    global unreachable
    global start_pick_up
    global rotation_angle
    
    # placement coordinate
    '''
    placement coordinate:
    normal: (-15 + 0.5, 6 - 0.5, 1.5)
    36.2 = 35.7 + 0.5 is unreachable 
    '''
    goal_coord_x, goal_coord_y, goal_coord_z = (-20 + 0.5, 6 - 0.5, 1.5) if (not last_robot) else (-15 + 0.5, 6 - 0.5, 1.5)
        
    # Remove to target postion, high is 6 cm, through return result to judge whether it can reach the specified location 
    # if the running time is not given，it is automatically calculated and returned by the result

    result = AK.setPitchRangeMoving((world_X, world_Y, 7), -90, -90, 0)  
    if result != False:
        time.sleep(result[2]/1000) # if it can reach to specified location, then get running time 

        servo2_angle = getAngle(world_X, world_Y, rotation_angle) # calculate angle at that the clamper gripper needs to rotate
        Board.setBusServoPulse(1, servo1 - 280, 500)  # claw open
        Board.setBusServoPulse(2, servo2_angle, 500) # rotate the second servo
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
            
        servo2_angle = getAngle(goal_coord_x, goal_coord_y, -90)
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

        initMove()  # back to initial position
        time.sleep(1.5)
    else:
        print("Could not reach the coordinates %s" % str(world_X, world_Y))