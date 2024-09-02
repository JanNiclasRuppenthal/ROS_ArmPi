import cv2
import sys
sys.path.append('/home/pi/ArmPi/')
import Camera
import math
import numpy as np
import time

from util.object_type import calculate_object_type

class ObjectFinder():

    def __init__(self):
        self.__my_camera = Camera.Camera()
        self.__point = -1
        self.__angle = -1
        self.__rotation_direction = -1
        self.__object_type = -1
        self.__number_of_objects = -1


    def __close_camera_and_window(self):
        self.__my_camera.camera_close()
        cv2.destroyAllWindows()

    # euclidean distance
    def __calculate_distance(self, point_a, point_b):
        x_pow = math.pow(point_b[0] - point_a[0], 2)
        y_pow = math.pow(point_b[1] - point_a[1], 2)
        return math.sqrt(x_pow + y_pow)

    def __count_objects(self, data):
        count = 0
        position_of_objects = []
        for (x, y) in [(d[0], d[1]) for d in data]:
            found_new_object = True
            for (prev_x, prev_y) in position_of_objects:
                if abs(x - prev_x) <= 0.5 and abs(y - prev_y) <= 0.5:
                    found_new_object = False
                    break

            
            if found_new_object:
                count += 1

            position_of_objects.append((x, y))

        return count


    def calculate_object_parameters(self):
        self.__my_camera.camera_open()

        number_of_data_points = 0
        max_number_of_data_points = 33
        data_list = []

        start_time = time.time()
        
        while number_of_data_points < max_number_of_data_points:
            img = self.__my_camera.frame
            if img is not None:
                frame = img.copy()

                # Convert to grayscale
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Apply Gaussian Blur to reduce noise and improve edge detection
                blurred = cv2.GaussianBlur(gray, (5, 5), 0)

                # Apply Canny Edge Detector
                edges = cv2.Canny(blurred, 50, 150)

                # Find contours in the edge-detected image
                contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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

                    length01 = self.__calculate_distance(box[0], box[1])
                    length02 = self.__calculate_distance(box[1], box[2])
                    min_length = min(length01, length02)

                    # sort the points of the box with their y coordinate
                    box = sorted(box, key=lambda p: p[1])

                    # the last two points have the highest y coordinate
                    bottom_points = box[2:] 

                    # Determine the rotation direction
                    if bottom_points[0][0] < bottom_points[1][0]:
                        rotation_direction = 1
                    else:
                        rotation_direction = -1

                    # calculate the middle point between these two bottom points
                    mid_bottom_x = (bottom_points[0][0] + bottom_points[1][0]) // 2
                    mid_bottom_y = (bottom_points[0][1] + bottom_points[1][1]) // 2

                    # mark the position with a rectangle (yellow)
                    cv2.rectangle(frame_out, (mid_bottom_x, mid_bottom_y), (mid_bottom_x + 10, mid_bottom_y + 10), (0, 255, 255), 2)

                    # calculate the center of the rectangle
                    center_x = x + w // 2
                    center_y = y + h // 2
                    # mark the center with a rectangle (red)
                    cv2.rectangle(frame_out, (center_x, center_y), (center_x + 10, center_y + 10), (0, 0, 255), 2)

                    # calucalate the position between the center and bottom points
                    final_x = center_x + (mid_bottom_x - center_x) // 2
                    final_y = center_y + (mid_bottom_y - center_y) // 2

                    # mark the middle point between the center and bottom point with an rectangle (blue)
                    final_x, final_y = np.int0([final_x, final_y])
                    cv2.rectangle(frame_out, (final_x, final_y), (final_x + 10, final_y + 10), (255, 0, 0), 2)

                    angle = rect[2]

                    # Calculate position in real-world coordinates (linear interpolation)
                    pos_x = -(23/2) + (final_x * (23 / 720))
                    pos_y = 12 + ((final_y-480) * (16 / -480))

                    
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
                self.__close_camera_and_window()

                if number_of_data_points != 0:
                    break

                return


        # Sort the data after their x coordinates
        sorted_data = sorted(data_list, key=lambda d: d[0])
        left_data = sorted_data[0]
        
        self.__point = left_data[0], left_data[1]
        self.__angle = left_data[2]
        self.__rotation_direction = left_data[3]
        self.__object_type = calculate_object_type(left_data[4])
        self.__number_of_objects = self.__count_objects(sorted_data)

        # Release the camera and close all OpenCV windows
        self.__close_camera_and_window()

        print(f"Point to grab: {str(self.__point)}")
        print(f"Angle to grab: {str(self.__angle)}")
        print(f"Rotation direction: {self.__rotation_direction}")
        print(f"Object type: {self.__object_type}")
        print(f"Get number of found objects: {self.__number_of_objects}")


    def get_position(self):
        return self.__point[0], self.__point[1]
    
    def get_angle(self):
        return self.__angle
    
    def get_rotation_direction(self):
        return self.__rotation_direction
    
    def get_object_type(self):
        return self.__object_type
    
    def get_number_of_objects(self):
        return self.__number_of_objects