import time
import sys
sys.path.append('/home/pi/ArmPi/')
import HiwonderSDK.Board as Board
from ArmIK.ArmMoveIK import *


from coordinates import get_coordinates

AK = ArmIK()

def initMove():
    Board.setBusServoPulse(1, 450, 300)
    Board.setBusServoPulse(2, 500, 500)
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)


if __name__ == '__main__':
    initMove()
    time.sleep(2)
    
    print("run camera")
    world_X, world_Y = get_coordinates()

