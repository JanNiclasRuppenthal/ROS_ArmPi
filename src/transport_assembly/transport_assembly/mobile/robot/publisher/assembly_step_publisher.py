from common.abstract_nodes.publisher.Apublisher import RobotPublisher
from id_interface.msg import IDArmPi

class AssemblyStepPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('assembly_step_publisher', armpi)
        self.__publisher = self.create_publisher(IDArmPi, 'assembly_step/stationary', 10)

    def create_msg(self, ID):
        id_armpi_message = IDArmPi()
        id_armpi_message.id = ID
        return id_armpi_message

    def send_msg(self, ID):
        message = self.create_msg(ID)
        self.__publisher.publish(message)
        self.get_logger().info(f"Notify the stationary robot (ID = {ID}) for the next assembly step!")