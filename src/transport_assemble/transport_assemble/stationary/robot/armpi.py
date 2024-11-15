class ArmPi():
    def __init__(self, ID, number_of_stationary_robots):
        self.__ID = ID
        self.__number_of_stationary_robots = number_of_stationary_robots
        self.__letting_go_pipe = False

    def get_ID(self):
        return self.__ID
    
    def get_number_of_stationary_robots(self):
        return self.__number_of_stationary_robots
    
    def need_to_let_go_pipe(self):
        return self.__letting_go_pipe
    
    def set_letting_go_pipe(self, bool_value):
        self.__letting_go_pipe = bool_value