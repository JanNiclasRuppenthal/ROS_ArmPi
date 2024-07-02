import sys
sys.path.append('/home/pi/ArmPi/')
import cv2
import time
import Camera
import math
import numpy as np
#from LABConfig import color_range
from ArmIK.Transform import *
from ArmIK.ArmMoveIK import *

import HiwonderSDK.Board as Board
from CameraCalibration.CalibrationConfig import *

#AK = ArmIK()

size = (640, 480)

color_range = {
'red': [(0, 151, 100), (255, 255, 255)], 
'green': [(0, 0, 0), (255, 115, 255)], 
'blue': [(0, 0, 0), (255, 255, 110)], 
'black': [(0, 0, 0), (56, 255, 255)], 
'white': [(193, 0, 0), (255, 250, 255)], 
}

range_rgb = {
    'red':   (0, 0, 255),
    'blue':  (255, 0, 0),
    'green': (0, 255, 0),
    'black': (0, 0, 0),
    'white': (255, 255, 255),
}

__target_color = ['red']

# find the maximum area contour
# the parameter is a list of contours to be compared
def getAreaMaxContour(contours):
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

unreachable = False
__isRunning = True
count = 0
color_list = []
get_roi = False
__isRunning = False
detect_color = 'None'
start_pick_up = False
start_count_t1 = True

t1 = 0
roi = ()
center_list = []
last_x, last_y = 0, 0
draw_color = range_rgb["black"]
world_x, world_y = 0, 0

def run(img):
    global roi
    global rect
    global count
    global get_roi
    global center_list
    global unreachable
    global __isRunning
    global start_pick_up
    global rotation_angle
    global last_x, last_y
    global world_X, world_Y
    global world_x, world_y
    global start_count_t1, t1
    global detect_color, draw_color, color_list
    
    img_copy = img.copy()
    img_h, img_w = img.shape[:2]
    cv2.line(img, (0, int(img_h / 2)), (img_w, int(img_h / 2)), (0, 0, 200), 1)
    cv2.line(img, (int(img_w / 2), 0), (int(img_w / 2), img_h), (0, 0, 200), 1)

    if not __isRunning:
        return img

    frame_resize = cv2.resize(img_copy, size, interpolation=cv2.INTER_NEAREST)
    frame_gb = cv2.GaussianBlur(frame_resize, (11, 11), 11)
    # If it is detected with a aera recognized object, the area will be detected ubtil there is no object
    if get_roi and not start_pick_up:
        get_roi = False
        frame_gb = getMaskROI(frame_gb, roi, size)      
    frame_lab = cv2.cvtColor(frame_gb, cv2.COLOR_BGR2LAB)  # convert the image to LAB space

    color_area_max = None
    max_area = 0
    areaMaxContour_max = 0
    
    if not start_pick_up:
        for i in color_range:
            if i in __target_color:
                frame_mask = cv2.inRange(frame_lab, color_range[i][0], color_range[i][1])  # mathematical operation on the original image and mask
                opened = cv2.morphologyEx(frame_mask, cv2.MORPH_OPEN, np.ones((6,6),np.uint8))  # Opening (morphology)
                closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, np.ones((6,6),np.uint8)) # Closing (morphology)
                contours = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # find countour
                areaMaxContour, area_max = getAreaMaxContour(contours)  # find the maximum countour
                if areaMaxContour is not None:
                    if area_max > max_area:# find the maximum area
                        max_area = area_max
                        color_area_max = i
                        areaMaxContour_max = areaMaxContour
        if max_area > 2500:  # have found the maximum area
            rect = cv2.minAreaRect(areaMaxContour_max)
            box = np.int0(cv2.boxPoints(rect))
            
            roi = getROI(box) # get roi zone
            get_roi = True
            img_centerx, img_centery = getCenter(rect, roi, size, square_length)  # get the center coordinates of block
             
            world_x, world_y = convertCoordinate(img_centerx, img_centery, size) # convert to world coordinates
            
            cv2.drawContours(img, [box], -1, range_rgb[color_area_max], 2)
            cv2.putText(img, '(' + str(world_x) + ',' + str(world_y) + ')', (min(box[0, 0], box[2, 0]), box[2, 1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, range_rgb[color_area_max], 1) # draw center position
            
            distance = math.sqrt(pow(world_x - last_x, 2) + pow(world_y - last_y, 2)) # compare the last coordinate to determine whether to move
            last_x, last_y = world_x, world_y
            if not start_pick_up:
                if color_area_max == 'red':  # red area is the maximum
                    color = 1
                elif color_area_max == 'green':  # green area is the maximum
                    color = 2
                elif color_area_max == 'blue':  # blue area is the maximum
                    color = 3
                else:
                    color = 0
                color_list.append(color)
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
                        start_pick_up = True
                else:
                    t1 = time.time()
                    start_count_t1 = True
                    center_list = []
                    count = 0

                if len(color_list) == 3:  # multiple judgments
                    # take evaluation value
                    color = int(round(np.mean(np.array(color_list))))
                    color_list = []
                    if color == 1:
                        detect_color = 'red'
                        draw_color = range_rgb["red"]
                    elif color == 2:
                        detect_color = 'green'
                        draw_color = range_rgb["green"]
                    elif color == 3:
                        detect_color = 'blue'
                        draw_color = range_rgb["blue"]
                    else:
                        detect_color = 'None'
                        draw_color = range_rgb["black"]
        else:
            if not start_pick_up:
                draw_color = (0, 0, 0)
                detect_color = "None"
    
    print("Pos: %s, %s" % (world_x, world_y))

    cv2.putText(img, "Color: " + detect_color, (10, img.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.65, draw_color, 2)
    return img
    

def run_camera():
    global __isRunning
    __isRunning = True
    __target_color = ('red', 'green', 'blue')
    my_camera = Camera.Camera()
    my_camera.camera_open()
    while True:
        img = my_camera.frame
        if img is not None:
            frame = img.copy()
            Frame = run(frame)           
            #cv2.imshow('Frame', Frame)
            key = cv2.waitKey(1)
            if key == 27:
                break
    my_camera.camera_close()
    cv2.destroyAllWindows()