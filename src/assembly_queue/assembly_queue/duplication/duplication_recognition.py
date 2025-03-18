import time

from rclpy.node import Node

from assembly_queue.duplication.recognition_state import RecognitionState
from assembly_queue.nodes.assembly_queue_publisher import AssemblyQueuePublisher
from object_detection.object_type import ObjectType
from transport_assembly.stationary.robot.armpi import ArmPi


class DuplicationRecognition(Node):
    def __init__ (self, armpi : ArmPi):
        super().__init__('duplication_recognition_node')
        self.__object_id = 0
        self.__armpi = armpi
        self.assembly_queue_publisher = AssemblyQueuePublisher(armpi)
        self.__state = RecognitionState

    def get_object_id(self) -> int:
        return self.__object_id

    def reset_object_id(self):
        self.__object_id = 0

    def recognize_duplicates(self, descending_order=False) -> RecognitionState:
        while True:
            self.assembly_queue_publisher.send_msg()

            while not self.__all_robots_grabbed_a_pipe():

                if self.__armpi.get_finish_flag():
                    self.get_logger().warn("End the recognition of duplicates because one robot send a finish message!")
                    return self.__state.END_SCENARIO

                self.assembly_queue_publisher.send_msg()
                time.sleep(1)

            self.get_logger().info("All available robots grabbed a pipe!")

            assembly_queue = self.__armpi.get_assembly_queue()
            assembly_queue.calculate_assembly_queue(descending_order)
            if not self.__multiple_elements_in_dictionary():
                self.get_logger().info("No duplicates found!")
                break


            self.__armpi.set_assembly_queue_flag(False)
            dict_duplicates = assembly_queue.get_dict_with_duplicates()

            put_down_object = self.__determine_the_need_to_put_down_the_object(dict_duplicates)

            assembly_queue.reset()
            if put_down_object:
                self.get_logger().info("This robot needs to put down the pipe!")
                self.__object_id += 1
                return self.__state.PUT_DOWN_OBJECT


        return self.__state.CONTINUE_TO_ASSEMBLY

    def __all_robots_grabbed_a_pipe(self):
        return self.__armpi.get_assembly_queue().count() == self.__armpi.get_number_of_robots()

    def __multiple_elements_in_dictionary(self):
        return self.__armpi.get_assembly_queue().test_duplicates_in_queue()

    def __determine_the_need_to_put_down_the_object(self, dict_duplicates):
        put_down_object = False
        for obj_type in ObjectType:
            if self.__found_duplicates(dict_duplicates, obj_type):
                continue

            '''
            Skip the first robot because is has the lowest number of objects in its view 
            and the lowest ID
            '''
            dict_duplicates[obj_type.value].pop(0)

            for id in [armpi_id for (armpi_id, num_obj) in dict_duplicates[obj_type.value]]:
                if id == self.__armpi.get_ID():
                    put_down_object = True

        return put_down_object

    def __found_duplicates(self, dict_duplicates, obj_type):
        return len(dict_duplicates[obj_type.value]) == 0