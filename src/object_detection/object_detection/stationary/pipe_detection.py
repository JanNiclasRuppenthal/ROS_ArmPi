from object_detection.detected_object import DetectedObject
from object_detection.stationary.detection import Detection
from object_detection.stationary.grab_type import GrabType

class PipeDetection(Detection):
    def __init__(self):
        super().__init__()

    def calculate_upper_parameters(self):
        self._calculate_object_parameters(GrabType.UPPER, color='red')
        self.get_logger().info("Calculated upper parameters of all pipes!")

    def calculate_middle_parameters(self):
        self._calculate_object_parameters(GrabType.MIDDLE, color="red")
        self.get_logger().info("Calculated middle parameters of all pipes!")

    def calculate_bottom_parameters(self):
        self._calculate_object_parameters(GrabType.BOTTOM, color='red')
        self.get_logger().info("Calculated bottom parameters of all pipes!")


    def get_ith_detected_object(self, i) -> DetectedObject:
        x, y = self.get_position_of_ith_object(i)
        angle = self.get_angle_of_ith_object(i)
        rotation_direction = self.get_rotation_direction_of_ith_object(i)
        object_type = self.get_object_type_of_ith_object(i)

        return DetectedObject(x, y, angle, rotation_direction, object_type)