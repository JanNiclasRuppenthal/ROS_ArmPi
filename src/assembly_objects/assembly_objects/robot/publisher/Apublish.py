from rclpy.node import Node

class RobotPublisher(Node):

    def __init__(self, name, armpi):
        super().__init__(name)
        self.__ID = armpi.get_ID()

    def get_ID(self):
        return self.__ID