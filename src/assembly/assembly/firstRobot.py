import sys
sys.path.append('/home/pi/ArmPi/')
import HiwonderSDK.Board as Board
from ArmIK.ArmMoveIK import *

from get_position import run_camera

AK = ArmIK()

def initMove():
    Board.setBusServoPulse(1, 450, 300)
    Board.setBusServoPulse(2, 500, 500)
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)


if __name__ == '__main__':
    initMove()
    

    print("run camera")
    run_camera()

