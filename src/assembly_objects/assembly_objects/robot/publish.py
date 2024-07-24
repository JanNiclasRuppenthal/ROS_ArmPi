from rclpy.node import Node

from armpi_interfaces.msg import PositionWithAngle
from armpi_interfaces.msg import IDArmPi

class RobotPublisher(Node):

    def __init__(self, name, armpi):
        super().__init__(name)
        self.__ID = armpi.get_ID()

    def get_ID(self):
        return self.__ID


class ReadyPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('ready_publisher', armpi)
        self.__publisher = self.create_publisher(IDArmPi, 'ready', 10)

    def create_msg(self):
        msg = IDArmPi()
        msg.id = self.get_ID()
        return msg
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info('Send ready message from ID %d' % (message.id))



class PositionPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('position_publisher', armpi)
        self.__publisher = self.create_publisher(PositionWithAngle, 'position', 10)

    def create_msg(self, x, y, z, angle):
        msg = PositionWithAngle()
        msg.id = self.get_ID()
        msg.x = x
        msg.y = y
        msg.z = z
        msg.angle = angle

        return msg
        
    
    def send_msg(self, x, y, z, angle):
        message = self.create_msg(x, y, z, angle)
        self.__publisher.publish(message)
        self.get_logger().info('Send following position and angle: (%f, %f, %f, %d)' % (message.x, message.y, message.z, message.angle))


def create_ready_publisher_node(armpi):
    __publisher = ReadyPublisher(armpi)
    return __publisher

def create_pos_publisher_node(armpi):
    __publisher = PositionPublisher(armpi)
    return __publisher
