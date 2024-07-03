import time

from coordinates import get_coordinates
from deliver import initMove, deliver





if __name__ == '__main__':
    initMove()
    time.sleep(2)
    
    print("run camera")
    world_X, world_Y = get_coordinates()
    deliver(world_X, world_Y)

