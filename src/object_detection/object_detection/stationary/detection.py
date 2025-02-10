from object_detection.Adetection import ADetection

from LABConfig import *
import Camera
import cv2
import numpy as np
import time
import math

class Detection(ADetection):

    def __init__(self, node_name):
        super().__init__(node_name)
        self.__my_camera = Camera.Camera()

    def __close_camera_and_window(self):
        self.__my_camera.camera_close()
        self.__my_camera.reset_last_frame()
        cv2.destroyAllWindows()

    def _calculate_real_world_coordinates(self, x, y):
        x_world_coord = -(23/2) + (x * (23 / 720))
        y_world_coord = 12 + ((y-480) * (16 / -480))
        return x_world_coord, y_world_coord

    def _calculate_object_parameters(self, grab_type, color):
        self.__my_camera.camera_open()
        self.get_logger().info("Opened the stationary camera!")

        number_of_data_points = 0
        max_number_of_data_points = 33
        data_list = []

        start_time = time.time()
        
        while number_of_data_points < max_number_of_data_points:
            img = self.__my_camera.frame
            if img is not None:
                frame = img.copy()

                frame_resize = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_NEAREST)

                # Apply Gaussian Blur to reduce noise and improve edge detection
                blurred = cv2.GaussianBlur(frame_resize, (11, 11), 0)
                frame_lab = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
                frame_mask = cv2.inRange(frame_lab, color_range[color][0], color_range[color][1])  # mathematical operation on the original image and mask
                contours = self._calculate_contours(frame_mask)
                
                frame_out = frame.copy()

                for contour in contours:
                    contour_area = math.fabs(cv2.contourArea(contour)) 
                    if contour_area < 400: # contour is too small
                        continue

                    x, y, w, h = cv2.boundingRect(contour)
                    rect = cv2.minAreaRect(contour)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)

                    cv2.drawContours(frame_out, [box], 0, (0, 255, 0), 2)
                    min_length, rotation_direction = self._determine_rotation_direction(box)

                    # calculate the center of the rectangle
                    center_x = x + w // 2
                    center_y = y + h // 2

                    x, y = self._calculate_x_y_coordinates(frame_out, box, center_x, center_y, grab_type)

                    angle_of_rect = rect[2]
                    angle = self._calculate_angle_based_on_rotation_direction(angle_of_rect, rotation_direction)

                    # Calculate position in real-world coordinates (linear interpolation)
                    pos_x, pos_y = self._calculate_real_world_coordinates(x, y)
                    
                    data_list += [(pos_x, pos_y, angle, rotation_direction, min_length)]
                    number_of_data_points += 1
                    start_time = time.time()
            
                '''
                # Display the resulting frame
                cv2.imshow('Frame', frame_out)

                # Break the loop on 'ESC' key press
                key = cv2.waitKey(30)
                if key == 27:  # ESC key
                    break
                '''

            # only wait for 5 seconds
            if time.time() - start_time >= 5:
                self.get_logger().warn("After 5 seconds, I abort the detection of the pipes!")
                self.__close_camera_and_window()
                break


        self.get_logger().info("Collected all necessary parameters of all pipes!")

        # Sort the data after their x coordinates
        self.sorted_data = sorted(data_list, key=lambda d: d[0])
        self._collect_data_to_dictionary()

        self.get_logger().info("Sorted and collected all data!")

        # Release the camera and close all OpenCV windows
        self.__close_camera_and_window()
        self.get_logger().info("Closed the stationary camera!")
