from common_abstract_nodes.publisher.Apublisher import RobotPublisher
from armpi_interfaces.msg import IDArmPi

class NotifyPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('notify_publisher', armpi)
        self.__publisher = self.create_publisher(IDArmPi, 'notify_assembly_queue', 10)

    def create_msg(self, id_of_robot):
        msg = IDArmPi()
        msg.id = id_of_robot
        return msg
    
    def send_msg(self, id_of_robot):
        message = self.create_msg(id_of_robot)
        self.__publisher.publish(message)
        self.get_logger().info(f"Notify the ArmPi with the ID {id_of_robot} to initalte the next step for the grab!")


def create_notify_publisher_node(armpi):
    __publisher = NotifyPublisher(armpi)
    return __publisher