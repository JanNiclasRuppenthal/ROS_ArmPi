from rclpy.node import Node

import time

from movement.mobile.driving.drive import DriveMovement
from movement.mobile.pipes.grab import GrabMovement
from transport_assembly.mobile.robot.armpi import ArmPi


class HandoverStep(Node):
    def __init__(self, armpi : ArmPi, drive_movement : DriveMovement, grab_movement : GrabMovement):
        super().__init__('process_handover_step_node')
        self.__armpi = armpi
        self.__drive_movement = drive_movement
        self.__grab_movement = grab_movement


    def grab_handover_pipe_process(self, id_from_stationary_robot_to_drive):
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


    def __waiting_until_handover_of_pipe_finished(self):
        self.get_logger().info("Waiting until the robot can drive away.")
        while self.__armpi.get_first_robot_hold_pipe():
            time.sleep(0.5)
        self.__armpi.reset_first_robot_hold_pipe()


