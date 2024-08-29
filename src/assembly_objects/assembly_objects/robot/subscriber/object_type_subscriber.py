from robot.subscriber.Asubscribe import RobotSubscriber
from armpi_interfaces.msg import ObjectType

class ObjectTypeSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('object_type_subscriber', armpi)
        self.__subscription = self.create_subscription(ObjectType, 'object_type', self.callback,10)
        self.__subscription  # prevent unused variable warning
        # the first robot with ID 0 is ready
        self.__ready_robot_list = [True] + ([False] * (armpi.get_number_of_robots() - 1))

    def callback(self, msg):
        # if it is not the same ID and it does not received a ready message before
        if self.get_ID() != msg.id:
            self.get_logger().info('I heard a object type message from %d with the following type: "%d"' % (msg.id, msg.type))


def create_object_type_subscriber_node(armpi):
    __subscriber = ObjectTypeSubscriber(armpi)
    return __subscriber