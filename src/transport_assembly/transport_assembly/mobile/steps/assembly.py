from rclpy.node import Node

import time

from transport_assembly.mobile.robot.publisher.assembly_step_publisher import AssemblyStepPublisher

class AssemblyStep(Node):
    def __init__(self, transporter):
        super().__init__('process_assembly_step_node')
        self.__transporter = transporter
        self.__armpi = transporter.get_armpi()
        self.__assembly_movement = transporter.get_assembly_movement()
        self.__drive_movement = transporter.get_drive_movement()
        self.__grab_movement = transporter.get_grab_movement()
        self.__assembly_step_publisher = AssemblyStepPublisher(self.__armpi)


    def assembly_grabbed_pipe_process(self) -> int:
        self.__drive_movement.init_move()
        self.__drive_movement.start_to_drive()
        id_from_stationary_robot_to_assembly = self.__armpi.pop_IDList()

        self.get_logger().info(f"Driving to the next robot (ID = {id_from_stationary_robot_to_assembly})!")
        self.__transporter.waiting_until_next_stationary_robot_is_reached()
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

        return id_from_stationary_robot_to_assembly

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