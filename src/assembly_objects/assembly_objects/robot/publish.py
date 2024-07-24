from rclpy.node import Node

from armpi_interfaces.msg import PositionWithAngle

class RobotPublisher(Node):

    def __init__(self, armpi):
        super().__init__('robot_publisher')
        self.ID = armpi.get_ID()
        self.publisher_ = self.create_publisher(PositionWithAngle, 'position', 10)

    def create_msgs(self, x, y, z, angle):
        msg = PositionWithAngle()
        msg.id = self.ID
        msg.x = x
        msg.y = y
        msg.z = z
        msg.angle = angle

        return msg
        
    
    def send_msgs(self, x, y, z, angle):
        message = self.create_msgs(x, y, z, angle)

        
        self.publisher_.publish(message)
        self.get_logger().info('Send following position and angle: (%f, %f, %f, %d)' % (message.x, message.y, message.z, message.angle))


def create_publisher_node(armpi):
    __publisher = RobotPublisher(armpi)
    return __publisher
