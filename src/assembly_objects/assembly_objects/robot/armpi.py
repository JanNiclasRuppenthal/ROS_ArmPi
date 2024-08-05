class ArmPi():
    def __init__(self, ID, number_of_robots):
        self.__ID = ID
        self.__number_of_robots = number_of_robots
        self.__ready = False
        self.__done = False
        self.__finish = False
        self.__position_with_angle = None

    def get_ID(self):
        return self.__ID
    
    def get_number_of_robots(self):
        return self.__number_of_robots
    
    def set_ready_flag(self, flag):
        self.__ready = flag

    def get_ready_flag(self):
        return self.__ready
    
    def set_done_flag(self, flag):
        self.__done = flag

    def get_done_flag(self):
        return self.__done

    def set_finish_flag(self, flag):
        self.__finish = flag

    def get_finish_flag(self):
        return self.__finish

    def set_position_with_angle(self, x, y, z, angle):
        self.__position_with_angle = (x, y, z, angle)

    def get_position_with_angle(self):
        return self.__position_with_angle

    