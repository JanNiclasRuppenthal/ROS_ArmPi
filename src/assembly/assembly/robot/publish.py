from rclpy.node import Node

from armpi_interfaces.msg import IDArmPi

class DeliveryPublisher(Node):

    def __init__(self, armpi):
        super().__init__('delivery_publisher')
        self.ID = armpi.get_ID()
        self.last_robot = armpi.get_last_robot_flag()
        self.publisher_ = self.create_publisher(IDArmPi, 'delivery', 10)

    def create_msgs(self):
        msg_prev = IDArmPi()
        msg_prev.id = (self.ID - 1)
        
        msg_next = IDArmPi()
        msg_next.id = (self.ID + 1)
        return msg_prev, msg_next
    
    def send_msgs(self):
        message_prev_ID, message_next_ID = self.create_msgs()

        if message_prev_ID.id >= 0:
            self.publisher_.publish(message_prev_ID)
            self.get_logger().info('Notifying from: "%d" to "%d"' % (self.ID, message_prev_ID.id))

        if not self.last_robot:
            self.publisher_.publish(message_next_ID)
            self.get_logger().info('Notifying from: "%d" to "%d"' % (self.ID, message_next_ID.id))


def create_delivery_publisher_node(armpi):
    __publisher = DeliveryPublisher(armpi)
    return __publisher
