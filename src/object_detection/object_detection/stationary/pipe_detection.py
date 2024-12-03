from object_detection.stationary.detection import Detection
from object_detection.stationary.grab_type import GrabType

class PipeDetection(Detection):

    def calculate_upper_parameters(self):
        self._calculate_object_parameters(GrabType.UPPER, color='red')

    def calculate_middle_parameters(self):
        self._calculate_object_parameters(GrabType.MIDDLE, color="red")

    def calculate_bottom_parameters(self):
        self._calculate_object_parameters(GrabType.BOTTOM, color='red')