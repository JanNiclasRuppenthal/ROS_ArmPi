import Camera
import cv2

class Cam():
    def __init__(self):
        self.__camera = Camera.Camera()

    def open(self):
        self.__camera.camera_open()
    
    def shutdown(self):
        self.__camera.camera_close()
        cv2.destroyAllWindows()

    def get_camera(self):
        return self.__camera