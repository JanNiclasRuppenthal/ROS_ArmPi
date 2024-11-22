from common_abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from armpi_interfaces.msg import IDArmPi

class AssemblyStepSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('assembly_step_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'assembly_step/stationary', self.callback,10)
        self.__subscription  # prevent unused variable warning

    def callback(self, msg):
        self.get_logger().info(f"I heard: {str(msg)}")
        if self.get_armpi().get_ID() == msg.id:
            self.get_armpi().set_permission_to_do_next_assembly_step(True)
            self.get_logger().info("I am now allowed to initiate the next step for the assembly!")


def create_assembly_step_subscriber_node(armpi):
    __subscriber = AssemblyStepSubscriber(armpi)
    return __subscriber