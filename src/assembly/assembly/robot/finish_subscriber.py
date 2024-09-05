import rclpy
from rclpy.node import Node

from armpi_interfaces.msg import IDArmPi

class FinishSubscriber(Node):

    def __init__(self, armpi):
        super().__init__('finish_subscriber')
        self.ID = armpi.get_ID()
        self.armpi = armpi
        self.subscription = self.create_subscription(IDArmPi,'finish',self.callback,10)
        self.subscription  # prevent unused variable warning

    def callback(self, msg):
        self.get_logger().info('I heard: "%d"' % msg.id)

        if (msg.id == self.ID):
            self.armpi.set_finish_flag(True)


def create_finish_subscriber_node(armpi):
    __subscriber = FinishSubscriber(armpi)
    return __subscriber