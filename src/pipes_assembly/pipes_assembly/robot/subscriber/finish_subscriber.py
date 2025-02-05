from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDArmPi


class FinishSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('finish_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'finish', self.callback,10)

    def callback(self, msg):
        # if it is not the same ID and it does not recieved a ready message before
        if not self._received_same_id(msg.id) and not self.get_armpi().get_finish_flag():
            self.get_logger().info('I heard an end message from robot with ID: "%s"' % str(msg.id))

            self.get_armpi().set_finish_flag(True)