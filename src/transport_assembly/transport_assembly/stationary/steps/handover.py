from rclpy.node import Node

import time

from movement.stationary.pipes.handover import HandoverMovement
from transport_assembly.stationary.robot.armpi import ArmPi
from transport_assembly.stationary.robot.publisher.holding_publisher import HoldingPublisher


class Handover(Node):
    def __init__(self, armpi : ArmPi, AK):
        super().__init__('process_handover_node')
        self.__handover_movement = HandoverMovement(AK)
        self.__armpi = armpi
        self.__holding_publisher = HoldingPublisher(self.__armpi)

    def handover_pipe(self):
        self.__go_to_position()

        log_text = "Waiting until I can let go the pipe!"
        self.__wait_until_receiving_notification_for_next_assembly_step(log_text)

        # we wait because we do not want to open the grabber immediately
        time.sleep(2)

        self.__let_the_pipe_go()

        self.get_logger().info("ArmPi Pro can now drive away and my Job is done!")
        self.__holding_publisher.send_msg()
        self.__move_back()

    def __go_to_position(self):
        self.__handover_movement.go_to_handover_position(self.__armpi.get_ID())

    def __let_the_pipe_go(self):
        self.__handover_movement.open_claw()

    def __move_back(self):
        self.__handover_movement.move_back_from_handover_position(self.__armpi.get_ID())
        self.__handover_movement.move_down_from_handover_position()
        self.__handover_movement.init_move()

    def __wait_until_receiving_notification_for_next_assembly_step(self, log_text : str):
        self.get_logger().info(log_text)
        while not self.__armpi.get_permission_to_do_next_assembly_step():
            time.sleep(0.5)

        self.__armpi.set_permission_to_do_next_assembly_step(False)