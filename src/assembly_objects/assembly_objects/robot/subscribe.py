import rclpy
from rclpy.node import Node

from armpi_interfaces.msg import PositionWithAngle

class RobotSubscriber(Node):

    def __init__(self, armpi):
        super().__init__('robot_subscriber')
        self.__ID = armpi.get_ID()
        self.__armpi = armpi
        self.__subscription = self.create_subscription(PositionWithAngle,'position',self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        if msg.id != self.__ID:
            self.get_logger().info('I heard: "%s"' % str(msg))

            (x, y, z, angle) = (msg.x, msg.y, msg.z, msg.angle)
            self.__armpi.set_position_with_angle(x, y, z, angle)
            self.__armpi.set_got_position_flag(True)


    def get_correct_message(self):
        while rclpy.ok():
            rclpy.spin_once(self)


def create_subscriber_node(armpi):
    __subscriber = RobotSubscriber(armpi)
    return __subscriber