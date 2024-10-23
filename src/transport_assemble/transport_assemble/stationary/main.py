from transport_assemble.movement.grab import *
from object_detection.object_finder_stationary import ObjectFinder



obj_finder = ObjectFinder()
obj_finder.calculate_upper_parameters()
x, y = obj_finder.get_position_of_ith_object(0)
angle = obj_finder.get_angle_of_ith_object(0)
rotation_direction = obj_finder.get_rotation_direction_of_ith_object(0)
object_type = obj_finder.get_object_type_of_ith_object(0)
number_of_objects = obj_finder.get_number_of_objects()

grab_the_object(0, x, y, angle, rotation_direction, object_type)
go_to_delivery_position()