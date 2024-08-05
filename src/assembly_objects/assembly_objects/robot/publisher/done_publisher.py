from .Apublish import RobotPublisher
from armpi_interfaces.msg import IDArmPi

class DonePublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('done_publisher', armpi)
        self.__publisher = self.create_publisher(IDArmPi, 'done', 10)

    def create_msg(self):
        msg = IDArmPi()
        msg.id = self.get_ID()
        return msg
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info('Send done message from ID %d' % (message.id))


def create_done_publisher_node(armpi):
    __publisher = DonePublisher(armpi)
    return __publisher