import time
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board



class Movement:
    def __init__(self, AK):
        self.__AK = AK

    def init_move(self):
        Board.setBusServoPulse(1, 450, 300)
        Board.setBusServoPulse(2, 500, 500)
        self.__AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)
        time.sleep(1.5)

    def are_coordinates_valid(self, x, y):
        return x != -1 and y != -1

    def _move_to_goal_coordinate(self, goal_coord_x, goal_coord_y, goal_coord_z):
        # ArmPi goes to the goal coordinates with z = 12
        result = self.__AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, 12), -90, -90, 0)
        time.sleep(result[2] / 1000)

        servo2_angle = getAngle(goal_coord_x, goal_coord_y, -90)
        Board.setBusServoPulse(2, servo2_angle, 500)
        time.sleep(0.5)

        # ArmPi goes down to z = goal_coord_z + 3
        self.__AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, goal_coord_z + 3), -90, -90, 0, 500)
        time.sleep(0.5)

        # ArmPi is at the next coordinates
        self.__AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, goal_coord_z), -90, -90, 0, 1000)
        time.sleep(0.8)

    def _move_arm_up(self, x, y, time_in_s):
        time_in_ms = int(time_in_s * 1000)
        self.__AK.setPitchRangeMoving((x, y, 12), -90, -90, 0, time_in_ms) # ArmPi Robot arm up
        time.sleep(time_in_s)