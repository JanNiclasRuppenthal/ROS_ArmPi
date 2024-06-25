import sys
sys.path.append('/home/pi/ArmPi/')
import time

import HiwonderSDK.Board as Board
from ArmIK.ArmMoveIK import *

AK = ArmIK()

def initMove():
    Board.setBusServoPulse(1, 500, 300)
    Board.setBusServoPulse(2, 500, 500)
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)

def setBuzzer(timer):
    Board.setBuzzer(0)
    Board.setBuzzer(1)
    time.sleep(timer)
    Board.setBuzzer(0)

def dance(servo_id, start_pulse, middle_pulse, end_pulse, start_time, middle_time, end_time):
    Board.setBusServoPulse(servo_id, start_pulse, start_time)
    time.sleep(start_time/1000)
    Board.setBusServoPulse(servo_id, middle_pulse, middle_time)
    time.sleep(middle_time/1000)
    Board.setBusServoPulse(servo_id, end_pulse, end_time)
    time.sleep(1 + end_time/1000)
