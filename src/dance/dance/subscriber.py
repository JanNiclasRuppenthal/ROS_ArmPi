import time

import rclpy
from rclpy.node import Node

from .move import dance, initMove

from std_msgs.msg import String


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'dance',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        valuesSTR = msg.data
        self.get_logger().info('I heard: "%s"' % msg.data)

        values = valuesSTR[1:-1].split(',')
        servo_id, start_pulse, middle_pulse, end_pulse, start_time, middle_time, end_time = tuple(int(v) for v in values)

        if (servo_id == 0):
            initMove()
            time.sleep(3)
        else:
            dance(servo_id, start_pulse, middle_pulse, end_pulse, start_time, middle_time, end_time)


def main(args=None):
    rclpy.init(args=args)

    initMove()
    time.sleep(2)


    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
