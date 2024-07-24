class ArmPi():
    def __init__(self, ID):
        self.__ID = ID
        self.__ready = False 
        self.__got_position = False
        self.__position_with_angle = None

    def get_ID(self):
        return self.__ID

    def get_ready_flag(self):
        return self.__ready
    
    def get_got_position_flag(self):
        return self.__got_position
    
    def set_got_position_flag(self, flag):
        self.__got_position = flag

    def set_position_with_angle(self, x, y, z, angle):
        self.__position_with_angle = (x, y, z, angle)

    def get_position_with_angle(self):
        return self.__position_with_angle

    