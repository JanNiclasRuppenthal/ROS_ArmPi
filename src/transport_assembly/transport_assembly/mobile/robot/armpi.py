class ArmPi():
    def __init__(self, number):
        self.__ID = 0
        self.__number_of_stationary_robots = number
        self.__first_robot_hold_pipe = True
        self.__permission_to_do_next_step_for_assembly = False
        self.__finish_flag = False
        self.__IDList = []
        self.__assembly_order_status = False

    def get_ID(self):
        return self.__ID

    def get_number_of_stationary_robots(self):
        return self.__number_of_stationary_robots

    def get_first_robot_hold_pipe(self):
        return self.__first_robot_hold_pipe

    def set_first_robot_hold_pipe(self, bool_value):
        self.__first_robot_hold_pipe = bool_value

    def reset_first_robot_hold_pipe(self):
        self.__first_robot_hold_pipe = True

    def get_permission_to_do_next_assembly_step(self):
        return self.__permission_to_do_next_step_for_assembly

    def set_permission_to_do_next_assembly_step(self, value):
        self.__permission_to_do_next_step_for_assembly = value

    def get_finish_flag(self):
        return self.__finish_flag

    def set_finish_flag(self, value):
        self.__finish_flag = value

    def get_IDList(self):
        return self.__IDList

    def set_IDList(self, list):
        self.__IDList = list

    def get_first_ID_IDList(self):
        if (self.is_empty_IDList()):
            return -1

        return self.__IDList[0]

    def is_full_IDList(self):
        return len(self.__IDList) == self.__number_of_stationary_robots

    def is_empty_IDList(self):
        return len(self.__IDList) == 0

    def pop_IDList(self):
        if (self.is_empty_IDList()):
            return -1

        return self.__IDList.pop(0)

    def get_assembly_order_status(self):
        return self.__assembly_order_status

    def set_assembly_order_status(self, value):
        self.__assembly_order_status = value