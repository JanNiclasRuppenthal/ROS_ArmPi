from common_abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from std_msgs.msg import Empty

class HoldingSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('holding_subscriber', armpi)
        self.__subscription = self.create_subscription(Empty, 'holding', self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        self.get_logger().info('I got notified!')
        self.get_armpi().set_first_robot_hold_pipe(False)

def create_pos_subscriber_node(armpi):
    __subscriber = HoldingSubscriber(armpi)
    return __subscriber