from common_abstract_nodes.publisher.Apublisher import RobotPublisher

from armpi_interfaces.msg import IDArmPi

class FinishPublisher(RobotPublisher):

    def __init__(self, armpi):
        super().__init__('finish_publisher', armpi)
        self.__last_robot = armpi.get_last_robot_flag()
        self.publisher = self.create_publisher(IDArmPi, 'finish', 10)

    def create_msgs(self):
        msg_next = IDArmPi()
        msg_next.id = (self.get_ID() + 1)
        return msg_next
    
    def send_msgs(self):
        message_next_ID = self.create_msgs()

        if not self.__last_robot:
            self.publisher.publish(message_next_ID)
            self.get_logger().info('Notifying from: "%d" to "%d"' % (self.get_ID(), message_next_ID.id))


def create_finish_publisher_node(armpi):
    __publisher = FinishPublisher(armpi)
    return __publisher
