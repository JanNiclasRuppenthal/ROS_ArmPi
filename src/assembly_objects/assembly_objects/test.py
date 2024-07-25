import cv2
import sys
sys.path.append('/home/pi/ArmPi/')
import Camera
import math

from ArmIK.Transform import *
import numpy as np

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

# get the center coordinates of the block
# load in the rect object returned by the minAreaRect function,the extreme point of the block, the image resolution, the side length of the block
def getCenter2(rect, roi, size, square_length):
    x_min, x_max, y_min, y_max = roi
    # according to the coordinates of the center of the wood block, the vertex closest to the center of the image is selected as the basis for calculating the accurate center
    if rect[0][0] >= size[0]/2:
        x = x_max 
    else:
        x = x_min
    if rect[0][1] >= size[1]/2:
        y = y_max
    else:
        y = y_min

    # calculate the diagonal length of the block
    square_l = (pow(x ,2) + pow(y, 2)) #square_length/math.cos(math.pi/4)

    # convert length to pixel length
    square_l = world2pixel(square_l, size)

    # calculate the center point based on the rotation angle of the block
    dx = abs(math.cos(math.radians(45 - abs(rect[2]))))
    dy = abs(math.sin(math.radians(45 + abs(rect[2]))))
    if rect[0][0] >= size[0] / 2:
        x = round(x - (square_l/2) * dx, 2)
    else:
        x = round(x + (square_l/2) * dx, 2)
    if rect[0][1] >= size[1] / 2:
        y = round(y - (square_l/2) * dy, 2)
    else:
        y = round(y + (square_l/2) * dy, 2)

    return  x, y

def main():
    my_camera = Camera.Camera()
    my_camera.camera_open()
    
    while True:
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
            if area_max > 2000:
                x, y, w, h = cv2.boundingRect(areaMaxContour)
                rect = cv2.minAreaRect(areaMaxContour)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                # Draw the bounding rectangle
                cv2.drawContours(frame_out, [box], 0, (0, 255, 0), 2)

                center_x = x + w // 2
                center_y = y + h // 2
                # Draw the center point
                cv2.rectangle(frame_out, (center_x, center_y), (center_x + 10, center_y + 10), (0, 0, 255), 2)

                # The object has a length of 10 cm
                object_length = 10
                one_fifth_length = object_length / 5

                angle_deg = rect[2]
                angle_rad = math.radians(angle_deg)

                # Calculate position in real-world coordinates
                pos_x = -11.5 + (x + (w / 2)) * 0.0359375
                pos_y = 28 - (y + (h / 2)) * (1 / 30)

                x_ = pos_x - one_fifth_length * math.sin(angle_deg)
                y_ = pos_y - one_fifth_length * math.cos(angle_deg)

                # Print the calculated positions and angle
                print("Positions: (%f, %f)" % (pos_x, pos_y))
                print("1/5 Positions: (%f, %f)" % (x_, y_))
                print("Angle in radians: %f" % angle_rad)
                print("Angle in degrees: %f" % angle_deg)

            # Display the resulting frame
            cv2.imshow('Frame', frame_out)



            # Break the loop on 'ESC' key press
            key = cv2.waitKey(30)
            if key == 27:  # ESC key
                break

    # Release the camera and close all OpenCV windows
    my_camera.camera_close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
