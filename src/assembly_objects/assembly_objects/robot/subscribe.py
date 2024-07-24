import rclpy
from rclpy.node import Node

from armpi_interfaces.msg import PositionWithAngle
from armpi_interfaces.msg import IDArmPi

class RobotSubscriber(Node):
    def __init__(self, name, armpi):
        super().__init__(name)
        self.__ID = armpi.get_ID()
        self.__armpi = armpi

    def get_ID(self):
        return self.__ID
    
    def get_armpi(self):
        return self.__armpi

class ReadySubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('ready_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi,'ready',self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        if msg.id != self.get_ID():
            self.get_logger().info('I heard: "%s"' % str(msg))

            self.get_armpi().set_ready_flag(True)

class PositionSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('position_subscriber', armpi)
        self.__subscription = self.create_subscription(PositionWithAngle,'position',self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        if msg.id != self.get_ID():
            self.get_logger().info('I heard: "%s"' % str(msg))

            (x, y, z, angle) = (msg.x, msg.y, msg.z, msg.angle)
            self.get_armpi().set_position_with_angle(x, y, z, angle)
            self.get_armpi().set_got_position_flag(True)


def create_ready_subscriber_node(armpi):
    __subscriber = ReadySubscriber(armpi)
    return __subscriber

def create_pos_subscriber_node(armpi):
    __subscriber = PositionSubscriber(armpi)
    return __subscriber