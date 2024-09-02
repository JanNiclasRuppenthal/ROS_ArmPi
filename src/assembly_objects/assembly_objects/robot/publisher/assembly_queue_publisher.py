from robot.publisher.Apublish import RobotPublisher
from armpi_interfaces.msg import AssemblyQueue

class AssemblyQueuePublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('assembly_queue_publisher', armpi)
        self.__publisher = self.create_publisher(AssemblyQueue, 'assembly_queue', 10)

    def create_msg(self):
        msg = AssemblyQueue()
        msg.id = self.get_ID()
        msg.type = self.get_Armpi().get_object_type().value
        msg.number_objects = self.get_Armpi().get_number_of_objects()
        return msg
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info('Send object type message with the follwowing type: %d and number: %d' % (message.type, message.number_objects))

def create_assembly_queue_publisher_node(armpi):
    __publisher = AssemblyQueuePublisher(armpi)
    return __publisher