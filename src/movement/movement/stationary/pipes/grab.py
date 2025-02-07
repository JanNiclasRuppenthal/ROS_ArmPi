import time

from movement.stationary.pipes.common_movement import Movement
from object_detection.detected_object import DetectedObject


class GrabMovement(Movement):
    def __init__(self, AK):
        super().__init__("movement_grab_node", AK)


    def grab_the_object(self, ID, detected_object : DetectedObject):
        # Go to the position of the object with z = 7
        result = self._AK.setPitchRangeMoving((detected_object.get_x(), detected_object.get_y(), 7), -90, -90, 0)
        self.get_logger().info(f"Move 7cm above the detected object ({detected_object.get_x()}, {detected_object.get_y()}, 7)  with the following values: {result}")
        time.sleep(result[2]/1000)

        self.open_claw()

        self._move_to_detected_object(detected_object)

        grab_pulse = self._determine_pulse(ID, detected_object.get_object_type())

        #close the claw with the above pulse value
        self._close_claw_with_value(grab_pulse)


    def go_to_waiting_position(self):
        # Go up again (waiting-position)
        result = self._AK.setPitchRangeMoving((0, 12.5, 10), -90, -90, 0)
        self.get_logger().info(f"Move to my waiting position (0, 12.5, 10) with the following values: {result}")
        time.sleep(result[2]/1000)

        # rotate the claw again
        initial_rotation_value_of_claw = 500
        self._rotate_claw_with_value(initial_rotation_value_of_claw)