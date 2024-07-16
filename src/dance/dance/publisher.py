import time

from .move import dance, initMove

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

values = [
    (0, 0, 0, 0, 0, 0, 0),
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
        self.i = 1

    def timer_callback(self):
        msg = String()
        msg.data = '%s' % str(values[self.i])
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)
    initMove()
    time.sleep(2)

    minimal_publisher = MinimalPublisher()

    round = 0
    while round != 3 and rclpy.ok():
        servo_id, start_pulse, middle_pulse, end_pulse, start_time, middle_time, end_time = values[minimal_publisher.i]
        minimal_publisher.timer_callback()

        if (servo_id == 0):
            initMove()
            time.sleep(3)
            round += 1
        else:
            dance(servo_id, start_pulse, middle_pulse, end_pulse, start_time, middle_time, end_time)

        minimal_publisher.i = (minimal_publisher.i + 1) % 7

            
        


    #rclpy.spin(minimal_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()