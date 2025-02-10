import rclpy
from rclpy.node import Node

import time
from threading import Thread

from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from visual_processing.msg import Result
from armpi_pro_kinematics import ik_transform
from armpi_pro import bus_servo_control, pid
from armpi_pro_service_client.client import call_service
from distance_ultrasonic.srv import Distance

from id_interface.msg import IDArmPi
from movement.mobile.control_visual import ControlVisualProcessing


class GrabMovement(Node):
    def __init__(self, control_visual_processing : ControlVisualProcessing):
        super().__init__('movement_grab_pro_node')
        self.__img_w = 640
        self.__img_h = 480
        self.__x_dis = 500
        self.__Z_DIS = 0.2
        self.__z_dis = self.__Z_DIS
        self.__x_pid = pid.PID(P=0.08, I=0.001, D=0)  # pid initialization
        self.__z_pid = pid.PID(P=0.00003, I=0, D=0)

        self.__DISTANCE_CAMERA_ULTRASONIC = 0.07 # cm
        self.__ik = ik_transform.ArmIK()

        self.__control_visual_processing = control_visual_processing

        self.__joints_publisher = self.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)
        self.__trigger_grab_publisher = self.create_publisher(IDArmPi, 'grabbed', 1)
        self.__result_sub = self.create_subscription(Result, '/visual_processing/result/rectangle_detection', self.__track_point_at_pipe, 1)

        self.__count_messages = 0
        self.__enable_rotation = True
        self.__grab_pipe_from_robot_id = -1


    def init_move(self):
        time.sleep(0.5)

        target = self.__ik.setPitchRanges((0, 0.12, 0.16), -90, -92, -88)
        if target:
            servo_data = target[1]
            bus_servo_control.set_servos(self.__joints_publisher, 2, ((1, 50), (2, 500), (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']),(6, servo_data['servo6'])))
            time.sleep(2)

    def set_grab_pipe_from_robot_id(self, id):
        self.__grab_pipe_from_robot_id = id

    def enable_rotation(self):
        self.__enable_rotation = True

    def __rotate_towards_object(self, x, y): #tracking
        # tracking along the X-axis
        self.__x_pid.SetPoint = self.__img_w / 2.0
        self.__x_pid.update(x)
        dx = self.__x_pid.output
        self.__x_dis += int(dx)

        self.__x_dis = 200 if self.__x_dis < 200 else self.__x_dis
        self.__x_dis = 800 if self.__x_dis > 800 else self.__x_dis

        #tracking along the Z-axis
        self.__z_pid.SetPoint = self.__img_h / 2.0
        self.__z_pid.update(y)
        dy = self.__z_pid.output
        self.__z_dis += dy

        self.__z_dis = 0.22 if self.__z_dis > 0.22 else self.__z_dis
        self.__z_dis = 0.17 if self.__z_dis < 0.17 else self.__z_dis

        target = self.__ik.setPitchRanges((0, 0.12, 0.16,'''round(z_dis, 4)'''), -90, -92, -88)
        if target:
            servo_data = target[1]
            bus_servo_control.set_servos(self.__joints_publisher, 0.5, (
                (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, self.__x_dis)))
            time.sleep(0.5)

        return dx, dy

    def __convert_angle_to_pulse(self, angle):
        pulse = int(500 + angle * (1000 / 240))
        return pulse

    def __grab_pipe(self, x_dis, z_dis, angle):
        self.__control_visual_processing.stop_visual_processing()

        x_dis += 5

        #height = round(z_dis, 2) + (DISTANCE_CAMERA_ULTRASONIC - 0.05) # 5 cm below the tracked point
        height = 0.21 # height if height <= 0.22 else 0.22
        target = self.__ik.setPitchRanges((0, 0.12, height), -90, -92, -88)
        if target:
            self.get_logger().info(f"I can reach the target with the following settings: {target}!")
            servo_data = target[1]
            bus_servo_control.set_servos(self.__joints_publisher, 1, (
                (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, x_dis)))
            time.sleep(2)
        else:
            self.get_logger().warn(f"I could not reach the target!")

        dist_response = call_service(self, Distance, '/distance_ultrasonic/get_distance', Distance.Request())
        distance = (dist_response.distance_cm - 3.5) / 100
        self.get_logger().info(f"Ultrasonic distance: {distance}")

        target = self.__ik.setPitchRanges((0, 0.12 + distance, height), -90, -85, -95)
        if target:
            self.get_logger().info(f"I can reach the target with the following settings: {target}!")
            servo_data = target[1]
            bus_servo_control.set_servos(self.__joints_publisher, 1, (
                (2, self.__convert_angle_to_pulse(angle)), (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, x_dis)))
            time.sleep(2)
        else:
            self.get_logger().info("not reachable!")
            return

        self.get_logger().info("Grab the pipe!")
        time.sleep(0.5)
        bus_servo_control.set_servos(self.__joints_publisher, 0.5, ((1, 350), ))
        time.sleep(1)

        id_armpi_message = IDArmPi()
        id_armpi_message.id = self.__grab_pipe_from_robot_id
        self.__trigger_grab_publisher.publish(id_armpi_message)
        self.get_logger().info(f"Send IDArmPi Message to {id_armpi_message.id}")

    def __track_point_at_pipe(self, msg): #tracking
        x = msg.center_x
        y = msg.center_y
        rotation_angle_of_pipe = msg.angle
        distance_x = None
        distance_y = None

        self.__count_messages = (self.__count_messages + 1) % 5

        if self.__count_messages != 0:
            return

        # Do not rotate towards the object, if the robot is already aligned to the object
        if self.__enable_rotation:
            distance_x, distance_y = self.__rotate_towards_object(x, y)

        print(f"Calculated distance to the detected pipe: ({distance_x}, {distance_y})!")

        if self.__enable_rotation and abs(distance_x) <= 1.0 and abs(distance_y) < 0.05:
            self.__enable_rotation = False
            t1 = Thread(target=self.__grab_pipe, args=(self.__x_dis, self.__z_dis, rotation_angle_of_pipe))
            t1.start()