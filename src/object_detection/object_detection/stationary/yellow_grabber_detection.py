from object_detection.stationary.detection import Detection
from object_detection.stationary.grab_type import GrabType

class GrabberDetection(Detection):

    def calculate_middle_between_grabber(self):
       self._calculate_object_parameters(GrabType.MIDDLE, color='yellow')
       x_left, y_left = self.get_position_of_ith_object(0) # there should be only one grabber in the view

       if x_left == -1 and y_left == -1:
           return 0, 20

       x_right, y_right = self.get_position_of_ith_object(1)
       
       self.get_logger().info(f"Left world coordinates: ({x_left}, {y_left})")
       self.get_logger().info(f"Right world coordinates: ({x_right}, {y_right})")

       pos_x  = (x_left + x_right) / 2
       pos_y = (y_left + y_right) / 2

       self.get_logger().info(f"Real world coordinates: ({pos_x}, {pos_y})")

       return pos_x, pos_y
