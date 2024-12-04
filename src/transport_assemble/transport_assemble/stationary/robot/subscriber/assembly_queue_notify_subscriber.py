from common_abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from armpi_interfaces.msg import IDArmPi

class NotifySubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('notify_assembly_queue_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'notify_assembly_queue', self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        if self.get_armpi().get_ID() == msg.id:
            self.get_armpi().set_transporter_received_list(True)
            self.get_logger().info("I can now continue")


def create_notify_subscriber_node(armpi):
    __subscriber = NotifySubscriber(armpi)
    return __subscriber