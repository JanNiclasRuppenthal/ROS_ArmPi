from robot.publisher.Apublish import RobotPublisher
from armpi_interfaces.msg import ObjectType

class ObjectTypePublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('object_type_publisher', armpi)
        self.__publisher = self.create_publisher(ObjectType, 'object_type', 10)

    def create_msg(self):
        msg = ObjectType()
        msg.id = self.get_ID()
        msg.type = self.get_Armpi().get_object_type().value
        return msg
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info('Send object type message with the follwowing type: %d' % (message.type))

def create_object_type_publisher_node(armpi):
    __publisher = ObjectTypePublisher(armpi)
    return __publisher