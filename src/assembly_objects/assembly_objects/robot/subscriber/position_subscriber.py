from .Asubscribe import RobotSubscriber
from armpi_interfaces.msg import PositionWithAngle

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

def create_pos_subscriber_node(armpi):
    __subscriber = PositionSubscriber(armpi)
    return __subscriber