import sys
sys.path.append('/home/pi/ArmPi/')

import time
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
from robot.armpi import ArmPi

AK = ArmIK()

def initMove():
    Board.setBusServoPulse(1, 500 - 50, 300)
    Board.setBusServoPulse(2, 500, 500)
    AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)

def read_all_arguments():
    ID = int(sys.argv[1])
    scenarioID = int(sys.argv[2])

    return ID, scenarioID


def main():

    ID, scenarioID = read_all_arguments()
    armpi = ArmPi(ID)

    initMove()
    time.sleep(2)

    # Go to the position of the object with z = 7
    result = AK.setPitchRangeMoving((0, 12.5, 7), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    Board.setBusServoPulse(1, 200, 500)
    time.sleep(0.5)

    # Go to the position of the object with z = 1
    result = AK.setPitchRangeMoving((0, 12.5, 1), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)

    #close the claw
    Board.setBusServoPulse(1, 600, 500)
    time.sleep(0.5)

    # Go up again (waiting-position)
    result = AK.setPitchRangeMoving((0, 12.5, 10), -90, -90, 0)
    time.sleep(result[2]/1000) 
    print(result)



    # Go into the right position
    #result = AK.setPitchRangeMoving((0, 28, 10), 10, 10, 0)
    #time.sleep(result[2]/1000) 
    #print(result)

    #result = AK.setPitchRangeMoving((0, 28, 27), 20, 20, 0)
    #time.sleep(result[2]/1000) 
    #print(result)


if __name__ == '__main__':
    main()