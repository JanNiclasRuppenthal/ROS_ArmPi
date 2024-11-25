from common_abstract_nodes.publisher.Apublisher import RobotPublisher
from std_msgs.msg import Empty

class FinishPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('finish_publisher', armpi)
        self.__publisher = self.create_publisher(Empty, 'finish', 10)

    def create_msg(self):
        msg = Empty()
        return msg
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info('Notify all robots to end the scenario!')


def create_finish_publisher_node(armpi):
    __publisher = FinishPublisher(armpi)
    return __publisher