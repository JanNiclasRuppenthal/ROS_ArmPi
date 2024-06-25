import time
import sys
sys.path.append('/home/pi/ArmPi/')

import HiwonderSDK.Board as Board
from .move import dance, initMove

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

values = [
    (1, 0, 1000, 500, 500, 1000, 1000),
    (2, 0, 1000, 500, 500, 1000, 1000),
    (3, 400, 1000, 500, 500, 1000, 1000),
    (4, 500, 1000, 500, 1000, 2000, 1000),
    (5, 300, 800, 500, 3000, 3000, 1000),
    (6, 0, 1000, 500, 2000, 4000, 1000)
]


class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'dance', 10)
        #timer_period = 0.5  # seconds
        #self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 1

    def timer_callback(self):
        msg = String()
        temp = Board.getBusServoTemp(self.i)
        #msg.data = 'My temp for servo %d: %d' % (self.i, temp)
        msg.data = '%s' % str(values[self.i - 1])
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        #self.i = self.i % 6 + 1


def main(args=None):
    rclpy.init(args=args)
    initMove()
    time.sleep(2)

    minimal_publisher = MinimalPublisher()
    
    send = True
    while rclpy.ok():
        servo_id, start_pulse, middle_pulse, end_pulse, start_time, middle_time, end_time = values[minimal_publisher.i - 1]
        minimal_publisher.timer_callback()
        dance(servo_id, start_pulse, middle_pulse, end_pulse, start_time, middle_time, end_time)
        minimal_publisher.i = minimal_publisher.i % 6 + 1

            
        


    #rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
