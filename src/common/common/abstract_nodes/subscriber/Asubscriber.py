from rclpy.node import Node

class RobotSubscriber(Node):
    def __init__(self, name, armpi):
        super().__init__(name)
        self.__ID = armpi.get_ID()
        self.__armpi = armpi

    def get_ID(self):
        return self.__ID
    
    def get_armpi(self):
        return self.__armpi

    def _received_same_id(self, message_id):
        return self.__ID == message_id