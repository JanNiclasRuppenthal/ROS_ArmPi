from rclpy.node import Node

import time
import math

from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board

from object_detection.detected_object import DetectedObject
from object_detection.object_type import ObjectType


class Movement(Node):
    def __init__(self, node_name, AK):
        super().__init__(node_name)
        self._AK = AK

        self.__grab_pulse_ID_0 = {
            ObjectType.SMALL : 600,
            ObjectType.MEDIUM : 500,
            ObjectType.LARGE : 400
        }

        self.__grab_pulse_ID_1 = {
            ObjectType.SMALL : 650,
            ObjectType.MEDIUM : 575,
            ObjectType.LARGE : 450
        }

    def init_move(self):
        Board.setBusServoPulse(1, 500 - 50, 300)
        Board.setBusServoPulse(2, 500, 500)
        result = self._AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)
        time.sleep(result[2]/1000)

    def open_claw(self):
        Board.setBusServoPulse(1, 100, 500)
        time.sleep(0.5)

    def _close_claw_with_value(self, value):
        Board.setBusServoPulse(1, value, 500)
        time.sleep(0.5)

    def _rotate_claw_with_value(self, value):
        Board.setBusServoPulse(2, value, 500)
        time.sleep(0.8)

    def rotate_away_from_camera(self):
        Board.setBusServoPulse(6, 875, 800)
        time.sleep(0.8)

    def _get_z_coordinate(self, object_type : ObjectType) -> float:
        if object_type == ObjectType.SMALL:
            result = 1.2
        else:
            result = 1.5

        return result

    def _determine_pulse(self, ID, object_type : ObjectType) -> int:
        if ID == 0:
            result = self.__grab_pulse_ID_0[object_type]
        else:
            result = self.__grab_pulse_ID_1[object_type]

        return result

    def __convert_angle_to_pulse(self, x, y, angle, rotation_direction) -> float:
        # We need to declare that the y-Axis has a degree of zero degrees and not 90 degrees
        # Because of that we need to subtract 90 to the result of atan2
        angle_from_origin_to_object = 90 - round(math.degrees(math.atan2(y, abs(x))), 1)

        # If the object has a positive x coordinate, then the servo needs to decrement its pulse
        # so that the arm is aligned with the x-axis
        if x > 0:
            angle_from_origin_to_object = -angle_from_origin_to_object

        calculated_angle = (angle_from_origin_to_object + rotation_direction * angle)
        pulse = int(500 + calculated_angle * (1000 / 240))
        return pulse

    def _move_to_detected_object(self, detected_object : DetectedObject):
        pulse_value = self.__convert_angle_to_pulse(detected_object.get_x(), detected_object.get_y(),
                                                   detected_object.get_angle(),
                                                   detected_object.get_rotation_direction())
        self._rotate_claw_with_value(pulse_value)
        
        # Go to the position of the object
        z = self._get_z_coordinate(detected_object.get_object_type())
        result = self._AK.setPitchRangeMoving((detected_object.get_x(), detected_object.get_y(), z), -90, -90, 0, 600)
        self.get_logger().info(f"Move to detected object at ({detected_object.get_x()}, {detected_object.get_y()}, {z}) with the following values: {result}")
        time.sleep(result[2] / 1000)
