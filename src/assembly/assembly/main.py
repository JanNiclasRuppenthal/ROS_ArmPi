import time
from threading import Thread

from robot.publish import start_publisher_node
from robot.subscribe import start_subscriber_node, destroy_subscriber_node

from util.coordinates import get_coordinates
from util.deliver import initMove, deliver





if __name__ == '__main__':
    # start the subscriber node in a thread
    thread = Thread(target=start_subscriber_node)
    thread.start()

    initMove()
    time.sleep(2)

    #wait unitl you get message
    
    world_X, world_Y = get_coordinates()
    deliver(world_X, world_Y)
    
    initMove()  # back to initial position
    time.sleep(1.5)

    #publish message
    start_publisher_node()

    #destroy_subscriber_node()
