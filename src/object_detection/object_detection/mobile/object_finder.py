from object_detection.Aobject_finder import AObjectFinder
import cv2
import numpy as np
import time
import math

class ObjectFinder(AObjectFinder):

    def __init__(self):
        super().__init__()
        self.img_out = None

    def __calculate_object_parameters(self, img, color_range, upper):
        number_of_data_points = 0
        data_list = []

        frame_resize = cv2.resize(img, (640, 480), interpolation=cv2.INTER_NEAREST)

        # Apply Gaussian Blur to reduce noise and improve edge detection
        blurred = cv2.GaussianBlur(frame_resize, (11, 11), 0)

        frame_lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)

        frame_mask = cv2.inRange(frame_lab, np.array(color_range['min']), np.array(color_range['max']))  # mathematical operation on the original image and mask
        opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6,6),np.uint8))  # Opening (morphology)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((6,6),np.uint8)) # Closing (morphology)

        # Find contours in the image
        contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]

        for contour in contours:
            contour_area = math.fabs(cv2.contourArea(contour)) 
            if contour_area < 400: # contour is too small
                continue

            x, y, w, h = cv2.boundingRect(contour)
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
            length01 = self.calculate_distance(box[0], box[1])
            length02 = self.calculate_distance(box[1], box[2])
            min_length = length01
            rotation_direction = -1
            if (min_length > length02):
                min_length = length02
                rotation_direction = 1
            
            
            # calculate the center of the rectangle
            center_x = x + w // 2
            center_y = y + h // 2

            if (upper):
                x, y = self.calculate_upper_points(img, box, center_x, center_y)
            else:
                x, y = self.calculate_bottom_points(img, box, center_x, center_y)

            angle = rect[2]

            # calculate the angle based on the rotation direction of the object
            if rotation_direction == 1:
                # If the object is right-rotated, then we need to subtract 90 from the angle
                # because the angle from cv2.minAreaRect is between the contour and the y-axis
                angle = angle
            else:
                # If the object is left-rotated, then we need to subtract 90 from the angle
                # because the angle from cv2.minAreaRect is between the contour and the x-axis
                angle = 90 - angle
            
            data_list += [(x, y, angle, rotation_direction, min_length)]
            number_of_data_points += 1

        # only wait for 5 seconds
        #if time.time() - start_time >= 5:
        #    break
        

        self.img_out = img

        # Sort the data after their x coordinates
        self.sorted_data = sorted(data_list, key=lambda d: d[0])
        self.collect_data_to_dictionary()

        return img  


    def calculate_upper_parameters(self, img, color_range):
        self.__calculate_object_parameters(img, color_range, upper=True)

    def calculate_bottom_parameters(self, img, color_range):
        self.__calculate_object_parameters(img, color_range, upper=False)

    def get_image_with_marks(self):
        return self.img_out