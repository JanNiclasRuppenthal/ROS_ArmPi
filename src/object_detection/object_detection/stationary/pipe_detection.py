from object_detection.stationary.detection import Detection

class PipeDetection(Detection):

    def calculate_upper_parameters(self):
        self._calculate_object_parameters(upper=True, color='red')

    def calculate_bottom_parameters(self):
        self._calculate_object_parameters(upper=False, color='red')