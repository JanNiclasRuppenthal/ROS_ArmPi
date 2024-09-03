from util.object_type import ObjectType

class AssembleQueue():
    def __init__(self):
        self.__queue = []
        self.__assemble_dict = {}
        self.__set_obj_type = set()

    def reset(self):
        self.__queue = []
        self.__assemble_dict = {}
        self.__set_obj_type = set()


    def add_assemble_request(self, id, object_type_value, number_objects):
        self.__assemble_dict[id] = (object_type_value, number_objects)


    def calculate_assemble_queue(self):
        entrys = []
        self.__set_obj_type = set()
        for id in self.__assemble_dict:
            entry = self.__assemble_dict[id]
            entrys.append((id, entry[0]))
            self.__set_obj_type.add(entry[0])

        # Sort after the value of the object type
        entrys = sorted(entrys, key=lambda e: e[1])

        # Fill the queue with the IDs 
        self.__queue = [entry[0] for entry in entrys]

    def test_duplicates_in_queue(self):
        return len(self.__queue) != len(self.__set_obj_type)
    
    def get_dict_with_duplicates(self):
        temp_dict = {}
        for obj_type in ObjectType:
            entry_list = []
            for id in self.__assemble_dict:
                entry = self.__assemble_dict[id]
                if obj_type.value == entry[0]:
                    entry_list.append((id, entry[1]))
            temp_dict[obj_type.value] = entry_list

        
        for obj_type in ObjectType:
            temp_dict[obj_type.value] = sorted(temp_dict[obj_type.value], key=lambda e: (e[1], e[0]))

        return temp_dict
    
    def get_queue(self):
        return self.__queue
    
    def remove_ID_from_queue(self, id):
        print(str(self.__queue))
        self.__queue.remove(id)
        print(str(self.__queue))
    
    def first(self):
        if len(self.__queue) == 0:
            return -1

        return self.__queue[0]
    
    def pop(self):
        self.__queue.pop(0)

    def empty(self):
        return len(self.__queue) == 0
    
    def count(self):
        return len(self.__assemble_dict)