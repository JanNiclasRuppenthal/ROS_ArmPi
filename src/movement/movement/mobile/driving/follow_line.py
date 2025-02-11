from rclpy.node import Node

from armpi_pro import pid
from visual_processing.msg import Result

from movement.mobile.control_visual import ControlVisualProcessing
from movement.mobile.driving.state import DrivingState
from transport_assembly.mobile.robot.armpi import ArmPi


class FollowLineMovement(Node):
    def __init__(self, armpi : ArmPi, drive_movement, control_visual_processing : ControlVisualProcessing):
        super().__init__('movement_follow_line_pro_node')
        self.__armpi = armpi
        self.__drive_movement = drive_movement
        self.__control_visual_processing = control_visual_processing

        self.__follow_lines_subscriber = self.create_subscription(Result, '/visual_processing/result/line', self.__follow_lines, 1)

        self.__img_w = 640
        self.__x_pid = pid.PID(P=0.003, I=0.0001, D=0.0001)

        self.__start = False
        self.__following_lines = False
        self.__last_width_of_detected_line  = 0
        self.__driving_state = DrivingState.DRIVE_TO_HANDOVER
        self.__next_stationary_robot_id = -1
        self.__last_stationary_robot_id = -1

        self.__list_with_stationary_robot_ids = []

    def start_following_lines(self):
        self.__control_visual_processing.set_visual_processing_to_following_line()
        self.__start = True
        self.__following_lines = True

    def stop_visual_processing_for_following_lines(self):
        self.__control_visual_processing.stop_visual_processing()
        self.__following_lines = False

    def is_robot_following_line(self):
        return self.__following_lines

    def set_id_list_for_following_lines(self, id_list):
        self.__list_with_stationary_robot_ids = id_list

    def get_last_stationary_robot_id(self):
        return self.__last_stationary_robot_id

    def __is_list_with_stationary_robot_ids_full(self):
        return len(self.__list_with_stationary_robot_ids) == self.__armpi.get_number_of_stationary_robots()

    def __is_list_with_stationary_robot_ids_empty(self):
        return len(self.__list_with_stationary_robot_ids) == 0

    def __pop_first_element_of_list_with_stationary_robot_ids(self):
        if self.__no_stationary_robot_left():
            return -1
        return self.__list_with_stationary_robot_ids.pop(0)

    def __get_first_element_of_list_with_stationary_robot_ids(self):
        if self.__no_stationary_robot_left():
            return -1
        return self.__list_with_stationary_robot_ids[0]

    def __follow_lines(self, msg):
        center_x = msg.center_x
        width_of_detected_line = msg.data

        if self.__detected_turn(width_of_detected_line):

            if self.__driving_state == DrivingState.DRIVE_TO_HANDOVER:
                self.__drive_movement.drive_forward_without_stopping(2.4)

                if self.__no_stationary_robot_left():
                    self.stop_visual_processing_for_following_lines()
                    self.__start = False
                    self.__drive_movement.stop_armpi_pro()

                elif self.__last_stationary_robot_id == -1 and self.__is_list_with_stationary_robot_ids_full():
                    self.__handle_first_turn_to_handover()

                self.__driving_state = DrivingState.DRIVE_TO_ASSEMBLY
                self.get_logger().info("Changing my driving state to DRIVE_TO_ASSEMBLY!")

            elif self.__driving_state == DrivingState.DRIVE_TO_ASSEMBLY:
                self.__handle_turn_to_assembly()

                self.__driving_state = DrivingState.DRIVE_TO_HANDOVER
                self.get_logger().info("Changing my driving state to DRIVE_TO_HANDOVER!")
                self.__last_stationary_robot_id = self.__next_stationary_robot_id
                return

        if self.__start and width_of_detected_line > 0:
            dx = self.__calculate_x_angular_direction(center_x)
            self.__drive_movement.drive_forward_with_angular_direction(dx)
            self.__following_lines = True

            if 20 <= width_of_detected_line:
                self.__last_width_of_detected_line = width_of_detected_line

        else:
            if self.__following_lines:
                self.get_logger().warn("Could not detect any line!")
                self.__following_lines = False
                self.__drive_movement.stop_armpi_pro()

    def __detected_turn(self, width_of_detected_line):
        return self.__last_width_of_detected_line != 0 and width_of_detected_line > 120

    def __no_stationary_robot_left(self):
        return self.__is_list_with_stationary_robot_ids_empty()

    def __handle_first_turn_to_handover(self):
        self.__drive_movement.stop_armpi_pro()
        first_id_in_list = self.__get_first_element_of_list_with_stationary_robot_ids()
        self.get_logger().info(f"Rotation based on the first ID in my list: {first_id_in_list}")
        self.__rotate_base_on_the_id(first_id_in_list)

    def __handle_turn_to_assembly(self):
        self.__next_stationary_robot_id = self.__pop_first_element_of_list_with_stationary_robot_ids()
        self.get_logger().info(
            f"For the assembly I drive to the stationary robot (ID = {self.__next_stationary_robot_id})!")
        time_to_drive = 2.5
        if self.__no_stationary_robot_left():
            '''
            Because of the grabbed pipe, the camera view of the driving robot is constrained.
            Because of that, it needs to drive a little bit longer
            '''
            time_to_drive = 2.75

        self.__drive_movement.drive_forward(time_to_drive)

        self.get_logger().info(
            f"Rotation based on the next ID of the stationary robot: {self.__next_stationary_robot_id}")
        self.__rotate_base_on_the_id(self.__next_stationary_robot_id)

    def __rotate_base_on_the_id(self, id):
        if id == 0:
            self.__drive_movement.rotate_90_deg_right()
        else:
            self.__drive_movement.rotate_90_deg_left()

    def __calculate_x_angular_direction(self, center_x):
        if abs(center_x - self.__img_w / 2) < 20:
            center_x = self.__img_w / 2
        self.__x_pid.SetPoint = self.__img_w / 2
        self.__x_pid.update(center_x)
        dx = round(self.__x_pid.output, 2)
        dx = 0.1 if dx > 0.1 else dx
        dx = -0.1 if dx < -0.1 else dx
        return dx