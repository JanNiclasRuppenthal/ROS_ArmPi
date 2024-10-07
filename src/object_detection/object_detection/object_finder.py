import cv2
import math
import numpy as np


from object_detection.object_type import calculate_object_type

class AObjectFinder():

    def __init__(self):
        self.sorted_data = []
        self.__object_to_parameter = {}

    # euclidean distance
    def calculate_distance(self, point_a, point_b):
        x_pow = math.pow(point_b[0] - point_a[0], 2)
        y_pow = math.pow(point_b[1] - point_a[1], 2)
        return math.sqrt(x_pow + y_pow)

    def collect_data_to_dictionary(self):
        count = 0
        position_of_objects = []
        for data in self.sorted_data:
            (x, y)  = (data[0], data[1])
            found_new_object = True
            for (prev_x, prev_y) in position_of_objects:
                if abs(x - prev_x) <= 0.5 and abs(y - prev_y) <= 0.5:
                    found_new_object = False
                    break

            
            if found_new_object:
                self.__object_to_parameter[count] = []
                count += 1

            position_of_objects.append((x, y))
            self.__object_to_parameter[count - 1].append(data)

        # Setup one default tuple
        self.__object_to_parameter[count] = [(-1, -1, -1, -1, -1)]

    def calculate_upper_points(self, frame_out, box, center_x, center_y):
        # sort the points of the box with their y coordinate
        box = sorted(box, key=lambda p: p[1])

        # the first two points have the lowest y coordinate
        upper_points = box[0:2]

        # calculate the middle point between these two bottom points
        mid_upper_x = (upper_points[0][0] + upper_points[1][0]) // 2
        mid_upper_y = (upper_points[0][1] + upper_points[1][1]) // 2

        # mark the position with a rectangle (yellow)
        cv2.rectangle(frame_out, (mid_upper_x, mid_upper_y), (mid_upper_x + 10, mid_upper_y + 10), (0, 255, 255), 2)

        # mark the center with a rectangle (red)
        cv2.rectangle(frame_out, (center_x, center_y), (center_x + 10, center_y + 10), (0, 0, 255), 2)

        # calucalate the position between the center and bottom points
        upper_x = center_x + (mid_upper_x - center_x) // 2
        upper_y = center_y + (mid_upper_y - center_y) // 2

        # mark the middle point between the center and bottom point with an rectangle (blue)
        upper_x, upper_y = np.int0([upper_x, upper_y])
        cv2.rectangle(frame_out, (upper_x, upper_y), (upper_x + 10, upper_y + 10), (255, 0, 0), 2)

        return upper_x, upper_y
    

    def calculate_bottom_points(self, frame_out, box, center_x, center_y):
        # sort the points of the box with their y coordinate
        box = sorted(box, key=lambda p: p[1])

        # the last two points have the highest y coordinate
        bottom_points = box[2:] 

        # calculate the middle point between these two bottom points
        mid_bottom_x = (bottom_points[0][0] + bottom_points[1][0]) // 2
        mid_bottom_y = (bottom_points[0][1] + bottom_points[1][1]) // 2

        # mark the position with a rectangle (yellow)
        cv2.rectangle(frame_out, (mid_bottom_x, mid_bottom_y), (mid_bottom_x + 10, mid_bottom_y + 10), (0, 255, 255), 2)

        # mark the center with a rectangle (red)
        cv2.rectangle(frame_out, (center_x, center_y), (center_x + 10, center_y + 10), (0, 0, 255), 2)

        # calucalate the position between the center and bottom points
        bottom_x = center_x + (mid_bottom_x - center_x) // 2
        bottom_y = center_y + (mid_bottom_y - center_y) // 2

        # mark the middle point between the center and bottom point with an rectangle (blue)
        bottom_x, bottom_y = np.int0([bottom_x, bottom_y])
        cv2.rectangle(frame_out, (bottom_x, bottom_y), (bottom_x + 10, bottom_y + 10), (255, 0, 0), 2)

        return bottom_x, bottom_y


    def get_position_of_ith_object(self, i):
        points = [(data[0], data[1]) for data in self.__object_to_parameter[i]]

        mean_x = sum([x for (x, y) in points]) / len(points)
        mean_y = sum([y for (x, y) in points]) / len(points)

        print(f"Point to grab: (x = %0.2f, y = %0.2f)" % (mean_x, mean_y))

        return mean_x, mean_y
    
    def get_angle_of_ith_object(self, i):
        angles = [(data[2]) for data in self.__object_to_parameter[i]]

        mean_angle = sum(angles) / len(angles)

        print(f"Angle to grab: alpha = %0.2f" % mean_angle)

        return mean_angle
    
    def get_rotation_direction_of_ith_object(self, i):
        # The value should be for one object consistent.
        # Therefore we do not need to calculate the mean of the roation direction
        # So we can just use the first value in the list

        rotation_direction = self.__object_to_parameter[i][0][3]

        print(f"Rotation direction: %d" % rotation_direction)

        return rotation_direction
    
    def get_object_type_of_ith_object(self, i):
        lengths = [(data[4]) for data in self.__object_to_parameter[i]]

        mean_length = sum(lengths) / len(lengths)
        object_type = calculate_object_type(mean_length)

        print(f"Type of object: alpha = %s" % object_type)

        return object_type
    
    def get_number_of_objects(self):
        # Decrement the length because we have always one default entry [(-1, -1, -1, -1, -1)] 

        number_of_objects = len(self.__object_to_parameter) - 1

        print(f"Number of objects c = %d" % number_of_objects)
        
        return number_of_objects