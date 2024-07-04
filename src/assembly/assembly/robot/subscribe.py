import rclpy
from rclpy.node import Node

from armpi_interfaces.msg import IDArmPi

class RobotSubscriber(Node):

    def __init__(self, ID, armpi):
        super().__init__('robot_subscriber')
        self.ID = ID
        self.armpi = armpi
        self.subscription = self.create_subscription(IDArmPi,'delivery',self.callback,10)
        self.subscription  # prevent unused variable warning

    def callback(self, msg):
        self.get_logger().info('I heard: "%d"' % msg.id)

        if (msg.id == self.ID):
            self.armpi.set_delivery_flag(True)
            print("Set True")

    def get_correct_message(self):
        while rclpy.ok():
            print("before")
            rclpy.spin_once(self)
            print("after")


def create_subscriber_node(ID, armpi):
    __subscriber = RobotSubscriber(ID, armpi)
    return __subscriber