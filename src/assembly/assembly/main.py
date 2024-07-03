import time

from util.coordinates import get_coordinates
from util.deliver import initMove, deliver





if __name__ == '__main__':
    initMove()
    time.sleep(2)

    #wait unitl you get message
    
    world_X, world_Y = get_coordinates()
    deliver(world_X, world_Y)

    #publish message
    
    initMove()  # back to initial position
    time.sleep(1.5)

