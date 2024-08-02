class ArmPi():
    def __init__(self, ID):
        self.__ID = ID
        self.__ready = False
        self.__finish = False
        self.__got_position = False
        self.__position_with_angle = None

    def get_ID(self):
        return self.__ID
    
    def set_ready_flag(self, flag):
        self.__ready = flag

    def get_ready_flag(self):
        return self.__ready

    def set_finish_flag(self, flag):
        self.__finish = flag

    def get_finish_flag(self):
        return self.__finish
    
    def get_got_position_flag(self):
        return self.__got_position
    
    def set_got_position_flag(self, flag):
        self.__got_position = flag

    def set_position_with_angle(self, x, y, z, angle):
        self.__position_with_angle = (x, y, z, angle)

    def get_position_with_angle(self):
        return self.__position_with_angle

    