import rclpy
from rclpy.executors import MultiThreadedExecutor

from std_srvs.srv import Trigger

from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from visual_processing.msg import Result
from visual_processing.srv import SetParam

from armpi_pro_kinematics import ik_transform
from armpi_pro import bus_servo_control, pid
from armpi_pro_service_client.client import call_service
from armpi_pro_common_service.srv import SetTarget

from distance_ultrasonic.srv import Distance

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

rclpy.init()
node = rclpy.create_node('init')

joints_pub = node.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)

def initMove():
    bus_servo_control.set_servos(joints_pub, 0.5, ((1, 50),))
    time.sleep(0.5)

    target = ik.setPitchRanges((0, 0.12, 0.16), -90, -92, -88)
    if target:
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 2, ((1, 50), (2, 500), (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']),(6, servo_data['servo6'])))
        time.sleep(2)
 
def rotate_towards_object(x, y):
    global x_dis, z_dis

    # tracking along the X-axis
    x_pid.SetPoint = img_w / 2.0
    x_pid.update(x)
    dx = x_pid.output
    x_dis += int(dx)             
    #
    x_dis = 200 if x_dis < 200 else x_dis
    x_dis = 800 if x_dis > 800 else x_dis

    #tracking along the Z-axis
    z_pid.SetPoint = img_h / 2.0
    z_pid.update(y)
    dy = z_pid.output
    z_dis += dy

    z_dis = 0.22 if z_dis > 0.22 else z_dis
    z_dis = 0.17 if z_dis < 0.17 else z_dis

    target = ik.setPitchRanges((0, 0.12, round(z_dis, 4)), -90, -85, -95)
    if target:
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 0.5, (
            (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, x_dis)))
        time.sleep(0.5)
        
    return dx, dy, x_dis, z_dis

def grab(x_dis, z_dis):
    global DISTANCE_CAMERA_ULTRASONIC

    time.sleep(0.5)
    call_service(node, SetParam, '/visual_processing/set_running', SetParam.Request())
    print("Stop visual_processing service!")

    height = round(z_dis, 2) + (DISTANCE_CAMERA_ULTRASONIC - 0.05) # 5 cm below the tracked point
    print(f"new Height for ultrasonic sensor {height}")
    target = ik.setPitchRanges((0, 0.12, height), -90, -85, -95)
    if target:
        print(target)
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 1, (
            (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, x_dis)))
        time.sleep(2)

    dist_response = call_service(node, Distance, '/distance_ultrasonic/get_distance', Distance.Request())
    distance = (dist_response.distance_cm - 2.5) / 100
    print(f"Ultrasonic distance: {distance}")

    target = ik.setPitchRanges((0, 0.12 + distance, height + 0.01), -90, -85, -95)
    if target:
        print("reachable")
        print(target)
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 1, (
            (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, x_dis)))
        time.sleep(2)
        print("I should be in the correct position!")
    else:
        print("not reachable!")
        return

    print("Grab the pipe!")
    time.sleep(0.5)
    bus_servo_control.set_servos(joints_pub, 0.5, ((1, 350), ))
    time.sleep(1)

dist = None
def run(msg):
    global enable_rotation, dist, count_messages

    x = msg.center_x
    y = msg.center_y
    other_data = msg.data
    distance_x = None
    distance_y = None

    count_messages = (count_messages + 1) % 10

    if count_messages != 0:
        return

    # Do not rotate towards the object, if the robot is already aligned to the object
    if enable_rotation:
        distance_x, distance_y, x_dis, z_dis = rotate_towards_object(x, y)

    print(f"Distance: ({distance_x}, {distance_y})")

    #TODO: What if distance_x is constant? Try to modify the pulse of servo 6

    if (enable_rotation and abs(distance_x) <= 0.75 and abs(distance_y) < 0.05):
        enable_rotation = False
        t1 = Thread(target=grab, args=(x_dis, z_dis,))
        t1.start()
        

          

initMove()
time.sleep(4)

call_service(node, Trigger, '/visual_processing/enter', Trigger.Request())
result_sub = node.create_subscription(Result, '/visual_processing/result', run, 1)

req = SetParam.Request()
req.type = 'transport_scenario'
req.color = 'green'
call_service(node, SetParam, '/visual_processing/set_running', req)

executor = MultiThreadedExecutor()
executor.add_node(node)
executor.spin()