import cv2
import time
import math
import numpy as np

from LABConfig import color_range
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *
from CameraCalibration.CalibrationConfig import *

from rclpy.node import Node


class CoordinatesCalculation(Node):
    def __init__(self):
        super().__init__("coordinates_calculation_node")

        self.size = (640, 480)
        self.range_rgb = {
            'red':   (0, 0, 255),
            'blue':  (255, 0, 0),
            'green': (0, 255, 0),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
        }

        self.detected_color = 'None'
        self.rotation_angle = 0


    def get_coordinates(self, cam):
        pos = self.__get_position(cam)
        self.get_logger().info("Position: %s." % str(pos))
        return pos

    def get_detected_color(self):
        self.get_logger().info("Detected color: %s" % self.detected_color)
        return self.detected_color

    def get_rotation_angle(self):
        return self.rotation_angle


    def __get_position(self, cam):
        while True:
            img = cam.get_camera().frame
            if img is not None:
                frame = img.copy()
                pos = self.__calculate_position(frame)
                key = cv2.waitKey(1)
                if key == 27:
                    break

                break

        return pos


    def __calculate_position(self, img):
        count = 0
        t1 = 0
        roi = ()
        center_list = []
        last_x, last_y = 0, 0
        world_x, world_y = -1, -1

        get_roi = False
        img_copy = img.copy()
        frame_resize = cv2.resize(img_copy, self.size, interpolation=cv2.INTER_NEAREST)
        frame_gb = cv2.GaussianBlur(frame_resize, (11, 11), 11)
        # If it is detected with a area recognized object, the area will be detected until there is no object
        if get_roi:
            get_roi = False
            frame_gb = getMaskROI(frame_gb, roi, self.size)
        frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # convert the image to LAB space

        color_area_max = None
        max_area = 0
        areaMaxContour = 0

        while True:
            for color in color_range:
                if color in ['red', 'green', 'blue']:
                    contours = self.__get_contours(frame_lab, color_range[color][0], color_range[color][1])
                    areaContour, area = self.__getAreaMaxContour(contours)  # find the maximum contour

                    #Test if we found a bigger area
                    if areaContour is not None:
                        if area > max_area:
                            max_area = area
                            color_area_max = color
                            areaMaxContour = areaContour

            # Test if the camera could catch a colored cube
            # Sometimes it can detect a black box of a shadow
            if color_area_max not in ['red', 'green', 'blue']:
                self.get_logger().warn("Color does not match RGB!")
            else:
                self.detected_color = color_area_max

            if max_area > 2500:  # have found the maximum area
                img_center_x, img_center_y = self.__get_image_center(areaMaxContour)

                world_x, world_y = convertCoordinate(img_center_x, img_center_y, self.size) # convert to world coordinates

                distance = math.sqrt(pow(world_x - last_x, 2) + pow(world_y - last_y, 2)) # compare the last coordinate to determine whether to move
                last_x, last_y = world_x, world_y

                # cumulative judgment
                if distance < 0.5:
                    count += 1
                    center_list.extend((world_x, world_y))
                    if start_count_t1:
                        start_count_t1 = False
                        t1 = time.time()
                    if time.time() - t1 > 1:
                        self.rotation_angle = rect[2]
                        start_count_t1 = True
                        world_X, world_Y = np.mean(np.array(center_list).reshape(count, 2), axis=0)
                        center_list = []
                        count = 0
                        return world_X, world_Y
                else:
                    t1 = time.time()
                    start_count_t1 = True
                    center_list = []
                    count = 0

            else:
                return -1, -1


    def __get_contours(self, frame_lab, start_color, end_color):
        frame_mask = cv2.inRange(frame_lab, start_color, end_color)  # mathematical operation on the original image and mask
        opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6,6),np.uint8))  # Opening (morphology)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((6,6),np.uint8)) # Closing (morphology)
        contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # find countour
        return contours


    # find the maximum area contour
    # the parameter is a list of contours to be compared
    def __getAreaMaxContour(self, contours):
        contour_area_temp = 0
        contour_area_max = 0
        area_max_contour = None

        for c in contours : # traversal all the contours
            contour_area_temp = math.fabs(cv2.contourArea(c))  # calculate the countour area
            if contour_area_temp > contour_area_max:
                contour_area_max = contour_area_temp
                if contour_area_temp > 300:  # only when the area is greater than 300, the contour of the maximum area is effective to filter interference
                    area_max_contour = c

        return area_max_contour, contour_area_max  # return the maximum area countour


    def __get_image_center(self, areaMaxContour):
        global rect, get_roi, roi
        rect = cv2.minAreaRect(areaMaxContour)
        box = np.int0(cv2.boxPoints(rect))
        roi = getROI(box) # get roi zone
        get_roi = True
        img_center_x, img_center_y = getCenter(rect, roi, self.size, square_length)  # get the center coordinates of block
        return img_center_x, img_center_y