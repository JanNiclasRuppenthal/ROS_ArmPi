from common.abstract_nodes.subscriber.Asubscriber import RobotSubscriber
from id_interface.msg import IDArmPi

class GrabbedSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('grabbed_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'grabbed', self.callback,10)

    def callback(self, msg):
        self.get_logger().info(f"I heard: {str(msg)}")
        if self.get_armpi().get_ID() == msg.id:
            self.get_armpi().set_letting_go_pipe(True)
            self.get_logger().info("I need to let go the pipe!")