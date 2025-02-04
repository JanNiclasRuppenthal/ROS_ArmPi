from common.abstract_nodes.publisher.Apublisher import RobotPublisher
from id_interface.msg import IDArmPi

class DeliveryPublisher(RobotPublisher):

    def __init__(self, armpi):
        super().__init__('delivery_publisher', armpi)
        self.__last_robot = armpi.get_last_robot_flag()
        self.publisher = self.create_publisher(IDArmPi, 'delivery', 10)

    def create_msgs(self):
        msg_prev = IDArmPi()
        msg_prev.id = (self.get_ID() - 1)
        
        msg_next = IDArmPi()
        msg_next.id = (self.get_ID() + 1)
        return msg_prev, msg_next
    
    def send_msgs(self):
        message_prev_ID, message_next_ID = self.create_msgs()

        if message_prev_ID.id >= 0:
            self.publisher.publish(message_prev_ID)
            self.get_logger().info('Notifying from: "%d" to "%d"' % (self.get_ID(), message_prev_ID.id))

        if not self.__last_robot:
            self.publisher.publish(message_next_ID)
            self.get_logger().info('Notifying from: "%d" to "%d"' % (self.get_ID(), message_next_ID.id))
