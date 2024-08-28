import cv2
import sys
sys.path.append('/home/pi/ArmPi/')
import Camera
import math
import numpy as np
import time

def getAreaMaxContour(contours):
    contour_area_temp = 0
    contour_area_max = 0
    area_max_contour = None

    for c in contours:  
        contour_area_temp = math.fabs(cv2.contourArea(c)) 
        if contour_area_temp > contour_area_max:
            contour_area_max = contour_area_temp
            if contour_area_temp > 200:  
                area_max_contour = c

    return area_max_contour, contour_area_max 

def close_camera_and_window(my_camera):
    my_camera.camera_close()
    cv2.destroyAllWindows()

def calculate_position_and_angle():
    my_camera = Camera.Camera()
    my_camera.camera_open()

    calculated_points = (0, 0)
    calculated_angles = 0
    number_of_data_points = 0
    max_number_of_data_points = 20

    start_time = time.time()
    
    while number_of_data_points < max_number_of_data_points:
        img = my_camera.frame
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
            areaMaxContour, area_max = getAreaMaxContour(contours)
            if area_max > 500:
                x, y, w, h = cv2.boundingRect(areaMaxContour)
                rect = cv2.minAreaRect(areaMaxContour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                cv2.drawContours(frame_out, [box], 0, (0, 255, 0), 2)

                # sort the points of the box with their y coordinate
                box = sorted(box, key=lambda p: p[1])

                # the last two points have the highest y coordinate
                bottom_points = box[2:] 

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

                
                calculated_points = (calculated_points[0] + pos_x, calculated_points[1] + pos_y)
                calculated_angles += angle
                number_of_data_points += 1
                start_time = time.time()
                print("Got Position!")


            ''' Comment this out, if you want to see the frames
            # Display the resulting frame
            #cv2.imshow('Frame', frame_out)

            # Break the loop on 'ESC' key press
            #key = cv2.waitKey(30)
            #if key == 27:  # ESC key
            #    break
            '''

        # only wait for 5 seconds
        if time.time() - start_time >= 5:
            close_camera_and_window(my_camera)

            if number_of_data_points != 0:
                break

            return -1, -1, -1, -1

    # Determine the rotation direction
    if bottom_points[0][0] < bottom_points[1][0]:
        rotation_direction = 1
    else:
        rotation_direction = -1

    
    point = calculated_points[0] / number_of_data_points, calculated_points[1] / number_of_data_points
    angle = calculated_angles / number_of_data_points

    # Release the camera and close all OpenCV windows
    close_camera_and_window(my_camera)

    print(f"Point to grab: {str(point)}")
    print(f"Angle to grab: {str(angle)}")
    print(f"Rotation direction: {rotation_direction}")
    x = point[0]
    y = point[1]

    return x, y, angle, rotation_direction