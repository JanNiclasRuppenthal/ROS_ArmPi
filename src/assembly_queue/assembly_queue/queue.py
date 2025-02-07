from object_detection.object_type import ObjectType

class AssemblyQueue:
    def __init__(self):
        self._queue = []
        self._assembly_dict = {}
        self._set_obj_type = set()

    def reset(self):
        self._queue = []
        self._assembly_dict = {}
        self._set_obj_type = set()


    def calculate_assembly_queue(self, descending_order):
        entries = []
        self._set_obj_type = set()
        for id in self._assembly_dict:
            entry = self._assembly_dict[id]
            entries.append((id, entry[0]))
            self._set_obj_type.add(entry[0])


        '''
        Sort after the value of the object type
        
        If the descending_order is False, then we sort the pipes from small to big.
        Otherwise, we sort the pipes from big to small.
        '''
        entries = sorted(entries, key=lambda e: e[1], reverse=descending_order)

        # Fill the queue with the IDs
        self._queue = [entry[0] for entry in entries]

    def add_assembly_request(self, id, object_type_value, number_objects):
        self._assembly_dict[id] = (object_type_value, number_objects)

    def test_duplicates_in_queue(self):
        return len(self._queue) != len(self._set_obj_type)
    
    def get_dict_with_duplicates(self):
        temp_dict = {}
        for obj_type in ObjectType:
            entry_list = []
            for id in self._assembly_dict:
                entry = self._assembly_dict[id]
                if obj_type.value == entry[0]:
                    entry_list.append((id, entry[1]))
            temp_dict[obj_type.value] = entry_list

        
        for obj_type in ObjectType:
            temp_dict[obj_type.value] = sorted(temp_dict[obj_type.value], key=lambda e: (e[1], e[0]))

        return temp_dict

    
    def get_queue(self):
        return self._queue
    
    def remove_ID_from_queue(self, id):
        self._queue.remove(id)
    
    def first(self):
        if len(self._queue) == 0:
            return -1

        return self._queue[0]
    
    def pop(self):
        self._queue.pop(0)

    def empty(self):
        return len(self._queue) == 0
    
    def count(self):
        return len(self._assembly_dict)