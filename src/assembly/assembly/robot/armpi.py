class ArmPi():
    def __init__(self, ID, last_robot):
        self.__got_delivery = False
        self.__finish = False
        self.__ID = ID
        self.__last_robot = last_robot

    def set_delivery_flag(self, flag):
        self.__got_delivery = flag

    def get_delivery_flag(self):
        return self.__got_delivery
    
    def set_finish_flag(self, flag):
        self.__finish = flag

    def get_finish_flag(self):
        return self.__finish
    
    def get_ID(self):
        return self.__ID
    
    def get_last_robot_flag(self):
        return self.__last_robot