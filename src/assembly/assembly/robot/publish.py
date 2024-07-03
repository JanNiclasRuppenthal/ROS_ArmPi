import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class RobotPublisher(Node):

    def __init__(self):
        super().__init__('robot_publisher')
        self.publisher_ = self.create_publisher(String, 'delivery', 10)

    def create_msg(self):
        msg = String()
        msg.data = 'Hello World!'
        self.get_logger().info('Publishing: "%s"' % msg.data)
        return msg

__robot_publisher = None
def start_publisher_node(args=None):
    global __robot_publisher

    __robot_publisher = RobotPublisher()

    __robot_publisher.publisher_.publish(__robot_publisher.create_msg())
    
    # destroy_publisher_node()

def destroy_publisher_node():
    __robot_publisher.destroy_node()
    rclpy.shutdown()