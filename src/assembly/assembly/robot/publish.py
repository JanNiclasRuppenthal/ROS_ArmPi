import rclpy
from rclpy.node import Node

from std_msgs.msg import String

from armpi_interfaces.msg import IDArmPi

class RobotPublisher(Node):

    def __init__(self):
        super().__init__('robot_publisher')
        self.publisher_ = self.create_publisher(IDArmPi, 'delivery', 10)

    def create_msg(self, ID):
        msg = IDArmPi()
        msg.id = (ID + 1)
        self.get_logger().info('Publishing: "%d"' % msg.id)
        return msg

__robot_publisher = None
def start_publisher_node(ID, last_robot):
    global __robot_publisher

    __robot_publisher = RobotPublisher()

    __robot_publisher.publisher_.publish(__robot_publisher.create_msg(ID))
    
    # destroy_publisher_node()

def destroy_publisher_node():
    __robot_publisher.destroy_node()
    rclpy.shutdown()