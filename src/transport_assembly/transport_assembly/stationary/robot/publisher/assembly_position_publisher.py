from common.abstract_nodes.publisher.Apublisher import RobotPublisher
from position_interface.msg import Position2D

class AssemblyPositionPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('assembly_position_publisher', armpi)
        self.__publisher = self.create_publisher(Position2D, 'assembly_position_publisher', 10)

    def create_msg(self, x, y):
        message = Position2D()
        message.x = x
        message.y = y
        return message
    
    def send_msg(self, x, y):
        message = self.create_msg(x, y)
        self.__publisher.publish(message)
        self.get_logger().info(f"Send to ArmPi Pro the following positions: ({x}, {y}).")


def create_assembly_position_publisher_node(armpi):
    __publisher = AssemblyPositionPublisher(armpi)
    return __publisher