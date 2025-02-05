from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDArmPi

class FinishSubscriber(RobotSubscriber):

    def __init__(self, armpi):
        super().__init__('finish_subscriber', armpi)
        self.subscription = self.create_subscription(IDArmPi,'finish',self.callback,10)

    def callback(self, msg):
        if not self._received_same_id(msg.id):
            self.get_logger().info('My predecessor detected no cube!')
            self.get_armpi().set_finish_flag(True)