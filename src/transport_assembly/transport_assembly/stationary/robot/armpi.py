from assembly_queue.assembly_queue_states import AssemblyQueueStates

class ArmPi(AssemblyQueueStates):
    def __init__(self, ID, number_of_stationary_robots):
        super().__init__()
        self.__ID = ID
        self.__number_of_stationary_robots = number_of_stationary_robots
        self.__letting_go_pipe = False
        self.__permission_to_do_next_step_for_assembly = False
        self.__finish_flag = False
        self.__transporter_received_list = False

    def get_ID(self) -> int:
        return self.__ID

    def get_number_of_robots(self) -> int:
        return self.__number_of_stationary_robots

    def need_to_let_go_pipe(self) -> bool:
        return self.__letting_go_pipe

    def set_letting_go_pipe(self, bool_value):
        self.__letting_go_pipe = bool_value

    def get_permission_to_do_next_assembly_step(self) -> bool:
        return self.__permission_to_do_next_step_for_assembly

    def set_permission_to_do_next_assembly_step(self, value):
        self.__permission_to_do_next_step_for_assembly = value

    def get_finish_flag(self) -> bool:
        return self.__finish_flag

    def set_finish_flag(self, value):
        self.__finish_flag = value

    def did_transporter_received_list(self) -> bool:
        return self.__transporter_received_list

    def set_transporter_received_list(self, value):
        self.__transporter_received_list = value