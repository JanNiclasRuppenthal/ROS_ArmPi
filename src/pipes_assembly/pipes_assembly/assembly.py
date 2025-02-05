from threading import Thread

from robot.armpi import ArmPi
from robot.publisher.done_publisher import DonePublisher
from robot.publisher.finish_publisher import FinishPublisher
from robot.publisher.position_publisher import PositionPublisher
from robot.subscriber.done_subscriber import DoneSubscriber
from robot.subscriber.finish_subscriber import FinishSubscriber
from robot.subscriber.position_subscriber import PositionSubscriber

from assembly_queue.nodes.assembly_queue_publisher import AssemblyQueuePublisher
from assembly_queue.nodes.assembly_queue_subscriber import AssemblyQueueSubscriber
from object_detection.stationary.pipe_detection import PipeDetection
from common.executor.executor_subscriptions import MultiExecutor
from movement.stationary.pipes.grab import *

object_id = 0

class AssemblyPipes:
    def __init__(self, ID, number_of_robots):
        self.__armpi = ArmPi(ID, number_of_robots)
        init_move()

        self.__create_all_nodes()
        self.executor = MultiExecutor(self.subscriber_nodes_list)
        self.__start_executor()

    def __create_all_nodes(self):
        self.done_publisher = DonePublisher(self.__armpi)
        self.finish_publisher = FinishPublisher(self.__armpi)
        self.pos_publisher = PositionPublisher(self.__armpi)
        self.assembly_queue_publisher = AssemblyQueuePublisher(self.__armpi)
        self.done_subscriber = DoneSubscriber(self.__armpi)
        self.finish_subscriber = FinishSubscriber(self.__armpi)
        self.pos_subscriber = PositionSubscriber(self.__armpi)
        self.assembly_queue_subscriber = AssemblyQueueSubscriber(self.__armpi)

        publisher_nodes_list = [self.done_publisher , self.finish_publisher, self.pos_publisher, self.assembly_queue_publisher]
        self.subscriber_nodes_list = [self.done_subscriber, self.finish_subscriber, self.pos_subscriber, self.assembly_queue_subscriber]
        self.all_nodes_list = publisher_nodes_list + self.subscriber_nodes_list

    def __start_executor(self):
        # start the executor in a thread for spinning all subscriber nodes
        self.thread = Thread(target=self.executor.start_spinning, args=())
        self.thread.start()

    def __end_scenario(self, x, y, angle, rotation_direction, object_type):
        put_down_grabbed_object(x, y, angle, rotation_direction, object_type)
        init_move()
        self.executor.execute_shutdown()

    def process_scenario(self):
        global object_id
        obj_detection = PipeDetection()
        obj_detection.calculate_bottom_parameters()
        x, y = obj_detection.get_position_of_ith_object(object_id)
        angle = obj_detection.get_angle_of_ith_object(object_id)
        rotation_direction = obj_detection.get_rotation_direction_of_ith_object(object_id)
        object_type = obj_detection.get_object_type_of_ith_object(object_id)
        number_of_objects = obj_detection.get_number_of_objects()

        # found no object in the field
        if x == -1 and y == -1:
            self.finish_publisher.send_msg()
            self.executor.execute_shutdown()
            return

        # If one robot had already send a finish message
        if self.__armpi.get_finish_flag():
            self.executor.execute_shutdown()
            return

        self.__armpi.set_object_type(object_type)
        self.__armpi.set_number_of_objects(number_of_objects - 1 - object_id) # decrement the number because we grabbed one object already
        grab_the_object(self.__armpi.get_ID(), x, y, angle, rotation_direction, object_type)
        go_to_waiting_position()

        while True:
            self.assembly_queue_publisher.send_msg()

            while self.__armpi.get_assembly_queue().count() != self.__armpi.get_number_of_robots():

                if self.__armpi.get_finish_flag():
                    self.__end_scenario(x, y, angle, rotation_direction, object_type)
                    return

                self.assembly_queue_publisher.send_msg()
                time.sleep(1)

            self.__armpi.get_assembly_queue().calculate_assembly_queue()
            if not self.__armpi.get_assembly_queue().test_duplicates_in_queue():
                break


            self.__armpi.set_assembly_queue_flag(False)
            dict_duplicates = self.__armpi.get_assembly_queue().get_dict_with_duplicates()

            put_down_object = False
            for obj_type in ObjectType:
                if len(dict_duplicates[obj_type.value]) == 0:
                    continue

                '''
                Skip the first robot because is has the lowest number of objects in its view 
                and the lowest ID
                '''
                dict_duplicates[obj_type.value].pop(0)

                for id in [id for (id, num_obj) in dict_duplicates[obj_type.value]]:
                    if id == self.__armpi.get_ID():
                        put_down_object = True

            self.__armpi.get_assembly_queue().reset()
            if put_down_object:
                put_down_grabbed_object(x, y, angle, rotation_direction, object_type)
                init_move()
                object_id += 1
                return


        if self.__armpi.get_ID() == self.__armpi.get_assembly_queue().first():
            (assemble_x, assemble_y, assemble_z, assemble_angle) = (x, 30, 10, 10)
            go_to_assemble_position(assemble_x, assemble_y, assemble_z, assemble_angle)
            self.pos_publisher.send_msg(float(assemble_x), float(assemble_y), float(assemble_z), assemble_angle)

            self.done_publisher.send_msg()

            while not self.__armpi.get_assembly_queue().empty(): # all robots are done
                time.sleep(0.1)

            put_down_assembled_object(object_type)
            init_move()

        else:
            go_to_upper_position()
            while not self.__armpi.get_ID() == self.__armpi.get_assembly_queue().first():
                time.sleep(0.1)

            self.__armpi.set_done_flag(False)

            (x, y, z, angle) = self.__armpi.get_position_with_angle()

            # set the z value a little bit higher so there is no contact between these two objects
            z += 12
            assemble_objects(x, y, z, angle)
            move_back_to_y_25(x, z, angle)

            # send to the next robot that it can proceed
            self.done_publisher.send_msg()

        self.__armpi.get_assembly_queue().reset()
        object_id = 0


    def start_scenario(self):
        while True:
            self.process_scenario()

            if self.executor.get_shutdown_status():
                for node in self.all_nodes_list:
                    node.destroy_node()

                self.thread.join()
                break