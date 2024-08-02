from .Asubscribe import RobotSubscriber
from armpi_interfaces.msg import IDArmPi

class ReadySubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('ready_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi,'ready',self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        # if it is not the same ID and it does not recieved a ready message before
        if msg.id != self.get_ID() and not self.get_armpi().get_ready_flag():
            self.get_logger().info('I heard: "%s"' % str(msg))

            self.get_armpi().set_ready_flag(True)


def create_ready_subscriber_node(armpi):
    __subscriber = ReadySubscriber(armpi)
    return __subscriber