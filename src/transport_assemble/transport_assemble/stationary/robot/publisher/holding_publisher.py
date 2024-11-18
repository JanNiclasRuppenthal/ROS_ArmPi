from common_abstract_nodes.publisher.Apublisher import RobotPublisher
from std_msgs.msg import Empty

class HoldingPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('holding_publisher', armpi)
        self.__publisher = self.create_publisher(Empty, 'holding', 10)

    def create_msg(self):
        msg = Empty()
        return msg
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info('Notify ArmPi Pro to drive away!')


def create_holding_publisher_node(armpi):
    __publisher = HoldingPublisher(armpi)
    return __publisher