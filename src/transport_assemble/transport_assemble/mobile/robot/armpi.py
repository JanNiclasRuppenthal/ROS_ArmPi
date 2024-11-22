class ArmPi():
    def __init__(self, id):
        self.__ID = id
        self.__first_robot_hold_pipe = True

        self.__permission_to_do_next_step_for_assembly = False

    def get_ID(self):
        return self.__ID
    
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