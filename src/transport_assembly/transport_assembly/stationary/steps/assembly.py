from rclpy.node import Node

import time

from movement.stationary.pipes.assembly import AssemblyMovement
from movement.stationary.pipes.put_down import PutDownMovement
from object_detection.detected_object import DetectedObject
from object_detection.stationary.yellow_grabber_detection import GrabberDetection
from transport_assembly.stationary.robot.armpi import ArmPi
from transport_assembly.stationary.robot.publisher.assembly_position_publisher import AssemblyPositionPublisher
from transport_assembly.stationary.robot.publisher.assembly_step_publisher import AssemblyStepPublisher


class AssemblyStep(Node):
    def __init__(self, armpi : ArmPi, AK):
        super().__init__('process_assembly_node')
        self.__assembly_movement = AssemblyMovement(AK)
        self.__grabber_detection = GrabberDetection()
        self.__armpi = armpi
        self.__assembly_position_publisher = AssemblyPositionPublisher(self.__armpi)
        self.__assembly_step_publisher = AssemblyStepPublisher(self.__armpi)


    def assembling_pipes(self):
        self.get_logger().info("Waiting until the driving robot received the order for the assembly")
        while not self.__armpi.did_transporter_received_list():
            time.sleep(0.5)

        self.__armpi.set_transporter_received_list(False)
        self.__rotate_arm()

        log_text = "Waiting until the driving robot reached my view!"
        self.__wait_until_receiving_notification_for_next_assembly_step(log_text)

        x, y = self.__get_position_of_grabber()
        self.__assembly_position_publisher.send_msg(x, y)

        log_text = "Waiting until the driving robot moved its arm away!"
        self.__wait_until_receiving_notification_for_next_assembly_step(log_text)
        self.__initiate_moving_to_assembly_position()

        # notify ArmPi Pro
        self.__assembly_step_publisher.send_msg()

        log_text = "Waiting until the driving robot opened its claw and drove away!"
        self.__wait_until_receiving_notification_for_next_assembly_step(log_text)

    def __wait_until_receiving_notification_for_next_assembly_step(self, log_text : str):
        self.get_logger().info(log_text)
        while not self.__armpi.get_permission_to_do_next_assembly_step():
            time.sleep(0.5)

        self.__armpi.set_permission_to_do_next_assembly_step(False)

    def __rotate_arm(self):
        self.__assembly_movement.rotate_away_from_camera()

    def __get_position_of_grabber(self) -> tuple[float, float]:
        return self.__grabber_detection.calculate_middle_between_grabber()

    def __initiate_moving_to_assembly_position(self):
        self.__assembly_movement.move_to_origin(19)

    def put_the_assembled_pipe_down(self, movement : PutDownMovement, detected_object : DetectedObject):
        movement.put_down_assembled_object(detected_object.get_object_type())
        movement.init_move()