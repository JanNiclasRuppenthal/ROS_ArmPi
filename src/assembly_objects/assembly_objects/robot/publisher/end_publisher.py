from robot.publisher.Apublish import RobotPublisher
from armpi_interfaces.msg import IDArmPi

class EndPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('end_publisher', armpi)
        self.__publisher = self.create_publisher(IDArmPi, 'end', 10)

    def create_msg(self):
        msg = IDArmPi()
        msg.id = self.get_ID()
        return msg
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info('Send end message from ID %d' % (message.id))


def create_end_publisher_node(armpi):
    __publisher = EndPublisher(armpi)
    return __publisher