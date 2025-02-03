from common_abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from assembly_queue_interface import AssemblyQueue

class AssembleQueueSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('assemble_queue_subscriber', armpi)
        self.__subscription = self.create_subscription(AssemblyQueue, 'assemble_queue', self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        if self.get_ID() != msg.id:
            self.get_logger().info('I heard a assembly queue message from %d with the following type: "%d" and it has "%d" objects.' % (msg.id, msg.type, msg.number_objects))

        self.get_armpi().set_object_type_value_next_robot(msg.type)
        self.get_armpi().get_assemble_queue().add_assemble_request(msg.id, msg.type, msg.number_objects)


def create_assemble_queue_subscriber_node(armpi):
    __subscriber = AssembleQueueSubscriber(armpi)
    return __subscriber