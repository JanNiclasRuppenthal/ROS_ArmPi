from rclpy.node import Node

import time

from transport_assembly.mobile.transport import Transporter

class HandoverStep(Node):
    def __init__(self, transporter : Transporter):
        super().__init__('process_handover_step_node')
        self.__transporter = transporter
        self.__armpi = transporter.get_armpi()
        self.__drive_movement = transporter.get_drive_movement()
        self.__grab_movement = transporter.get_grab_movement()


    def grab_handover_pipe_process(self, id_from_stationary_robot_to_drive):
        self.__drive_movement.start_to_drive()
        self.get_logger().info(f"Driving to the next robot (ID = {id_from_stationary_robot_to_drive})!")

        self.__transporter.waiting_until_next_stationary_robot_is_reached()

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


