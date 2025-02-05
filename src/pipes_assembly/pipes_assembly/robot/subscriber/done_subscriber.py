from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDArmPi

class DoneSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('done_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'done', self.callback,10)

    def callback(self, msg):
        # if it is the same ID then ignore it
        if msg.id != self.get_ID():
            self.get_logger().info('I heard a done message from robot with ID: "%s"' % str(msg.id))
            self.get_armpi().get_assembly_queue().pop()