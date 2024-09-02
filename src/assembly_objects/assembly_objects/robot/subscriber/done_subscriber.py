from robot.subscriber.Asubscribe import RobotSubscriber
from armpi_interfaces.msg import IDArmPi

class DoneSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('done_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'done', self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        # if it is not the same ID and it does not received a done message before
        if msg.id != self.get_ID():
            self.get_logger().info('I heard a done message from robot with ID: "%s"' % str(msg.id))
            self.get_armpi().get_assemble_queue().pop()
            self.get_logger().info('here is the new queue: "%s"' % str(self.get_armpi().get_assemble_queue()))

            if (self.get_armpi().get_assemble_queue().empty()):
                self.get_armpi().get_assemble_queue().clear_dict()



def create_done_subscriber_node(armpi):
    __subscriber = DoneSubscriber(armpi)
    return __subscriber