import time
from rclpy.node import Node

from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from armpi_pro_kinematics import ik_transform
from armpi_pro import bus_servo_control

from position_interface.msg import Position2D


class AssemblyMovement(Node):
    def __init__(self):
        super().__init__('movement_assembly_pro_node')
        self.__enable_rotation = True

        self.__ik = ik_transform.ArmIK()
        self.__joints_publisher = self.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)
        self.__assembly_position_subscriber = self.create_subscription(Position2D, 'assembly_position', self.__save_assembly_position, 1)

        self.__received_position = None

    def get_subscriber_list(self):
        return [self.__assembly_position_subscriber]

    def init_move(self):
        time.sleep(0.5)
        target = self.__ik.setPitchRanges((0, 0.24, 0.12), -90, -92, -88)
        self.__try_to_move_arm_to_target(target)

    def received_assembly_position(self):
        return self.__position is not None

    def __save_assembly_position(self, position2D_message):
        self.__position = position2D_message.x, position2D_message.y

    def open_claw(self):
        time.sleep(0.5)
        bus_servo_control.set_servos(self.__joints_publisher, 1.5, ((1, 50),))
        time.sleep(1.5)

    def move_arm_up(self):
        x_pos, y_pos = self.__constraint_the_assembly_position()

        time.sleep(0.5)

        target = self.__ik.setPitchRanges((x_pos, y_pos-0.01, 0.24), -90, -92, -88) # or you can use the position (0, 0.22)
        self.__try_to_move_arm_to_target(target)


    def move_arm_down(self):
        x_pos, y_pos = self.__constraint_the_assembly_position()

        time.sleep(0.5)

        target = self.__ik.setPitchRanges((x_pos, y_pos-0.01, 0.18), -90, -92, -88) # or you can use the position (0, 0.22)
        self.__try_to_move_arm_to_target(target)

    def __constraint_the_assembly_position(self):
        if self.__position[0] > 0:
            x_pos = 0 + self.__position[0] if 0 + self.__position[0] <= 0.03 else 0.03
        else:
            x_pos = 0 + self.__position[0] if 0 + self.__position[0] >= -0.03 else -0.03
        if self.__position[1] > 0:
            y_pos = 0.22 + self.__position[1] if 0.22 + self.__position[1] <= 0.24 else 0.24
        else:
            y_pos = 0.22 + self.__position[1] if 0.22 + self.__position[1] >= 0.20 else 0.20

        self.get_logger().info(f"The received position ({self.__position[0]}, {self.__position[1]}) was constrained "
                               f"to the position ({x_pos}, {y_pos})!")

        return x_pos, y_pos

    def __try_to_move_arm_to_target(self, target):
        if target:
            self.get_logger().info(f"I can reach the target with the following settings for the servos: {target}!")
            servo_data = target[1]
            bus_servo_control.set_servos(self.__joints_publisher, 1.5, (
                (2, 500),
                (3, servo_data['servo3']),
                (4, servo_data['servo4']),
                (5, servo_data['servo5']),
                (6, servo_data['servo6'])
            ))
            time.sleep(2)
        else:
            self.get_logger().info("I could not reach the target!")
