import copy
import time
from threading import Thread

from rclpy.node import Node

from movement.mobile.control_visual import ControlVisualProcessing
from movement.mobile.pipes.assembly import AssemblyMovement
from movement.mobile.pipes.grab import GrabMovement
from movement.mobile.driving.drive import DriveMovement
from .robot.armpi import ArmPi
from .robot.subscriber.holding_subscriber import HoldingSubscriber
from .robot.subscriber.assembly_order_subscriber import AssemblyOrderSubscriber
from .robot.subscriber.assembly_step_subscriber import AssemblyStepSubscriber
from .robot.subscriber.finish_subscriber import FinishSubscriber
from .robot.publisher.assembly_queue_notify_publisher import NotifyReceivingAssemblyQueuePublisher
from .robot.publisher.assembly_step_publisher import AssemblyStepPublisher

from common.executor.executor_subscriptions import MultiExecutor

class Transporter(Node):
    def __init__(self, number_of_stationary_robots, allow_buzzer: bool):
        super().__init__("transporter")
        self.__id_from_last_stationary_robot = -1
        self.__armpi = ArmPi(number_of_stationary_robots)

        self.__control_visual_processing = ControlVisualProcessing()

        self.__assembly_movement = AssemblyMovement()
        self.__grab_movement = GrabMovement(self.__control_visual_processing)
        self.__drive_movement = DriveMovement(self.__armpi, self.__control_visual_processing, allow_buzzer)

        self.__create_nodes()
        self.__start_executor()

        self.__grab_movement.init_move()
        self.__control_visual_processing.enter_visual_processing()


    def __create_nodes(self):
        self.__list_subscriber_nodes = [
            self.__drive_movement,
            self.__grab_movement.get_tracking_pipe_node(),
            self.__assembly_movement,
            HoldingSubscriber(self.__armpi),
            AssemblyOrderSubscriber(self.__armpi),
            AssemblyStepSubscriber(self.__armpi),
            FinishSubscriber(self.__armpi)
        ]

        self.__notify_receiving_assembly_queue_publisher = NotifyReceivingAssemblyQueuePublisher(self.__armpi)
        self.__assembly_step_publisher = AssemblyStepPublisher(self.__armpi)

        list_publisher_nodes = [
            self.__notify_receiving_assembly_queue_publisher,
            self.__assembly_step_publisher
        ]

        self.__list_all_nodes = list_publisher_nodes + self.__list_subscriber_nodes

    def __start_executor(self):
        self.__executor = MultiExecutor(self.__list_subscriber_nodes)
        self.__thread = Thread(target=self.__executor.start_spinning, args=())
        self.__thread.start()

    def __end_scenario(self):
        self.__control_visual_processing.exit_visual_processing()

        if self.__id_from_last_stationary_robot != -1:
            self.get_logger().info("I can park now!")
            self.__grab_movement.init_move()
            self.__drive_movement.park()

        self.__executor.execute_shutdown()

    def __transport_pipe(self):
        self.get_logger().info("Waiting for an assembly order of one stationary robot!")
        while not self.__received_assembly_order():
            if self.__armpi.get_finish_flag():
                self.__end_scenario()
                return

            time.sleep(0.5)

        self.get_logger().info("I received a list with all the order of the stationary robots!")
        self.__armpi.set_assembly_order_status(False)
        self.__drive_movement.set_id_list_for_following_lines(copy.deepcopy(self.__armpi.get_IDList()))

        self.__handover_process()

        while not self.__armpi.is_empty_IDList():
            self.__assembly_process()

        self.__drive_movement.init_move()
        self.__drive_movement.start_to_drive()
        self.__waiting_until_next_stationary_robot_is_reached()

    def __handover_process(self):
        id_from_stationary_robot_to_drive = self.__armpi.pop_IDList()
        self.__notify_receiving_assembly_queue_publisher.send_msg()

        if id_from_stationary_robot_to_drive == self.__id_from_last_stationary_robot:
            self.get_logger().info("Rotate 180 degrees!")
            self.__drive_movement.rotate_180_deg()
        if self.__id_from_last_stationary_robot == -1:
            self.__drive_movement.init_move()

        self.__drive_movement.start_to_drive()

        self.get_logger().info(f"Driving to the next robot (ID = {id_from_stationary_robot_to_drive})!")
        self.__waiting_until_next_stationary_robot_is_reached()

        self.__grab_movement.set_grab_pipe_from_robot_id(id_from_stationary_robot_to_drive)
        self.__grab_movement.init_move()

        self.__drive_movement.drive_forward(1)

        self.__grab_movement.track_pipe()

        self.__waiting_until_handover_of_pipe_finished()
        self.get_logger().info("Drive backwards and rotate based on the position of the stationary robot!")
        self.__drive_movement.drive_away_from_stationary_robot(id_from_stationary_robot_to_drive)

    def __received_assembly_order(self):
        return self.__armpi.get_assembly_order_status()

    def __waiting_until_handover_of_pipe_finished(self):
        self.get_logger().info("Waiting until I can drive away.")
        while self.__armpi.get_first_robot_hold_pipe():
            time.sleep(0.5)
        self.__armpi.reset_first_robot_hold_pipe()

    def __assembly_process(self):
        self.__drive_movement.init_move()
        self.__drive_movement.start_to_drive()
        id_from_stationary_robot_to_assembly = self.__armpi.pop_IDList()

        self.get_logger().info(f"Driving to the next robot (ID = {id_from_stationary_robot_to_assembly})!")
        self.__waiting_until_next_stationary_robot_is_reached()
        self.get_logger().info("Reached the next stationary robot!")

        self.__assembly_movement.init_move()
        self.__drive_movement.drive_forward(1.3)

        self.__notify_next_robot_for_next_assembly_step(id_from_stationary_robot_to_assembly)
        self.__waiting_for_receiving_assembly_position()

        self.get_logger().info("Moving arm up!")
        self.__assembly_movement.move_arm_up()

        self.__notify_next_robot_for_next_assembly_step(id_from_stationary_robot_to_assembly)
        self.__waiting_for_permission_to_do_next_assembly_step()

        self.get_logger().info("Moving arm down!")
        self.__assembly_movement.move_arm_down()

        self.get_logger().info("Opening claw!")
        self.__assembly_movement.open_claw()
        self.__grab_movement.init_move()

        self.__notify_next_robot_for_next_assembly_step(id_from_stationary_robot_to_assembly)
        self.__drive_movement.drive_away_from_stationary_robot(id_from_stationary_robot_to_assembly)

        self.__id_from_last_stationary_robot = id_from_stationary_robot_to_assembly

    def __waiting_for_receiving_assembly_position(self):
        while not self.__assembly_movement.received_assembly_position():
            time.sleep(0.5)
        self.get_logger().info("Got position to move my arm to the assembly position!")

    def __waiting_for_permission_to_do_next_assembly_step(self):
        self.get_logger().info("Waiting until stationary robot moved its arm to (0, 20)!")
        while not self.__armpi.get_permission_to_do_next_assembly_step():
            time.sleep(0.5)
        self.__armpi.set_permission_to_do_next_assembly_step(False)

    def __notify_next_robot_for_next_assembly_step(self, next_id):
        self.__assembly_step_publisher.send_msg(next_id)

    def __waiting_until_next_stationary_robot_is_reached(self):
        while not self.__drive_movement.reached_the_next_stationary_robot():
            time.sleep(0.5)

    def start_scenario(self):
        while True:
            self.__transport_pipe()

            if self.__executor.get_shutdown_status():
                for node in self.__list_all_nodes:
                    node.destroy_node()

                self.__thread.join()
                break

