from object_detection.Adetection import ADetection
import cv2
import numpy as np
import math

from object_detection.grab_type import GrabType


class PipeDetection(ADetection):

    def __init__(self):
        super().__init__("pipe_detection_node")
        self.img_out = None

    def __calculate_object_parameters(self, img, color_range, grab_type):
        data_list = []

        frame_resize = cv2.resize(img, (640, 480), interpolation=cv2.INTER_NEAREST)

        # Apply Gaussian Blur to reduce noise and improve edge detection
        blurred = cv2.GaussianBlur(frame_resize, (11, 11), 0)
        frame_lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
        frame_mask = cv2.inRange(frame_lab, np.array(color_range['min']), np.array(color_range['max']))  # mathematical operation on the original image and mask
        contours = self._calculate_contours(frame_mask)

        for contour in contours:
            contour_area = math.fabs(cv2.contourArea(contour)) 
            if contour_area < 400: # contour is too small
                continue

            x, y, w, h = cv2.boundingRect(contour)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
            min_length, rotation_direction = self._determine_rotation_direction(box)
            
            
            # calculate the center of the rectangle
            center_x = x + w // 2
            center_y = y + h // 2

            x, y = self._calculate_x_y_coordinates(img, box, center_x, center_y, grab_type)

            angle_of_rect = rect[2]
            angle = self._calculate_angle_based_on_rotation_direction(angle_of_rect, rotation_direction)
            
            data_list += [(x, y, angle, rotation_direction, min_length)]

        # only wait for 5 seconds
        #if time.time() - start_time >= 5:
        #    break

        self.img_out = img

        # Sort the data after their x coordinates
        self.sorted_data = sorted(data_list, key=lambda d: d[0])
        self._collect_data_to_dictionary()

        return img

    def calculate_upper_parameters(self, img, color_range):
        self.__calculate_object_parameters(img, color_range, GrabType.UPPER)

    def calculate_bottom_parameters(self, img, color_range):
        self.__calculate_object_parameters(img, color_range, GrabType.BOTTOM)

    def get_image_with_marks(self):
        return self.img_out