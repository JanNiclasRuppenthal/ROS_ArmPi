from common_abstract_nodes.publisher.Apublisher import RobotPublisher
from id_interface.msg import IDList

class AssemblyOrderPublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('assembly_order_publisher', armpi)
        self.__publisher = self.create_publisher(IDList, 'assembly_order', 10)

    def create_msg(self, list):
        message = IDList()
        message.ids = list
        return message
    
    def send_msg(self, list):
        message = self.create_msg(list)
        self.__publisher.publish(message)
        self.get_logger().info(f"Send to ArmPi Pro the order for the assembly: {list}.")


def create_assembly_order_publisher_node(armpi):
    __publisher = AssemblyOrderPublisher(armpi)
    return __publisher