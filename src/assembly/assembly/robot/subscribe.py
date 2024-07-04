import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from armpi_interfaces.msg import IDArmPi

class RobotSubscriber(Node):

    def __init__(self):
        super().__init__('robot_subscriber')
        self.subscription = self.create_subscription(IDArmPi,'delivery',self.callback,10)
        self.subscription  # prevent unused variable warning

    def callback(self, msg):
        self.get_logger().info('I heard: "%d"' % msg.id)

__subscriber = None

def start_subscriber_node(context):
    global __subscriber

    print("Started the subscriber node")
    __subscriber = RobotSubscriber(context = context)
    return __subscriber

def destroy_subscriber_node():
    global __subscriber

    __subscriber.destroy_node()
    rclpy.shutdown()