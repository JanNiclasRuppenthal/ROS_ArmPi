from object_detection.stationary.detection import Detection

class GrabberDetection(Detection):

    def calculate_middle_between_grabber(self):
       self._calculate_object_parameters(upper=False, color='yellow')
       x_left, y_left = self.get_position_of_ith_object(0)
       x_right, y_right = self.get_position_of_ith_object(1)

       pos_x  = (x_left + x_right) / 2
       pos_y = (y_left + y_right) / 2

       #pos_x, pos_y = self._calculate_real_world_coordinates(x_middle, y_middle)

       print(f"Real world coordinates: ({pos_x}, {pos_y})")

       return pos_x, pos_y
