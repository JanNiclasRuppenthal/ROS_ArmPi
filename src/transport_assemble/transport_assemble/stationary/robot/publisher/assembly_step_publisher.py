from common_abstract_nodes.publisher.Apublisher import RobotPublisher
from std_msgs.msg import Empty

class AssemblyStepPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('assembly_step_publisher', armpi)
        self.__publisher = self.create_publisher(Empty, 'assembly_step/mobile', 10)

    def create_msg(self):
        return Empty()
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info("Notify the ArmPi Pro to initalte the next step for the assembly!")


def create_assembly_step_publisher_node(armpi):
    __publisher = AssemblyStepPublisher(armpi)
    return __publisher