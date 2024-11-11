from movement.stationary.pipes.grab import *
from object_detection.stationary.pipe_detection import PipeDetection



pipe_detection = PipeDetection()
#obj_finder.calculate_upper_parameters()
pipe_detection.calculate_bottom_parameters()
x, y = pipe_detection.get_position_of_ith_object(0)
angle = pipe_detection.get_angle_of_ith_object(0)
rotation_direction = pipe_detection.get_rotation_direction_of_ith_object(0)
object_type = pipe_detection.get_object_type_of_ith_object(0)
number_of_objects = pipe_detection.get_number_of_objects()

grab_the_object(0, x, y, angle, rotation_direction, object_type)
go_to_delivery_position()