from rclpy.node import Node

from armpi_pro import bus_servo_control
from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from chassis_control.msg import SetVelocity

import time

from movement.mobile.control_visual import ControlVisualProcessing
from movement.mobile.driving.backwards_buzzer import BackwardsBuzzer
from movement.mobile.driving.follow_line import FollowLineMovement
from transport_assembly.mobile.robot.armpi import ArmPi


class DriveMovement(Node):
    def __init__(self, armpi : ArmPi, control_visual_processing : ControlVisualProcessing, buzzer_allowed : bool):
        super().__init__('movement_drive_pro_node')
        self.__buzzer_allowed = buzzer_allowed
        self.__backwards_buzzer = BackwardsBuzzer()
        self.__follow_line_movement = FollowLineMovement(armpi, self, control_visual_processing)

        self.__set_velocity_publisher = self.create_publisher(SetVelocity, '/chassis_control/set_velocity', 1)
        self.__joints_publisher = self.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)

        self.__TWO_AND_HALF_SECONDS = 2.5

    def start_to_drive(self):
        self.__follow_line_movement.start_following_lines()

    def get_follow_line_movement(self):
        return self.__follow_line_movement

    def set_id_list_for_following_lines(self, id_list):
        self.__follow_line_movement.set_id_list_for_following_lines(id_list)

    def reached_the_next_stationary_robot(self):
        self.get_logger().info(f"Is the robot following the line? {self.__follow_line_movement.is_robot_following_line()}")
        if not self.__follow_line_movement.is_robot_following_line():
            self.__follow_line_movement.stop_visual_processing_for_following_lines()
            return True
        return False

    def init_move(self):
        time.sleep(0.5)
        bus_servo_control.set_servos(self.__joints_publisher, 1.5, ((2, 500), (3, 250), (4, 825), (5, 500),(6, 500)))
        time.sleep(2)

    def __create_set_velocity_message(self, velocity, direction, angular):
        set_velocity_message = SetVelocity()
        set_velocity_message.velocity = float(velocity)
        set_velocity_message.direction =  float(direction)
        set_velocity_message.angular =  float(angular)
        return set_velocity_message

    def stop_armpi_pro(self):
        self.get_logger().info("Sending SetVelocityMessage to stop driving!")
        stop_message = self.__create_set_velocity_message(0, 90, 0)
        self.__set_velocity_publisher.publish(stop_message)
        time.sleep(0.5)

    def drive_forward(self, duration_in_s):
        self.get_logger().info("Sending SetVelocityMessage to drive forward!")
        forward_message = self.__create_set_velocity_message(100, 90, 0)
        self.__set_velocity_publisher.publish(forward_message)
        time.sleep(duration_in_s)
        self.stop_armpi_pro()

    def drive_forward_with_angular_direction(self, dx):
        self.__set_velocity_publisher.publish(self.__create_set_velocity_message(100, 90, dx))

    def drive_forward_without_stopping(self, duration_in_s):
        self.get_logger().info("Sending SetVelocityMessage to drive forward without stopping!")
        forward_message = self.__create_set_velocity_message(100, 90, 0)
        self.__set_velocity_publisher.publish(forward_message)
        time.sleep(duration_in_s)

    def __drive_backward(self, duration_in_s):
        self.get_logger().info("Sending SetVelocityMessage to drive backward!")
        backwards_message = self.__create_set_velocity_message(75, -90, 0)
        self.__set_velocity_publisher.publish(backwards_message)

        if self.__buzzer_allowed:
            self.__backwards_buzzer.buzz(1200, 0.5, 0.5, 10)

        time.sleep(duration_in_s)

        self.stop_armpi_pro()

        if self.__buzzer_allowed:
            self.__backwards_buzzer.buzz(1200, 0.0, 0.0, 1)

    def rotate_90_deg_right(self):
        self.get_logger().info("Sending SetVelocityMessage to rotate 90 degrees to the right!")
        rotation_message = self.__create_set_velocity_message(0, 90, -0.45)
        self.__set_velocity_publisher.publish(rotation_message)
        time.sleep(self.__TWO_AND_HALF_SECONDS)
        self.stop_armpi_pro()

    def rotate_90_deg_left(self):
        self.get_logger().info("Sending SetVelocityMessage to rotate 90 degrees to the left!")
        rotation_message = self.__create_set_velocity_message(0, 90, 0.45)
        self.__set_velocity_publisher.publish(rotation_message)
        time.sleep(self.__TWO_AND_HALF_SECONDS)
        self.stop_armpi_pro()

    def drive_away_from_stationary_robot(self, id):
        self.__drive_backward(3.5)
        if id == 0:
            self.rotate_90_deg_right()
        elif id == 1:
            self.rotate_90_deg_left()

    def rotate_180_deg(self):
        self.get_logger().info("Sending SetVelocityMessage to rotate 180 degrees!")
        rotation_message = self.__create_set_velocity_message(0, 90, 0.45)
        self.__set_velocity_publisher.publish(rotation_message)
        time.sleep(self.__TWO_AND_HALF_SECONDS * 2)
        self.stop_armpi_pro()

    def park(self):
        last_id = self.__follow_line_movement.get_last_stationary_robot_id()
        if last_id == 0:
            self.rotate_90_deg_right()
        elif last_id == 1:
            self.rotate_90_deg_left()

        self.__drive_backward(7.5)