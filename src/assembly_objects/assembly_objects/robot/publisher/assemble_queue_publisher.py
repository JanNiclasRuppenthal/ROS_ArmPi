from robot.publisher.Apublish import RobotPublisher
from armpi_interfaces.msg import AssembleQueue

class AssembleQueuePublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('assemble_queue_publisher', armpi)
        self.__publisher = self.create_publisher(AssembleQueue, 'assemble_queue', 10)

    def create_msg(self):
        msg = AssembleQueue()
        msg.id = self.get_ID()
        msg.type = self.get_armpi().get_object_type().value
        msg.number_objects = self.get_armpi().get_number_of_objects()
        return msg
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info('Send assembly message with the follwowing type: %d and number: %d' % (message.type, message.number_objects))

def create_assemble_queue_publisher_node(armpi):
    __publisher = AssembleQueuePublisher(armpi)
    return __publisher