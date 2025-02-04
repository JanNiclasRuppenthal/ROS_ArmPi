from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDArmPi

class DeliverySubscriber(RobotSubscriber):

    def __init__(self, armpi):
        super().__init__('delivery_subscriber', armpi)
        self.subscription = self.create_subscription(IDArmPi,'delivery',self.callback,10)

    def callback(self, msg):
        if msg.id == self.get_ID():
            self.get_logger().info('I can deliver a cube!')
            self.get_armpi().set_delivery_flag(True)