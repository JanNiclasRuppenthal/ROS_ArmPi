from rclpy.node import Node

from armpi_interfaces.msg import IDArmPi

class DeliverySubscriber(Node):

    def __init__(self, armpi):
        super().__init__('delivery_subscriber')
        self.ID = armpi.get_ID()
        self.armpi = armpi
        self.subscription = self.create_subscription(IDArmPi,'delivery',self.callback,10)
        self.subscription  # prevent unused variable warning

    def callback(self, msg):
        self.get_logger().info('I heard: "%d"' % msg.id)

        if (msg.id == self.ID):
            self.armpi.set_delivery_flag(True)


def create_delivery_subscriber_node(armpi):
    __subscriber = DeliverySubscriber(armpi)
    return __subscriber