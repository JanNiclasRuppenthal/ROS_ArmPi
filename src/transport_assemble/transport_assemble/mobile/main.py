import rclpy

from std_srvs.srv import *

from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from visual_processing.msg import Result
from visual_processing.srv import SetParam
from color_tracking.srv import SetTarget #TODO: change that to a new service in armpi_pro_jazzy

from armpi_pro_kinematics import ik_transform
from armpi_pro import bus_servo_control, pid
from armpi_pro_service_client.client import call_service
from distance_ultrasonic.srv import Distance

img_w = 640
img_h = 480
x_dis = 500
Z_DIS = 0.2
z_dis = Z_DIS
x_pid = pid.PID(P=0.08, I=0.001, D=0)  # pid初始化(pid initialization)
z_pid = pid.PID(P=0.00003, I=0, D=0)

enable_rotation = True

ik = ik_transform.ArmIK()

rclpy.init()
node = rclpy.create_node('init')

joints_pub = node.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)

def initMove():
    target = ik.setPitchRanges((0, 0.12, 0.16), -90, -92, -88) # 逆运动学求解(inverse kinematics solving)
    if target:
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 1.5, ((1, 200), (2, 500), (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']),(6, servo_data['servo6'])))
 
def rotate_towards_object(x, y):
    global x_dis, z_dis

    # X轴追踪(tracking along the X-axis)
    x_pid.SetPoint = img_w / 2.0  # 设定(set)
    x_pid.update(x)        # 当前(current)
    dx = x_pid.output      # 输出(output)
    x_dis += int(dx)             
    # 限幅(Clamping)
    x_dis = 200 if x_dis < 200 else x_dis
    x_dis = 800 if x_dis > 800 else x_dis

    # Z轴追踪((tracking along the Z-axis)）
    z_pid.SetPoint = img_h / 2.0  # 设定(set)
    z_pid.update(y)        # 当前(current)
    dy = z_pid.output      # 输出(output)
    z_dis += dy

    z_dis = 0.22 if z_dis > 0.22 else z_dis
    z_dis = 0.17 if z_dis < 0.17 else z_dis

    target = ik.setPitchRanges((0, 0.12, 0.16), -90, -85, -95) # 逆运动学求解（inverse kinematics solving）
    if target:
        servo_data = target[1]
        bus_servo_control.set_servos(joints_pub, 0.02, (
            (3, servo_data['servo3']), (4, servo_data['servo4']), (5, servo_data['servo5']), (6, x_dis)))
        
    return dx, dy


def run(msg):
    global enable_rotation

    x = msg.center_x
    y = msg.center_y
    other_data = msg.data
    distance_x = 0
    distance_y = 0

    # Do not rotate towards the object, if the robot is already aligned to the object
    #if enable_rotation:
    distance_x, distance_y = rotate_towards_object(x, y)

    if (abs(distance_x) < 1 and abs(distance_y) < 0.5):
        #enable_rotation = False
        print("here")
        req = Distance.Request()
        dist = call_service(node, Distance, '/get_distance', req)

initMove()

call_service(node, Trigger, '/visual_processing/enter', Trigger.Request())
result_sub = node.create_subscription(Result, '/visual_processing/result', run, 1)

req = SetParam.Request()
req.type = 'transport_scenario'
req.color = 'green'
call_service(node, SetParam, '/visual_processing/set_running', req)


rclpy.spin(node)