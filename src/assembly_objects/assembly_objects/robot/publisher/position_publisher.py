from robot.publisher.Apublish import RobotPublisher
from armpi_interfaces.msg import PositionWithAngle

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



def create_pos_publisher_node(armpi):
    __publisher = PositionPublisher(armpi)
    return __publisher