from common_abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDArmPi

class FinishSubscriber(RobotSubscriber):

    def __init__(self, armpi):
        super().__init__('finish_subscriber', armpi)
        self.subscription = self.create_subscription(IDArmPi,'finish',self.callback,10)
        self.subscription  # prevent unused variable warning

    def callback(self, msg):
        if (msg.id == self.get_ID()):
            self.get_logger().info('My predecessor detected no cube!')
            self.get_armpi().set_finish_flag(True)


def create_finish_subscriber_node(armpi):
    __subscriber = FinishSubscriber(armpi)
    return __subscriber