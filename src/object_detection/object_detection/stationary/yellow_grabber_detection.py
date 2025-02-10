from object_detection.stationary.detection import Detection
from object_detection.grab_type import GrabType

class GrabberDetection(Detection):
    
    def __init__(self):
      super().__init__("grabber_detection_node")

    def calculate_middle_between_grabber(self) -> tuple[float, float]:
       self._calculate_object_parameters(GrabType.MIDDLE, color='yellow')
       x_left, y_left = self.get_position_of_ith_object(0) # there should be only one grabber in the view

       if x_left == -1 and y_left == -1:
           return float(0.0), float(20)

       x_right, y_right = self.get_position_of_ith_object(1)
       
       self.get_logger().info(f"Left world coordinates: ({x_left}, {y_left})")
       self.get_logger().info(f"Right world coordinates: ({x_right}, {y_right})")

       pos_x  = (x_left + x_right) / 2
       pos_y = (y_left + y_right) / 2

       self.get_logger().info(f"Real world coordinates: ({pos_x}, {pos_y})")

       diff_x, diff_y = self.__determine_differece_for_movement(pos_x, pos_y)
       x, y = self.__convert_coordinates_from_cm_to_m(diff_x, diff_y)

       return float(x), float(y)

    def __determine_differece_for_movement(self, x, y):
       return x, y - 20

    def __convert_coordinates_from_cm_to_m(self, x, y):
       return x / 100, y / 100
