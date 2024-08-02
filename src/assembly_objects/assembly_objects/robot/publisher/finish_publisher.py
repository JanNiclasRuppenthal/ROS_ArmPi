from .Apublish import RobotPublisher
from armpi_interfaces.msg import IDArmPi

class FinishPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('finish_publisher', armpi)
        self.__publisher = self.create_publisher(IDArmPi, 'finish', 10)

    def create_msg(self):
        msg = IDArmPi()
        msg.id = self.get_ID()
        return msg
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info('Send finish message from ID %d' % (message.id))


def create_finish_publisher_node(armpi):
    __publisher = FinishPublisher(armpi)
    return __publisher