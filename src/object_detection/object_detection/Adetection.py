from rclpy.node import Node

import cv2
import math
import numpy as np

from object_detection.object_type import calculate_object_type
from object_detection.grab_type import GrabType


class ADetection(Node):

    def __init__(self, node_name):
        super().__init__(node_name)
        self.sorted_data = []
        self.__object_to_parameter = {}

    def _calculate_contours(self, frame_mask):
        opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6, 6), np.uint8))  # Opening (morphology)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((6, 6), np.uint8))  # Closing (morphology)
        # Find contours in the image
        contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]
        return contours

    # euclidean distance
    def _calculate_distance(self, point_a, point_b):
        x_pow = math.pow(point_b[0] - point_a[0], 2)
        y_pow = math.pow(point_b[1] - point_a[1], 2)
        return math.sqrt(x_pow + y_pow)

    def _collect_data_to_dictionary(self):
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

    def _determine_rotation_direction(self, box):
        length01 = self._calculate_distance(box[0], box[1])
        length02 = self._calculate_distance(box[1], box[2])
        min_length = length01
        rotation_direction = -1
        if min_length > length02:
            min_length = length02
            rotation_direction = 1
        return min_length, rotation_direction

    def _calculate_angle_based_on_rotation_direction(self, angle, rotation_direction):
        if rotation_direction == 1:
            # If the object is right-rotated, then we need to subtract 90 from the angle
            # because the angle from cv2.minAreaRect is between the contour and the y-axis
            angle = angle
        else:
            # If the object is left-rotated, then we need to subtract 90 from the angle
            # because the angle from cv2.minAreaRect is between the contour and the x-axis
            angle = 90 - angle
        return angle

    def _calculate_x_y_coordinates(self, frame_out, box, center_x, center_y,  grab_type):
        if grab_type == GrabType.UPPER:
            x, y = self.__calculate_upper_points(frame_out, box, center_x, center_y)
        elif grab_type == GrabType.MIDDLE:
            x, y = center_x, center_y
        elif grab_type == GrabType.BOTTOM:
            x, y = self.__calculate_bottom_points(frame_out, box, center_x, center_y)
        return x, y

    def __calculate_upper_points(self, frame_out, box, center_x, center_y):
        # sort the points of the box with their y coordinate
        box = sorted(box, key=lambda p: p[1])

        # the first two points have the lowest y coordinate
        upper_points = box[0:2]
        upper_x, upper_y = self.__calculate_points(center_x, center_y, frame_out, upper_points)

        return upper_x, upper_y

    def __calculate_bottom_points(self, frame_out, box, center_x, center_y):
        # sort the points of the box with their y coordinate
        box = sorted(box, key=lambda p: p[1])

        # the last two points have the highest y coordinate
        bottom_points = box[2:]
        bottom_x, bottom_y = self.__calculate_points(center_x, center_y, frame_out, bottom_points)

        return bottom_x, bottom_y


    def __calculate_points(self, center_x, center_y, frame_out, upper_points):
        # calculate the middle point between these two bottom points
        mid_x = (upper_points[0][0] + upper_points[1][0]) // 2
        mid_y = (upper_points[0][1] + upper_points[1][1]) // 2

        # mark the position with a rectangle (yellow)
        cv2.rectangle(frame_out, (mid_x, mid_y), (mid_x + 10, mid_y + 10), (0, 255, 255), 2)

        # mark the center with a rectangle (red)
        cv2.rectangle(frame_out, (center_x, center_y), (center_x + 10, center_y + 10), (0, 0, 255), 2)

        # calucalate the position between the center and bottom points
        _x = center_x + (mid_x - center_x) // 2
        _y = center_y + (mid_y - center_y) // 2

        # mark the middle point between the center and bottom point with a rectangle (blue)
        x, y = np.int0([_x, _y])
        cv2.rectangle(frame_out, (x, y), (x + 10, y + 10), (255, 0, 0), 2)

        return x, y


    def get_position_of_ith_object(self, i):
        points = [(data[0], data[1]) for data in self.__object_to_parameter[i]]

        mean_x = sum([x for (x, y) in points]) / len(points)
        mean_y = sum([y for (x, y) in points]) / len(points)

        return mean_x, mean_y

    def get_angle_of_ith_object(self, i):
        angles = [(data[2]) for data in self.__object_to_parameter[i]]
        mean_angle = sum(angles) / len(angles)
        return mean_angle

    def get_rotation_direction_of_ith_object(self, i):
        # The value should be for one object consistent.
        # Therefore, we do not need to calculate the mean of the rotation direction
        # So we can just use the first value in the list
        rotation_direction = self.__object_to_parameter[i][0][3]
        return rotation_direction

    def get_object_type_of_ith_object(self, i):
        lengths = [(data[4]) for data in self.__object_to_parameter[i]]

        mean_length = sum(lengths) / len(lengths)
        object_type = calculate_object_type(mean_length)

        return object_type

    def get_number_of_objects(self):
        # Decrement the length because we have always one default entry [(-1, -1, -1, -1, -1)]
        number_of_objects = len(self.__object_to_parameter) - 1
        return number_of_objects