from assemble_queue.transport_assemble.assemble_queue import AssembleQueue

class ArmPi():
    def __init__(self, ID, number_of_stationary_robots):
        self.__ID = ID
        self.__number_of_stationary_robots = number_of_stationary_robots
        self.__letting_go_pipe = False
        self.__position_with_angle = None
        self.__object_type = None
        self.__object_type_value_next_robot = None
        self.__assemble_queue_flag = False
        self.__number_of_objects = -1
        self.__number_of_objects_next_robot = -1
        self.__assemble_queue = AssembleQueue()

        self.__permission_to_do_next_step_for_assembly = False

    def get_ID(self):
        return self.__ID
    
    def get_number_of_stationary_robots(self):
        return self.__number_of_stationary_robots
    
    def need_to_let_go_pipe(self):
        return self.__letting_go_pipe
    
    def set_letting_go_pipe(self, bool_value):
        self.__letting_go_pipe = bool_value

    def set_position_with_angle(self, x, y, z, angle):
        self.__position_with_angle = (x, y, z, angle)

    def get_position_with_angle(self):
        return self.__position_with_angle
    
    def set_object_type(self, obj_type):
        self.__object_type = obj_type
    
    def get_object_type(self):
        return self.__object_type
    
    def set_assemble_queue_flag(self, flag):
        self.__assemble_queue_flag = flag

    def get_assemble_queue_flag(self):
        return self.__assemble_queue_flag
    
    def get_object_type_value_next_robot(self):
        return self.__object_type_value_next_robot
    
    def set_object_type_value_next_robot(self, obj_type):
        self.__object_type_value_next_robot = obj_type

    def get_number_of_objects(self):
        return self.__number_of_objects
    
    def set_number_of_objects(self, number):
        self.__number_of_objects = number

    def get_number_of_objects_next_robot(self):
        return self.__number_of_objects_next_robot
    
    def set_number_of_objects_next_robot(self, number):
        self.__number_of_objects_next_robot = number

    def get_assemble_queue(self):
        return self.__assemble_queue
    
    def get_permission_to_do_next_assembly_step(self):
        return self.__permission_to_do_next_step_for_assembly
    
    def set_permission_to_do_next_assembly_step(self, value):
        self.__permission_to_do_next_step_for_assembly = value