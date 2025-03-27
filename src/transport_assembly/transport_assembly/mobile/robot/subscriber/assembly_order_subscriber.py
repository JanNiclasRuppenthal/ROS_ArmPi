from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDList

class AssemblyOrderSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('assembly_order_subscriber', armpi)
        self.__subscription = self.create_subscription(IDList, 'assembly_order', self.callback,10)

    def callback(self, msg):
        list_of_ids = list(msg.ids)
        self.get_logger().info(f"I got the list for the assembly!")
        self.get_armpi().set_IDList(list_of_ids)
        self.get_armpi().set_assembly_order_status(True)

