from assembly_queue.queue import AssemblyQueue
from object_detection.object_type import ObjectType

class AssemblyQueueStates:
    def __init__(self):
        self.__object_type = None
        self.__object_type_value_next_robot = None
        self.__assembly_queue_flag = False
        self.__number_of_objects = -1
        self.__number_of_objects_next_robot = -1
        self.__assembly_queue = AssemblyQueue()

    def set_object_type(self, obj_type):
        self.__object_type = obj_type

    def get_object_type(self) -> ObjectType:
        return self.__object_type

    def set_assembly_queue_flag(self, flag):
        self.__assembly_queue_flag = flag

    def get_assembly_queue_flag(self) -> bool:
        return self.__assembly_queue_flag

    def get_object_type_value_next_robot(self):
        return self.__object_type_value_next_robot

    def set_object_type_value_next_robot(self, obj_type):
        self.__object_type_value_next_robot = obj_type

    def get_number_of_objects(self) -> int:
        return self.__number_of_objects

    def set_number_of_objects(self, number):
        self.__number_of_objects = number

    def get_number_of_objects_next_robot(self) -> int:
        return self.__number_of_objects_next_robot

    def set_number_of_objects_next_robot(self, number):
        self.__number_of_objects_next_robot = number

    def get_assembly_queue(self) -> AssemblyQueue:
        return self.__assembly_queue