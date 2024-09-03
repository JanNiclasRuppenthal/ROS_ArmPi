from robot.subscriber.Asubscribe import RobotSubscriber
from armpi_interfaces.msg import AssemblyQueue

class AssemblyQueueSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('assembly_queue_subscriber', armpi)
        self.__subscription = self.create_subscription(AssemblyQueue, 'assembly_queue', self.callback,10)
        self.__subscription  # prevent unused variable warning
        self.__assemble_list = ([False] * (armpi.get_number_of_robots()))

    def callback(self, msg):
        # if it is not the same ID and it does not received a assemble queue message before
        self.get_logger().info('I heard a assembly queue message from %d with the following type: "%d" and it has "%d" objects.' % (msg.id, msg.type, msg.number_objects))

        self.get_armpi().set_object_type_value_next_robot(msg.type)
        self.get_armpi().get_assemble_queue().add_assemble_request(msg.id, msg.type, msg.number_objects)


def create_assembly_queue_subscriber_node(armpi):
    __subscriber = AssemblyQueueSubscriber(armpi)
    return __subscriber