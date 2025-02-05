from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from position_interface.msg import PositionWithAngle

class PositionSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('position_subscriber', armpi)
        self.__subscription = self.create_subscription(PositionWithAngle, 'position', self.callback,10)

    def callback(self, msg):
        if not self._received_same_id(msg.id):
            self.get_logger().info('I heard: "%s"' % str(msg))

            (x, y, z, angle) = (msg.x, msg.y, msg.z, msg.angle)
            self.get_armpi().set_position_with_angle(x, y, z, angle)