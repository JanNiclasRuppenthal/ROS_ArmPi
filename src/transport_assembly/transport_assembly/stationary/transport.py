from threading import Thread
import time

from rclpy.node import Node

from ArmIK.ArmMoveIK import *

from assembly_queue.duplication.duplication_recognition import DuplicationRecognition
from assembly_queue.duplication.recognition_state import RecognitionState
from assembly_queue.nodes.assembly_queue_subscriber import AssemblyQueueSubscriber
from common.executor.executor_subscriptions import MultiExecutor
from movement.stationary.pipes.grab import GrabMovement
from movement.stationary.pipes.put_down import PutDownMovement
from object_detection.detected_object import DetectedObject
from object_detection.stationary.pipe_detection import PipeDetection
from .steps.assembly import Assembler
from .steps.handover import Handover
from .robot.armpi import ArmPi
from .robot.publisher.finish_publisher import FinishPublisher
from .robot.publisher.assembly_order_publisher import AssemblyOrderPublisher
from .robot.subscriber.assembly_queue_notify_subscriber import NotifySubscriber
from .robot.subscriber.assembly_step_subscriber import AssemblyStepSubscriber
from .robot.subscriber.finish_subscriber import FinishSubscriber
from .robot.subscriber.grabbed_subscriber import GrabbedSubscriber


class TransportAssembly(Node):
    def __init__(self, ID, number_of_stationary_robots):
        super().__init__('transport_assembly_pipes_node')
        self.__AK = ArmIK()
        self.__armpi = ArmPi(ID, number_of_stationary_robots)

        self.__grab_movement = GrabMovement(self.__AK)
        self.__put_down_movement = PutDownMovement(self.__AK)
        self.__grab_movement.init_move()

        self.__create_all_nodes()

        self.__pipe_detection = PipeDetection()
        self.__duplication_recognition = DuplicationRecognition(self.__armpi)

        self.__executor = MultiExecutor(self.__subscriber_nodes_list)
        self.__start_executor()


    def __create_all_nodes(self):
        self.__assembly_order_publisher = AssemblyOrderPublisher(self.__armpi)
        self.__finish_publisher = FinishPublisher(self.__armpi)

        self.__grabbed_subscriber = GrabbedSubscriber(self.__armpi)
        self.__notify_subscriber = NotifySubscriber(self.__armpi)
        self.__assembly_queue_subscriber = AssemblyQueueSubscriber(self.__armpi)
        self.__assembly_step_subscriber = AssemblyStepSubscriber(self.__armpi)
        self.__finish_subscriber = FinishSubscriber(self.__armpi)

        publisher_nodes_list = [
            self.__assembly_order_publisher,
            self.__finish_publisher
        ]

        self.__subscriber_nodes_list = [
            self.__grabbed_subscriber,
            self.__notify_subscriber,
            self.__assembly_queue_subscriber,
            self.__assembly_step_subscriber,
            self.__finish_subscriber
        ]

        self.__all_nodes_list = publisher_nodes_list + self.__subscriber_nodes_list

    def __start_executor(self):
        # start the executor in a thread for spinning all subscriber nodes
        self.thread = Thread(target=self.__executor.start_spinning, args=())
        self.thread.start()
        self.get_logger().info("Started MultiExecutor thread for all subscribers!")

    def __end_scenario(self, detected_object : DetectedObject):
        self.__put_down_movement.put_down_grabbed_object(detected_object)
        self.__put_down_movement.init_move()
        self.__executor.execute_shutdown()

    def __transport_assembly_pipes(self):
        if self.__one_robot_already_finished_scenario():
            self.__executor.execute_shutdown()
            return

        self.__pipe_detection.calculate_middle_parameters()
        number_of_objects = self.__pipe_detection.get_number_of_objects()
        object_id = self.__duplication_recognition.get_object_id()

        detected_object = self.__pipe_detection.get_ith_detected_object(object_id)
        if detected_object.are_coordinates_valid():
            self.__send_finish_messages()
            self.__executor.execute_shutdown()
            return

        if self.__one_robot_already_finished_scenario():
            self.__executor.execute_shutdown()
            return

        self.__armpi.set_object_type(detected_object.get_object_type())
        # decrement the number because we grabbed one object already
        self.__armpi.set_number_of_objects(number_of_objects - 1 - object_id)

        self.__grab_movement.grab_the_object(self.__armpi.get_ID(), detected_object)
        self.__grab_movement.go_to_waiting_position()

        recognition_state = self.__duplication_recognition.recognize_duplicates(True)

        if recognition_state == RecognitionState.END_SCENARIO:
            self.__end_scenario(detected_object)
            return

        if recognition_state == RecognitionState.PUT_DOWN_OBJECT:
            self.__put_down_movement.put_down_grabbed_object(detected_object)
            self.__put_down_movement.init_move()
            return

        if self.__robot_need_to_handover_pipe():
            #self.__initiate_sending_assembly_order()
            handover = Handover(self.__armpi, self.__AK)
            handover.handover_pipe()
        else:
            assembler = Assembler(self.__armpi, self.__AK)
            assembler.assembling_pipes()
            assembler.put_the_assembled_pipe_down(self.__put_down_movement, detected_object)

        self.__armpi.get_assembly_queue().reset()
        self.__duplication_recognition.reset_object_id()

    def __one_robot_already_finished_scenario(self):
        return self.__armpi.get_finish_flag()

    def __send_finish_messages(self):
        self.__finish_publisher.send_msg()
        while not self.__armpi.did_transporter_received_list():
            self.__finish_publisher.send_msg()
            time.sleep(0.5)

    def __robot_need_to_handover_pipe(self):
        return self.__armpi.get_ID() == self.__armpi.get_assembly_queue().first()

    def __initiate_sending_assembly_order(self):
        order_queue = self.__armpi.get_assembly_queue().get_queue()

        self.get_logger().info("Waiting until the driving robot received the order for the assembly")
        while not self.__armpi.did_transporter_received_list():
            self.__assembly_order_publisher.send_msg(order_queue)
            time.sleep(0.5)

        self.__armpi.set_transporter_received_list(False)

    def start_scenario(self):
        while True:
            self.__transport_assembly_pipes()

            if self.__executor.get_shutdown_status():
                for node in self.__all_nodes_list:
                    node.destroy_node()

                self.thread.join()
                break
