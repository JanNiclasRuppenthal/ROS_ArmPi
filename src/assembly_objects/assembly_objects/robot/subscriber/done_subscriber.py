from robot.subscriber.Asubscribe import RobotSubscriber
from armpi_interfaces.msg import IDArmPi

class DoneSubscriber(RobotSubscriber):
    def __init__(self, armpi):
        super().__init__('done_subscriber', armpi)
        self.__subscription = self.create_subscription(IDArmPi, 'done', self.callback,10)
        self.__subscription  # prevent unused variable warning
        # the first robot with ID 0 is done
        self.__done_robot_list = [True] + ([False] * (armpi.get_number_of_robots() - 1))

    def callback(self, msg):
        # if it is not the same ID and it does not received a done message before
        if msg.id != self.get_ID() and not self.get_armpi().get_done_flag():
            self.get_logger().info('I heard a done message from robot with ID: "%s"' % str(msg.id))

            if (self.get_ID() == 0):

                '''
                This robot is the first in the line.
                So it has to wait until every other robot did its task to put down the assembled object.
                '''

                self.__done_robot_list[msg.id] = True
                for done_robot_flag in self.__done_robot_list:

                    # if one robot in the list is not done, then do not set the done flag to True
                    if (not done_robot_flag):
                        return 

                self.get_armpi().set_done_flag(True)

                # reset the list again
                self.__done_robot_list = [True] + ([False] * (self.get_armpi().get_number_of_robots() - 1))
            elif (msg.id == (self.get_ID() - 1)): 
                # the previous robot did its task
                self.get_armpi().set_done_flag(True)


def create_done_subscriber_node(armpi):
    __subscriber = DoneSubscriber(armpi)
    return __subscriber