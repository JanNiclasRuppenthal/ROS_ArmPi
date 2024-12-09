import rclpy

from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from visual_processing.srv import SetParam
from visual_processing.msg import Result
from armpi_pro_kinematics import ik_transform
from armpi_pro import bus_servo_control, pid
from armpi_pro_service_client.client import call_service
from distance_ultrasonic.srv import Distance

from armpi_interfaces.msg import IDArmPi

import time
from threading import Thread



img_w = 640
img_h = 480
x_dis = 500
Z_DIS = 0.2
z_dis = Z_DIS
x_pid = pid.PID(P=0.08, I=0.001, D=0)  # pid initialization
z_pid = pid.PID(P=0.00003, I=0, D=0)

DISTANCE_CAMERA_ULTRASONIC = 0.07 # cm
count_messages = 0

enable_rotation = True

ik = ik_transform.ArmIK()

# TODO: Maybe I need to save the nodes somewhere
node = rclpy.create_node('grabbing_armpi_pro')
temp_grab_node = rclpy.create_node('temp_grab_node')
joints_pub = node.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)
trigger_grab_pub = node.create_publisher(IDArmPi, 'grabbed', 1)

master_node = None
grab_robot_id = -1


def get_grabbing_node():
    return node

def grab_init_move():
    time.sleep(0.5)

    target = ik.setPitchRanges((0, 0.12, 0.16), -90, -92, -88)
    if target:
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 2, ((1, 50), (2, 500), (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']),(6, servo_data['servo6'])))
        time.sleep(2)

def set_master_node_grabbing(n):
    global master_node 
    master_node = n

def set_grab_robot_id(id):
    global grab_robot_id

    grab_robot_id = id

def detect_pipe():
    global master_node, enable_rotation

    req = SetParam.Request()
    req.type = 'rectangle_detection'
    time.sleep(0.5)
    call_service(master_node, SetParam, '/visual_processing/set_running', req)
    enable_rotation = True

def stop_detecting():
    global master_node
    time.sleep(0.5)
    call_service(master_node, SetParam, '/visual_processing/set_running', SetParam.Request())
    print("Stop visual_processing service!")


def rotate_towards_object(x, y):
    global x_dis, z_dis

    # tracking along the X-axis
    x_pid.SetPoint = img_w / 2.0
    x_pid.update(x)
    dx = x_pid.output
    x_dis += int(dx)

    x_dis = 200 if x_dis < 200 else x_dis
    x_dis = 800 if x_dis > 800 else x_dis

    #tracking along the Z-axis
    z_pid.SetPoint = img_h / 2.0
    z_pid.update(y)
    dy = z_pid.output
    z_dis += dy

    z_dis = 0.22 if z_dis > 0.22 else z_dis
    z_dis = 0.17 if z_dis < 0.17 else z_dis

    target = ik.setPitchRanges((0, 0.12, 0.16,'''round(z_dis, 4)'''), -90, -92, -88)
    if target:
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 0.5, (
            (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, x_dis)))
        time.sleep(0.5)
        
    return dx, dy, x_dis, z_dis

def __convert_angle_to_pulse(angle):
    pulse = int(500 + angle * (1000 / 240))
    return pulse

def grab_pipe(x_dis, z_dis, angle):
    global DISTANCE_CAMERA_ULTRASONIC

    stop_detecting()

    x_dis += 5
    
    #height = round(z_dis, 2) + (DISTANCE_CAMERA_ULTRASONIC - 0.05) # 5 cm below the tracked point
    height = 0.21 # height if height <= 0.22 else 0.22
    print(f"new Height for ultrasonic sensor {height}")
    target = ik.setPitchRanges((0, 0.12, height), -90, -92, -88)
    if target:
        print(target)
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 1, (
            (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, x_dis)))
        time.sleep(2)

    dist_response = call_service(temp_grab_node, Distance, '/distance_ultrasonic/get_distance', Distance.Request())
    distance = (dist_response.distance_cm - 3.5) / 100
    print(f"Ultrasonic distance: {distance}")

    target = ik.setPitchRanges((0, 0.12 + distance, height), -90, -85, -95)
    if target:
        print(target)
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 1, (
            (2, __convert_angle_to_pulse(angle)), (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, x_dis)))
        time.sleep(2)
        print("I should be in the correct position!")
    else:
        print("not reachable!")
        return

    print("Grab the pipe!")
    time.sleep(0.5)
    bus_servo_control.set_servos(joints_pub, 0.5, ((1, 350), ))
    time.sleep(1)

    id_armpi_message = IDArmPi()
    id_armpi_message.id = grab_robot_id
    trigger_grab_pub.publish(id_armpi_message)
    node.get_logger().info(f"Send IDArmPi Message to {id_armpi_message.id}")

dist = None
def track_point_at_pipe(msg):
    global enable_rotation, dist, count_messages
    x = msg.center_x
    y = msg.center_y
    rotation_angle_of_pipe = msg.angle
    distance_x = None
    distance_y = None

    count_messages = (count_messages + 1) % 5

    if count_messages != 0:
        return

    # Do not rotate towards the object, if the robot is already aligned to the object
    if enable_rotation:
        distance_x, distance_y, x_dis, z_dis = rotate_towards_object(x, y)

    print(f"Distance: ({distance_x}, {distance_y})")

    if (enable_rotation and abs(distance_x) <= 1.0 and abs(distance_y) < 0.05):
        enable_rotation = False
        t1 = Thread(target=grab_pipe, args=(x_dis, z_dis, rotation_angle_of_pipe))
        t1.start()


result_sub = node.create_subscription(Result, '/visual_processing/result/rectangle_detection', track_point_at_pipe, 1)