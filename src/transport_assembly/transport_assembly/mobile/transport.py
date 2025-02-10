import copy
import time
from threading import Thread

from rclpy.node import Node

from std_srvs.srv import Trigger
from armpi_pro_service_client.client import call_service

from movement.mobile.pipes.grab import set_master_node_grabbing, grab_init_move, get_grabbing_node, detect_pipe, set_grab_robot_id
from movement.mobile.pipes.assembly import *
from movement.mobile.drive import set_allow_buzzer, set_armpi, set_master_node_driving, drive_init_move, start_to_drive, get_driving_node, reached_the_next_stationary_robot, drive_forward, drive_backward, rotate_90_deg_right, rotate_90_deg_left, park, set_id_list_for_driving, drive_away_from_robot, rotate_180_deg
from .robot.armpi import ArmPi
from .robot.subscriber.holding_subscriber import HoldingSubscriber
from .robot.subscriber.assembly_order_subscriber import AssemblyOrderSubscriber
from .robot.subscriber.assembly_step_subscriber import AssemblyStepSubscriber
from .robot.subscriber.finish_subscriber import FinishSubscriber
from .robot.publisher.assembly_queue_notify_publisher import NotifyPublisher

from common.executor.executor_subscriptions import MultiExecutor

class Transporter(Node):
    def __init__(self, number_of_stationary_robots, allow_buzzer: bool):
        super().__init__("transporter")
        self.__id_from_last_stationary_robot = -1
        self.__armpi = ArmPi(number_of_stationary_robots)

        set_allow_buzzer(allow_buzzer)
        set_armpi(self.__armpi)

        self.__create_nodes()

        self.__start_executor()

        grab_init_move()

        set_master_node_driving(self)
        set_master_node_grabbing(self)

        call_service(self, Trigger, '/visual_processing/enter', Trigger.Request())

    def __create_nodes(self):
        self.__list_subscriber_nodes = [
            get_driving_node(),
            get_grabbing_node(),
            get_assembly_node(),
            HoldingSubscriber(self.__armpi),
            AssemblyOrderSubscriber(self.__armpi),
            AssemblyStepSubscriber(self.__armpi),
            FinishSubscriber(self.__armpi)
        ]
        self.__notify_publisher = NotifyPublisher(self.__armpi)
        self.__list_all_nodes = [self.__notify_publisher] + self.__list_subscriber_nodes

    def __start_executor(self):
        self.__executor = MultiExecutor(self.__list_subscriber_nodes)
        self.__thread = Thread(target=self.__executor.start_spinning, args=())
        self.__thread.start()

    def __end_scenario(self):
        self.__notify_publisher.send_msg()
        self.get_logger().warn("Exit the visual_processing!")
        call_service(self, Trigger, '/visual_processing/exit', Trigger.Request())

        if self.__id_from_last_stationary_robot != -1:
            self.get_logger().info("I can park now!")
            grab_init_move()
            park()

        self.__executor.execute_shutdown()

    def __transport_pipe(self):
        while not self.__received_assembly_order():
            if self.__armpi.get_finish_flag():
                self.__end_scenario()
                return

            time.sleep(0.5)

        self.get_logger().info("I received a list with all the order of the stationary robots!")
        self.__armpi.set_assembly_order_status(False)
        set_id_list_for_driving(copy.deepcopy(self.__armpi.get_IDList()))

        id_from_stationary_robot_to_drive = self.__armpi.pop_IDList()
        self.__notify_publisher.send_msg()

        if id_from_stationary_robot_to_drive == self.__id_from_last_stationary_robot:
            self.get_logger().info("Rotate 180 degrees!")
            rotate_180_deg()

        if self.__id_from_last_stationary_robot == -1:
            drive_init_move()

        start_to_drive()

        self.get_logger().info(f"Driving to the next robot (ID = {id_from_stationary_robot_to_drive})!")
        self.__waiting_until_next_stationary_robot_is_reached()

        set_grab_robot_id(id_from_stationary_robot_to_drive)

        grab_init_move()
        drive_forward(1)

        detect_pipe()

        self.__waiting_until_handover_of_pipe_finished()

        self.get_logger().info("Drive backwards and rotate!")
        drive_away_from_robot(id_from_stationary_robot_to_drive)

        while not self.__armpi.is_empty_IDList():
            self.__assembly_process()

        drive_init_move()
        start_to_drive()
        self.__waiting_until_next_stationary_robot_is_reached()

    def __received_assembly_order(self):
        return self.__armpi.get_assembly_order_status()

    def __waiting_until_handover_of_pipe_finished(self):
        self.get_logger().info("Waiting until I can drive away.")
        while self.__armpi.get_first_robot_hold_pipe():
            time.sleep(0.5)
        self.__armpi.reset_first_robot_hold_pipe()

    def __assembly_process(self):
        drive_init_move()
        start_to_drive()
        id_from_stationary_robot_to_assembly = self.__armpi.pop_IDList()

        self.get_logger().info(f"Driving to the next robot (ID = {id_from_stationary_robot_to_assembly})!")
        self.__waiting_until_next_stationary_robot_is_reached()
        self.get_logger().info("Reached the next stationary robot!")

        assembly_init_move()
        drive_forward(1.3)

        self.__notify_next_robot_for_next_assembly_step(id_from_stationary_robot_to_assembly)
        self.__waiting_for_receiving_assembly_position()

        self.get_logger().info("Moving arm up!")
        move_arm_up()

        self.__notify_next_robot_for_next_assembly_step(id_from_stationary_robot_to_assembly)
        self.__waiting_for_permission_to_do_next_assembly_step()

        self.get_logger().info("Moving arm down!")
        move_arm_down()

        self.get_logger().info("Opening claw!")
        open_claw()
        grab_init_move()

        self.__notify_next_robot_for_next_assembly_step(id_from_stationary_robot_to_assembly)
        drive_away_from_robot(id_from_stationary_robot_to_assembly)

        self.__id_from_last_stationary_robot = id_from_stationary_robot_to_assembly

    def __waiting_for_receiving_assembly_position(self):
        while not got_position():
            time.sleep(0.5)
        self.get_logger().info("Got position to move my arm to the assembly position!")

    def __waiting_for_permission_to_do_next_assembly_step(self):
        self.get_logger().info("Waiting until stationary robot moved its arm to (0, 20)!")
        while not self.__armpi.get_permission_to_do_next_assembly_step():
            time.sleep(0.5)
        self.__armpi.set_permission_to_do_next_assembly_step(False)

    def __notify_next_robot_for_next_assembly_step(self, next_id):
        self.get_logger().info(f"Notify the stationary robot (with ID = {next_id}) to initiate the next assembly step!")
        notify_stationary_robot_for_the_next_assembly_step(next_id)

    def __waiting_until_next_stationary_robot_is_reached(self):
        while not reached_the_next_stationary_robot():
            time.sleep(0.5)

    def start_scenario(self):
        while True:
            self.__transport_pipe()

            if self.__executor.get_shutdown_status():
                for node in self.__list_all_nodes:
                    node.destroy_node()

                self.__thread.join()
                break

