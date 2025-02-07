from threading import Thread
import time

from rclpy.node import Node

from assembly_queue.duplication.duplication_recognition import DuplicationRecognition
from assembly_queue.duplication.recognition_state import RecognitionState
from movement.stationary.pipes.assembly import AssemblyMovement
from movement.stationary.pipes.grab import GrabMovement
from movement.stationary.pipes.put_down import PutDownMovement
from object_detection.detected_object import DetectedObject
from robot.armpi import ArmPi
from robot.publisher.done_publisher import DonePublisher
from robot.publisher.finish_publisher import FinishPublisher
from robot.publisher.position_publisher import PositionPublisher
from robot.subscriber.done_subscriber import DoneSubscriber
from robot.subscriber.finish_subscriber import FinishSubscriber
from robot.subscriber.position_subscriber import PositionSubscriber

from assembly_queue.nodes.assembly_queue_subscriber import AssemblyQueueSubscriber
from object_detection.stationary.pipe_detection import PipeDetection
from common.executor.executor_subscriptions import MultiExecutor

class AssemblyPipes(Node):
    def __init__(self, ID, number_of_robots):
        super().__init__('assembly_pipes_node')
        self.__armpi = ArmPi(ID, number_of_robots)
        self.__grab_movement = GrabMovement()
        self.__put_down_movement = PutDownMovement()
        self.__assembly_movement = AssemblyMovement()

        self.__grab_movement.init_move()

        self.__create_all_nodes()

        self.__pipe_detection = PipeDetection()
        self.__duplication_recognition = DuplicationRecognition(self.__armpi)


        self.__executor = MultiExecutor(self.subscriber_nodes_list)
        self.__start_executor()

    def __create_all_nodes(self):
        self.done_publisher = DonePublisher(self.__armpi)
        self.finish_publisher = FinishPublisher(self.__armpi)
        self.pos_publisher = PositionPublisher(self.__armpi)
        self.done_subscriber = DoneSubscriber(self.__armpi)
        self.finish_subscriber = FinishSubscriber(self.__armpi)
        self.pos_subscriber = PositionSubscriber(self.__armpi)
        self.assembly_queue_subscriber = AssemblyQueueSubscriber(self.__armpi)

        publisher_nodes_list = [self.done_publisher , self.finish_publisher, self.pos_publisher]
        self.subscriber_nodes_list = [self.done_subscriber, self.finish_subscriber, self.pos_subscriber, self.assembly_queue_subscriber]
        self.all_nodes_list = publisher_nodes_list + self.subscriber_nodes_list

    def __start_executor(self):
        # start the executor in a thread for spinning all subscriber nodes
        self.thread = Thread(target=self.__executor.start_spinning, args=())
        self.thread.start()
        self.get_logger().info("Started MultiExecutor thread for all subscribers!")

    def __end_scenario(self, detected_object : DetectedObject):
        self.__put_down_movement.put_down_grabbed_object(detected_object)
        self.__put_down_movement.init_move()
        self.__executor.execute_shutdown()

    def __assembly_pipes(self):
        self.__pipe_detection.calculate_bottom_parameters()
        number_of_objects = self.__pipe_detection.get_number_of_objects()
        object_id = self.__duplication_recognition.get_object_id()

        detected_object = self.__pipe_detection.get_ith_detected_object(object_id)

        # found no object in the field
        if detected_object.are_coordinates_valid():
            self.finish_publisher.send_msg()
            self.__executor.execute_shutdown()
            return

        # If one robot had already finished, send a finish message
        if self.__armpi.get_finish_flag():
            self.__executor.execute_shutdown()
            return

        self.__armpi.set_object_type(detected_object.get_object_type())
        self.__armpi.set_number_of_objects(number_of_objects - 1 - object_id) # decrement the number because we grabbed one object already
        self.__grab_movement.grab_the_object(self.__armpi.get_ID(), detected_object)
        self.__grab_movement.go_to_waiting_position()

        recognition_state = self.__duplication_recognition.recognize_duplicates()


        if recognition_state == RecognitionState.END_SCENARIO:
            self.__end_scenario(detected_object)
            return

        if recognition_state == RecognitionState.PUT_DOWN_OBJECT:
            self.__put_down_movement.put_down_grabbed_object(detected_object)
            self.__put_down_movement.init_move()
            return


        if self.__armpi.get_ID() == self.__armpi.get_assembly_queue().first():
            self.__send_position_with_angle_for_assembly(detected_object)

            self.done_publisher.send_msg()

            self.__wait_until_all_robots_are_done()
            self.get_logger().info("All robots finished their assembly!")

            self.__put_down_movement.put_down_assembled_object(detected_object.get_object_type())
            self.__put_down_movement.init_move()
            self.get_logger().info("Finished the assembly cycle!")

        else:
            self.__assembly_movement.go_to_upper_position()
            self.__wait_until_robot_is_allowed_to_assembly()

            self.__armpi.set_done_flag(False)

            (x, y, z, angle) = self.__armpi.get_position_with_angle()

            self.__movement_for_assembly(angle, x, y, z)

            # send to the next robot that it can proceed
            self.done_publisher.send_msg()

        self.__armpi.get_assembly_queue().reset()
        self.__duplication_recognition.reset_object_id()

    def __send_position_with_angle_for_assembly(self, detected_object):
        (assembly_x, assembly_y, assembly_z, assembly_angle) = (detected_object.get_x(), 30, 10, 10)
        self.__assembly_movement.go_to_assembly_position(assembly_x, assembly_y, assembly_z, assembly_angle)
        self.pos_publisher.send_msg(float(assembly_x), float(assembly_y), float(assembly_z), assembly_angle)

    def __wait_until_all_robots_are_done(self):
        while not self.__armpi.get_assembly_queue().empty():  # all robots are done
            time.sleep(0.1)

    def __wait_until_robot_is_allowed_to_assembly(self):
        while not self.__armpi.get_ID() == self.__armpi.get_assembly_queue().first():
            time.sleep(0.1)

    def __movement_for_assembly(self, angle, x, y, z):
        # set the z value a little bit higher so there is no contact between these two objects
        z += 12
        self.__assembly_movement.assembly_objects(x, y, z, angle)
        self.__assembly_movement.move_back_to_y_25(x, z, angle)

    def start_scenario(self):
        while True:
            self.__assembly_pipes()

            if self.__executor.get_shutdown_status():
                for node in self.all_nodes_list:
                    node.destroy_node()

                self.thread.join()
                break

        self.get_logger().info("The program terminated!")