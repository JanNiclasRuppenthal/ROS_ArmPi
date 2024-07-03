import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class RobotSubscriber(Node):

    def __init__(self):
        super().__init__('robot_subscriber')
        self.subscription = self.create_subscription(String,'delivery',self.callback,10)
        self.subscription  # prevent unused variable warning

    def callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

__subscriber = None

def start_subscriber_node(args=None):
    global __subscriber

    print("Started the subscriber node")
    rclpy.init(args=args)

    __subscriber = RobotSubscriber()

    rclpy.spin(__subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    #destroy_subscriber_node()

def destroy_subscriber_node():
    global __subscriber

    __subscriber.destroy_node()
    rclpy.shutdown()