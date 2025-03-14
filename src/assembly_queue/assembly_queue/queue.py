from object_detection.object_type import ObjectType

class AssemblyQueue:
    def __init__(self):
        self._queue_of_ids = []
        self._assembly_dict = {}
        self._set_obj_type_values = set()

    def reset(self):
        self._queue_of_ids = []
        self._assembly_dict = {}
        self._set_obj_type_values = set()


    def calculate_assembly_queue(self, descending_order):
        entries_of_id_and_object_type_value = []
        self._set_obj_type_values = set()
        for id in self._assembly_dict:
            (object_type_value, number_of_next_grabable_objects) = self._assembly_dict[id]
            entries_of_id_and_object_type_value.append((id, object_type_value))
            self._set_obj_type_values.add(object_type_value)


        '''
        Sort after the value of the object type
        
        If the descending_order is False, then we sort the pipes from small to big.
        Otherwise, we sort the pipes from big to small.
        '''
        entries_of_id_and_object_type_value = (
            sorted(entries_of_id_and_object_type_value, key=lambda e: e[1], reverse=descending_order))

        # Fill the queue with the IDs
        self._queue_of_ids = [entry[0] for entry in entries_of_id_and_object_type_value]

    def add_assembly_request(self, id, object_type_value, number_of_next_grabable_objects):
        self._assembly_dict[id] = (object_type_value, number_of_next_grabable_objects)

    def test_duplicates_in_queue(self):
        return len(self._queue_of_ids) != len(self._set_obj_type_values)
    
    def get_dict_with_duplicates(self):
        temp_dict = {}
        for obj_type in ObjectType:
            temp_list_of_ids_and_number_of_grabable_objects = []
            for id in self._assembly_dict:
                (object_type_value, number_of_next_grabable_objects) = self._assembly_dict[id]
                if obj_type.value == object_type_value:
                    temp_list_of_ids_and_number_of_grabable_objects.append((id, number_of_next_grabable_objects))
            temp_dict[obj_type.value] = temp_list_of_ids_and_number_of_grabable_objects

        
        for obj_type in ObjectType:
            temp_dict[obj_type.value] = sorted(temp_dict[obj_type.value], key=lambda e: (e[1], e[0]))

        return temp_dict

    
    def get_queue_of_ids(self):
        return self._queue_of_ids
    
    def remove_ID_from_queue(self, id):
        self._queue_of_ids.remove(id)
    
    def first(self):
        if len(self._queue_of_ids) == 0:
            return -1

        return self._queue_of_ids[0]
    
    def pop(self):
        self._queue_of_ids.pop(0)

    def empty(self):
        return len(self._queue_of_ids) == 0
    
    def count(self):
        return len(self._assembly_dict)