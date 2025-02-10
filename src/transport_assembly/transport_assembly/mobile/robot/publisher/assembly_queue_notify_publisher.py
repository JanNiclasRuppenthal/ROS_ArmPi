from common.abstract_nodes.publisher.Apublisher import RobotPublisher
from std_msgs.msg import Empty

class NotifyReceivingAssemblyQueuePublisher(RobotPublisher):
    def __init__(self, armpi):
        super().__init__('notify_receiving_assembly_publisher', armpi)
        self.__publisher = self.create_publisher(Empty, 'notify_receiving_assembly_queue', 10)

    def create_msg(self):
        return Empty()
    
    def send_msg(self):
        message = self.create_msg()
        self.__publisher.publish(message)
        self.get_logger().info(f"Notify that I received the assembly order and "
                               f"all stationary ArmPis can initiate the scenario!")