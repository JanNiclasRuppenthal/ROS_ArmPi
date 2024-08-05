from .Asubscribe import RobotSubscriber
from armpi_interfaces.msg import IDArmPi

class ReadySubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('ready_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi,'ready',self.callback,10)
        self.__subscription  # prevent unused variable warning
        # the first robot with ID 0 is ready
        self.__ready_robot_list = [True] + ([False] * (armpi.get_number_of_robots() - 1))

    def callback(self, msg):
        # if it is not the same ID and it does not received a ready message before
        if msg.id != self.get_ID() and not self.get_armpi().get_ready_flag():
            self.get_logger().info('I heard a ready message from robot with ID: "%s"' % str(msg.id))

            if (self.get_ID() == 0):

                '''
                This robot is the first in the line.
                So it has to wait until every other robot is ready.
                '''

                self.__ready_robot_list[msg.id] = True
                for ready_robot_flag in self.__ready_robot_list:

                    # if one robot in the list is not ready, then do not set the ready flag to True
                    if (not ready_robot_flag):
                        return 

                self.get_armpi().set_ready_flag(True)
                
                # reset the list again
                self.__ready_robot_list = [True] + ([False] * (self.get_armpi().get_number_of_robots() - 1))
            elif (msg.id == 0): 
                # the first robot is ready
                self.get_armpi().set_ready_flag(True)


def create_ready_subscriber_node(armpi):
    __subscriber = ReadySubscriber(armpi)
    return __subscriber