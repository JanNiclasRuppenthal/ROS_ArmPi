from common_abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface import IDArmPi


class FinishSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('finish_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'finish', self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        # if it is not the same ID and it does not recieved a ready message before
        if msg.id != self.get_ID() and not self.get_armpi().get_finish_flag():
            self.get_logger().info('I heard an end message from robot with ID: "%s"' % str(msg.id))

            self.get_armpi().set_finish_flag(True)


def create_finish_subscriber_node(armpi):
    __subscriber = FinishSubscriber(armpi)
    return __subscriber