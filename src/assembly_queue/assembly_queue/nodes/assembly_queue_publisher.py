from common.abstract_nodes.publisher.Apublisher import RobotPublisher
from assembly_queue_interface.msg import AssemblyQueue

class AssemblyQueuePublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('assembly_queue_publisher', armpi)
        self.__publisher = self.create_publisher(AssemblyQueue, 'assembly_queue', 10)

    def create_msg(self):
        msg = AssemblyQueue()
        msg.id = self.get_ID()
        msg.type = self.get_armpi().get_object_type().value
        msg.number_objects = self.get_armpi().get_number_of_objects()
        return msg
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info('Send assembly message with the following type: %d and number: %d' % (message.type, message.number_objects))