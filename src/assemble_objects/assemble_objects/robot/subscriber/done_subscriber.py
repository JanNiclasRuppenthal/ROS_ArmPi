from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDArmPi

class DoneSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('done_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'done', self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        # if it is the same ID then ignore it
        if msg.id != self.get_ID():
            self.get_logger().info('I heard a done message from robot with ID: "%s"' % str(msg.id))
            self.get_armpi().get_assemble_queue().pop()



def create_done_subscriber_node(armpi):
    __subscriber = DoneSubscriber(armpi)
    return __subscriber