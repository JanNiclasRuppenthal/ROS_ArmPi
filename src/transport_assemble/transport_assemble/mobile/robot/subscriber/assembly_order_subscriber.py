from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDList

class AssemblyOrderSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('assembly_order_subscriber', armpi)
        self.__subscription = self.create_subscription(IDList, 'assembly_order', self.callback,10)
        self.__subscription

    def callback(self, msg):
        self.get_armpi().set_IDList(list(msg.ids))
        self.get_armpi().set_assembly_order_status(True)
        self.get_logger().info(f"I got the following list: {list(msg.ids)}!")


def create_assembly_order_subscriber_node(armpi):
    __subscriber = AssemblyOrderSubscriber(armpi)
    return __subscriber