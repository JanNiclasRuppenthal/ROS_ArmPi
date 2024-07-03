import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import Camera
import math
import numpy as np
from LABConfig import color_range
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *

import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *

#AK = ArmIK()

size = (640, 480)

range_rgb = {
    'red':   (0, 0, 255),
    'blue':  (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}

__target_color = ['red', 'green', 'blue']
unreachable = False
count = 0
color_list = []
get_roi = False
detect_color = 'None'
start_count_t1 = True

t1 = 0
roi = ()
center_list = []
last_x, last_y = 0, 0
draw_color = range_rgb["black"]
world_x, world_y = -1, -1

def get_coordinates():
    pos = __get_position()
    print(str(pos))
    return pos


def __get_position():
    my_camera = Camera.Camera()
    my_camera.camera_open()
    while True:
        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            pos = run(frame)
            key = cv2.waitKey(1)
            if key == 27:
                break

            if pos != (-1, -1):
                break

    my_camera.camera_close()
    cv2.destroyAllWindows()

    return pos


def run(img):
    global roi
    global rect
    global count
    global get_roi
    global center_list
    global unreachable
    global rotation_angle
    global last_x, last_y
    global world_X, world_Y
    global world_x, world_y
    global start_count_t1, t1
    global detect_color, color_list
    
    img_copy = img.copy()
    frame_resize = cv2.resize(img_copy, size, interpolation=cv2.INTER_NEAREST)
    frame_gb = cv2.GaussianBlur(frame_resize, (11, 11), 11)
    # If it is detected with a aera recognized object, the area will be detected until there is no object
    if get_roi:
        get_roi = False
        frame_gb = getMaskROI(frame_gb, roi, size)      
    frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # convert the image to LAB space

    max_area = 0
    areaMaxContour = 0
    
    while True:
        for color in color_range:
            if color in __target_color:
                contours = __get_contours(frame_lab, color_range[color][0], color_range[color][1])
                areaContour, area = __getAreaMaxContour(contours)  # find the maximum countour

                #Test if we found a bigger area
                if areaContour is not None:
                    if area > max_area:
                        max_area = area
                        areaMaxContour = areaContour
            
        if max_area > 2500:  # have found the maximum area
            img_center_x, img_center_y = __get_image_center(areaMaxContour)
            
            world_x, world_y = convertCoordinate(img_center_x, img_center_y, size) # convert to world coordinates
                
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
                    rotation_angle = rect[2] 
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
            return (-1, -1)
    

def __get_contours(frame_lab, start_color, end_color):
    frame_mask = cv2.inRange(frame_lab, start_color, end_color)  # mathematical operation on the original image and mask
    opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6,6),np.uint8))  # Opening (morphology)
    closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((6,6),np.uint8)) # Closing (morphology)
    contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # find countour
    return contours


# find the maximum area contour
# the parameter is a list of contours to be compared
def __getAreaMaxContour(contours):
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


def __get_image_center(areaMaxContour):
    global rect, get_roi
    rect = cv2.minAreaRect(areaMaxContour)
    box = np.int0(cv2.boxPoints(rect))
    roi = getROI(box) # get roi zone
    get_roi = True
    img_center_x, img_center_y = getCenter(rect, roi, size, square_length)  # get the center coordinates of block
    return img_center_x, img_center_y