from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDArmPi

class ReadyAssemblySubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('ready_for_assembly_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'ready_for_assembly', self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        self.get_logger().info(f"I heard: {str(msg)}")
        if self.get_armpi().get_ID() == msg.id:
            self.get_armpi().set_permission_to_determine_position_of_claw(True)
            self.get_logger().info("I can now determine the position of the claw!")


def create_ready_assembly_subscriber_node(armpi):
    __subscriber = ReadyAssemblySubscriber(armpi)
    return __subscriber