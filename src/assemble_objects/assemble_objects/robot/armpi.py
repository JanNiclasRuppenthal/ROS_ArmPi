from util.assemble_queue import AssembleQueue

class ArmPi():
    def __init__(self, ID, number_of_robots):
        self.__ID = ID
        self.__number_of_robots = number_of_robots
        self.__ready_flag = False
        self.__done_flag = False
        self.__finish_flag = False
        self.__position_with_angle = None
        self.__object_type = None
        self.__object_type_value_next_robot = None
        self.__assemble_queue_flag = False
        self.__number_of_objects = -1
        self.__number_of_objects_next_robot = -1
        self.__assemble_queue = AssembleQueue()

    def get_ID(self):
        return self.__ID
    
    def get_number_of_robots(self):
        return self.__number_of_robots
    
    def set_ready_flag(self, flag):
        self.__ready_flag = flag

    def get_ready_flag(self):
        return self.__ready_flag
    
    def set_done_flag(self, flag):
        self.__done_flag = flag

    def get_done_flag(self):
        return self.__done_flag

    def set_finish_flag(self, flag):
        self.__finish_flag = flag

    def get_finish_flag(self):
        return self.__finish_flag

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
    

    