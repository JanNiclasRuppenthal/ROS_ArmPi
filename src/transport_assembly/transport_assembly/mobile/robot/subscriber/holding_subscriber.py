from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from std_msgs.msg import Empty

class HoldingSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('holding_subscriber', armpi)
        self.__subscription = self.create_subscription(Empty, 'holding', self.callback,10)

    def callback(self, msg):
        self.get_armpi().set_first_robot_hold_pipe(False)
        self.get_logger().info('I got notified!')