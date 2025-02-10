from rclpy.node import Node

import time

from visual_processing.srv import SetParam
from visual_processing.msg import Result
from armpi_pro_service_client.client import call_service

class ControlVisualProcessing(Node):
    def __init__(self):
        super().__init__('control_visual_processing_node')

    def detect_pipe(self):
        req = SetParam.Request()
        req.type = 'rectangle_detection'
        time.sleep(0.5)
        call_service(self, SetParam, '/visual_processing/set_running', req)
        self.get_logger().warn(f"Set set_running in visual_processing with request {req.type}!")

    def stop_detecting(self):
        time.sleep(0.5)
        call_service(self, SetParam, '/visual_processing/set_running', SetParam.Request())
        self.get_logger().warn("Set set_running in visual_processing to false!")