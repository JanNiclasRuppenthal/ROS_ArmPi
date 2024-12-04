from object_detection.stationary.detection import Detection
from object_detection.stationary.grab_type import GrabType

class GrabberDetection(Detection):

    def calculate_middle_between_grabber(self):
       self._calculate_object_parameters(GrabType.MIDDLE, color='yellow')
       x_left, y_left = self.get_position_of_ith_object(0)
       x_right, y_right = self.get_position_of_ith_object(1)
       
       print(f"Left world coordinates: ({x_left}, {y_left})")
       print(f"Right world coordinates: ({x_right}, {y_right})")

       pos_x  = (x_left + x_right) / 2
       pos_y = (y_left + y_right) / 2

       print(f"Real world coordinates: ({pos_x}, {pos_y})")

       return pos_x, pos_y
