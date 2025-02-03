from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from std_msgs.msg import Empty

class FinishSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('finish_subscriber', armpi)
        self.__subscription = self.create_subscription(Empty, 'finish', self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        # Do this only once
        if not self.get_armpi().get_finish_flag():
            self.get_armpi().set_finish_flag(True)
            self.get_logger().info("I can now end the scenario!")


def create_finish_subscriber_node(armpi):
    __subscriber = FinishSubscriber(armpi)
    return __subscriber