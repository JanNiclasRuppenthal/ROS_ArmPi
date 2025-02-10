from rclpy.node import Node

import time
from threading import Thread

from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from visual_processing.msg import Result
from armpi_pro_kinematics import ik_transform
from armpi_pro import bus_servo_control, pid

class PipeTracking(Node):
    def __init__(self, grab_movement):
        super().__init__('pipe_tracking_node')

        self.__img_w = 640
        self.__img_h = 480
        self.__x_dis = 500
        self.__Z_DIS = 0.2
        self.__z_dis = self.__Z_DIS
        self.__x_pid = pid.PID(P=0.08, I=0.001, D=0)  # pid initialization
        self.__z_pid = pid.PID(P=0.00003, I=0, D=0)

        self.__grab_movement = grab_movement

        self.__enable_rotation = False
        self.__count_messages = 0
        self.__ik = ik_transform.ArmIK()
        self.__joints_publisher = self.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)
        self.__result_sub = self.create_subscription(Result, '/visual_processing/result/rectangle_detection', self.__track_point_at_pipe, 1)

    def enable_rotation(self):
        self.__enable_rotation = True

    def __rotate_towards_object(self, x, y):
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


    def __track_point_at_pipe(self, msg):
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

        if self.__enable_rotation and self.__distance_to_pipe_is_small_enough(distance_x, distance_y):
            self.__enable_rotation = False
            t1 = Thread(target=self.__grab_movement.grab_pipe, args=(self.__x_dis, self.__z_dis, rotation_angle_of_pipe))
            t1.start()

    def __distance_to_pipe_is_small_enough(self, distance_x, distance_y):
        return abs(distance_x) <= 1.0 and abs(distance_y) < 0.05