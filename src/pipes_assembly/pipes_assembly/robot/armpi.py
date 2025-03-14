from assembly_queue.assembly_queue_states import AssemblyQueueStates

class ArmPi(AssemblyQueueStates):
    def __init__(self, ID, number_of_robots):
        super().__init__()
        self.__ID = ID
        self.__number_of_robots = number_of_robots
        self.__ready_flag = False
        self.__done_flag = False
        self.__finish_flag = False
        self.__position_with_angle = None

    def get_ID(self) -> int:
        return self.__ID
    
    def get_number_of_robots(self) -> int:
        return self.__number_of_robots
    
    def set_ready_flag(self, flag):
        self.__ready_flag = flag

    def get_ready_flag(self) -> bool:
        return self.__ready_flag
    
    def set_done_flag(self, flag):
        self.__done_flag = flag

    def get_done_flag(self) -> bool:
        return self.__done_flag

    def set_finish_flag(self, flag):
        self.__finish_flag = flag

    def get_finish_flag(self) -> bool:
        return self.__finish_flag

    def set_position_with_angle(self, x, y, z, angle):
        self.__position_with_angle = (x, y, z, angle)

    def get_position_with_angle(self):
        return self.__position_with_angle