from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDArmPi

class AssemblyStepSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('assembly_step_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'assembly_step/stationary', self.callback,10)

    def callback(self, msg):
        self.get_logger().info(f"I heard: {str(msg)}")
        if self.get_armpi().get_ID() == msg.id:
            self.get_armpi().set_permission_to_do_next_assembly_step(True)
            self.get_logger().info("I am now allowed to initiate the next step for the assembly!")