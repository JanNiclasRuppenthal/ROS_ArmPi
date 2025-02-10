from rclpy.node import Node

import time

from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from armpi_pro_kinematics import ik_transform
from armpi_pro import bus_servo_control
from armpi_pro_service_client.client import call_service
from distance_ultrasonic.srv import Distance

from id_interface.msg import IDArmPi
from movement.mobile.control_visual import ControlVisualProcessing
from movement.mobile.pipes.track import PipeTracking


class GrabMovement(Node):
    def __init__(self, control_visual_processing : ControlVisualProcessing):
        super().__init__('movement_grab_pro_node')
        self.__pipe_tracker = PipeTracking(self)

        self.__DISTANCE_CAMERA_ULTRASONIC = 0.07 # cm
        self.__ik = ik_transform.ArmIK()

        self.__control_visual_processing = control_visual_processing

        self.__joints_publisher = self.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)
        self.__trigger_grab_publisher = self.create_publisher(IDArmPi, 'grabbed', 1)
        self.__grab_pipe_from_robot_id = -1


    def init_move(self):
        time.sleep(0.5)

        target = self.__ik.setPitchRanges((0, 0.12, 0.16), -90, -92, -88)
        if target:
            servo_data = target[1]
            bus_servo_control.set_servos(self.__joints_publisher, 2, (
                (1, 50),
                (2, 500),
                (3, servo_data['servo3']),
                (4, servo_data['servo4']),
                (5, servo_data['servo5']),
                (6, servo_data['servo6'])
            ))
            time.sleep(2)

    def get_tracking_pipe_node(self):
        return self.__pipe_tracker

    def set_grab_pipe_from_robot_id(self, id):
        self.__grab_pipe_from_robot_id = id

    def track_pipe(self):
        self.__pipe_tracker.enable_rotation()
        self.__control_visual_processing.set_visual_processing_to_tracking_pipe()

    def grab_pipe(self, x_dis, z_dis, angle):
        self.__control_visual_processing.stop_visual_processing()

        # rotate a little bit more
        x_dis += 5

        #height = round(z_dis, 2) + (DISTANCE_CAMERA_ULTRASONIC - 0.05) # 5 cm below the tracked point
        height = 0.21 # height if height <= 0.22 else 0.22
        target = self.__ik.setPitchRanges((0, 0.12, height), -90, -92, -88)
        if target:
            self.__move_arm_up_for_scanning_distance(target, x_dis)
        else:
            self.get_logger().warn(f"I could not reach the target!")

        dist_response = call_service(self, Distance, '/distance_ultrasonic/get_distance', Distance.Request())
        distance = (dist_response.distance_cm - 3.5) / 100
        self.get_logger().info(f"Got the following distance from the ultrasonic sensor: {distance} m!")

        target = self.__ik.setPitchRanges((0, 0.12 + distance, height), -90, -85, -95)
        if target:
            self.__move_to_the_tracked_pipe(angle, target, x_dis)
        else:
            self.get_logger().warn(f"I could not reach the target!")
            return

        self.__close_claw()
        self.__notify_stationary_robot_to_let_go_pipe()

    def __move_arm_up_for_scanning_distance(self, target, x_dis):
        self.get_logger().info(f"I move my arm up so that the ultrasonic sensor can scan the distance!")
        self.get_logger().info(f"I can reach the target with the following settings: {target}!")
        servo_data = target[1]
        bus_servo_control.set_servos(self.__joints_publisher, 1, (
            (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, x_dis)))
        time.sleep(2)

    def __move_to_the_tracked_pipe(self, angle, target, x_dis):
        self.get_logger().info(f"I move to the pipe!")
        self.get_logger().info(f"I can reach the target with the following settings: {target}!")
        servo_data = target[1]
        bus_servo_control.set_servos(self.__joints_publisher, 1, (
            (2, self.__convert_angle_to_pulse(angle)), (3, servo_data['servo3']), (4, servo_data['servo4']),
            (5, servo_data['servo5']), (6, x_dis)))
        time.sleep(2)

    def __convert_angle_to_pulse(self, angle):
        pulse = int(500 + angle * (1000 / 240))
        return pulse

    def __close_claw(self):
        self.get_logger().info("Grabbing the pipe!")
        time.sleep(0.5)
        bus_servo_control.set_servos(self.__joints_publisher, 0.5, ((1, 350),))
        time.sleep(1)

    def __notify_stationary_robot_to_let_go_pipe(self):
        id_armpi_message = IDArmPi()
        id_armpi_message.id = self.__grab_pipe_from_robot_id
        self.__trigger_grab_publisher.publish(id_armpi_message)
        self.get_logger().info(f"Notify stationary robot (ID = {id_armpi_message.id}) that I grabbed the pipe and "
                               f"it can let the pipe go!")
