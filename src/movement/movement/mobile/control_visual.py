from rclpy.node import Node

import time

from visual_processing.srv import SetParam
from std_srvs.srv import Trigger
from armpi_pro_service_client.client import call_service

class ControlVisualProcessing(Node):
    def __init__(self):
        super().__init__('control_visual_processing_node')

    def detect_pipe(self):
        req = SetParam.Request()
        req.type = 'rectangle_detection'
        time.sleep(0.5)
        call_service(self, SetParam, '/visual_processing/set_running', req)
        self.get_logger().info(f"Set set_running in visual_processing with request {req.type}!")

    def enter_visual_processing(self):
        call_service(self.__control_visual_processing, Trigger, '/visual_processing/enter', Trigger.Request())

    def stop_visual_processing(self):
        time.sleep(0.5)
        call_service(self, SetParam, '/visual_processing/set_running', SetParam.Request())
        self.get_logger().warn("Set set_running in visual_processing to false!")

    def exit_visual_processing(self):
        self.get_logger().warn("Exit the visual_processing!")
        call_service(self.__control_visual_processing, Trigger, '/visual_processing/exit', Trigger.Request())