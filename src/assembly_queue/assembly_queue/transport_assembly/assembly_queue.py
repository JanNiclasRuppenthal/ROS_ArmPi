from assembly_queue.Aqueue import AQueue

class AssemblyQueue(AQueue):
    def calculate_assembly_queue(self):
        entrys = []
        self._set_obj_type = set()
        for id in self._assemble_dict:
            entry = self._assemble_dict[id]
            entrys.append((id, entry[0]))
            self._set_obj_type.add(entry[0])

        # Sort after the value of the object type
        entrys = sorted(entrys, key=lambda e: e[1], reverse=True)

        # Fill the queue with the IDs 
        self._queue = [entry[0] for entry in entrys]