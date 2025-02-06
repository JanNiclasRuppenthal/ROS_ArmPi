import rclpy
import rclpy.executors

class MultiExecutor:
    def __init__(self, subscriber_nodes_list):
        self.__executor = rclpy.executors.MultiThreadedExecutor()
        self.__subscriber_nodes_list = subscriber_nodes_list
        self.__shutdown_status = False

    def start_spinning(self):
        for subscriber in self.__subscriber_nodes_list:
            self.__executor.add_node(subscriber)

        self.__executor.spin()
        rclpy.shutdown()

    def execute_shutdown(self):
        self.__executor.shutdown()
        self.__shutdown_status = True

    def get_shutdown_status(self):
        return self.__shutdown_status