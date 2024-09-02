from util.object_type import ObjectType

class AssembleQueue():
    def __init__(self):
        self.__queue = []
        self.__id_object_dict = {}


    def add_id_object_type_value(self, id, object_type_value):
        self.__id_object_dict[id] = object_type_value


    def calculate_assemble_queue(self):
        entrys = []
        for id in self.__id_object_dict:
            entrys.append((id, self.__id_object_dict[id]))

        entrys = sorted(entrys, key=lambda e: e[1])

        self.__queue = [entry[0] for entry in entrys]

    def test_duplicates_in_queue(self):
        set_of_queue = set(self.__queue)
        return len(self.__queue) != len(set_of_queue)
    
    def get_queue(self):
        return self.__queue
    
    def first(self):
        if len(self.__queue) == 0:
            return -1

        return self.__queue[0]
    
    def pop(self):
        self.__queue.pop(0)

    def empty(self):
        return len(self.__queue) == 0
    
    def clear_dict(self):
        self.__id_object_dict.clear()