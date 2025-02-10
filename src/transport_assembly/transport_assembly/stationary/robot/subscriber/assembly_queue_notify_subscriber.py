from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from std_msgs.msg import Empty

class NotifySubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('notify_assembly_queue_subscriber', armpi)
        self.__subscription = self.create_subscription(Empty, 'notify_assembly_queue', self.callback,10)

    def callback(self, msg):
        self.get_armpi().set_transporter_received_list(True)
        self.get_logger().info("I can now continue")