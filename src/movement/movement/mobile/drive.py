import rclpy

from visual_processing.srv import SetParam
from hiwonder_servo_msgs.msg import MultiRawIdPosDur
from chassis_control.msg import SetVelocity
from visual_processing.msg import Result

from armpi_pro import bus_servo_control, pid
from armpi_pro_service_client.client import call_service

from ros_robot_controller.msg import BuzzerState

import time

node = rclpy.create_node('driving_node')
set_velocity = node.create_publisher(SetVelocity, '/chassis_control/set_velocity', 1)
joints_pub = node.create_publisher(MultiRawIdPosDur, '/servo_controllers/port_id_1/multi_id_pos_dur', 1)
buzzer_publisher = node.create_publisher(BuzzerState, '/ros_robot_controller/set_buzzer', 1)

img_w = 640
x_pid = pid.PID(P=0.003, I=0.0001, D=0.0001)

TWO_AND_HALF_SECONDS = 2.5
move = None
last_width  = 0

master_node = None 
count = 0
allow_buzzer = False


def set_master_node_driving(n):
    global master_node 
    master_node = n

def set_allow_buzzer(value):
    global allow_buzzer
    allow_buzzer = value

def get_driving_node():
    return node
    

def start_to_drive():
    global master_node

    req = SetParam.Request()
    req.type = 'line'
    req.color = 'frogtape'
    time.sleep(0.5)
    call_service(master_node, SetParam, '/visual_processing/set_running', req)
    print("Call the visual processing")
    time.sleep(0.5)

def drive_init_move():
    time.sleep(0.5)
    bus_servo_control.set_servos(joints_pub, 1.5, ((2, 500), (3, 250), (4, 825), (5, 500),(6, 500)))
    #bus_servo_control.set_servos(joints_pub, 1.5, ((2, 750), (3, 250), (4, 900), (5, 500),(6, 500)))
    time.sleep(2)


def __create_set_velocity_message(velocity, direction, angular):
    set_velocity_message = SetVelocity()
    set_velocity_message.velocity = float(velocity)
    set_velocity_message.direction =  float(direction)
    set_velocity_message.angular =  float(angular)
    return set_velocity_message


def __create_buzzer_state_message(freq, on_time, off_time, repeat):
    set_buzzer_state_message = BuzzerState()
    set_buzzer_state_message.freq = int(freq)
    set_buzzer_state_message.on_time = float(on_time)
    set_buzzer_state_message.off_time = float(off_time)
    set_buzzer_state_message.repeat = int(repeat)

    return set_buzzer_state_message


def __stop_armpi_pro():
    stop_message = __create_set_velocity_message(0, 90, 0)
    set_velocity.publish(stop_message)
    time.sleep(0.5)


def drive_forward(duration_in_s):
    backwards_message = __create_set_velocity_message(100, 90, 0)
    set_velocity.publish(backwards_message)

    time.sleep(duration_in_s)

    __stop_armpi_pro()


def reached_the_next_stationary_robot():
    global master_node
    global move
    if move == False:
        time.sleep(0.5)
        call_service(master_node, SetParam, '/visual_processing/set_running', SetParam.Request())
        print("Stop the visual processing!")
        move = None # reset the move variable
        return True
    return False


def drive_backward(duration_in_s):
    global allow_buzzer

    backwards_message = __create_set_velocity_message(75, -90, 0)
    set_velocity.publish(backwards_message) 

    if allow_buzzer:
        start_buzzer_message = __create_buzzer_state_message(1200, 0.5, 0.5, 10)
        buzzer_publisher.publish(start_buzzer_message)

    time.sleep(duration_in_s)

    __stop_armpi_pro()

    if allow_buzzer:
        stop_buzzer_message = __create_buzzer_state_message(1200, 0.0, 0.0, 1)
        buzzer_publisher.publish(stop_buzzer_message)
    

def rotate_90_deg_right():
    backwards_message = __create_set_velocity_message(0, 90, -0.45)
    set_velocity.publish(backwards_message) 

    time.sleep(TWO_AND_HALF_SECONDS)

    __stop_armpi_pro()

def rotate_90_deg_left():
    backwards_message = __create_set_velocity_message(0, 90, 0.45)
    set_velocity.publish(backwards_message) 

    time.sleep(TWO_AND_HALF_SECONDS)

    __stop_armpi_pro()


def follow_lines(msg):
    global move, last_width, count
    
    center_x = msg.center_x
    width = msg.data

    if last_width != 0 and width > 60:
        drive_forward(2.75)
        if count == 0:
            count += 1
            rotate_90_deg_right()
        else:
            count = 0
            rotate_90_deg_left()
        return

    if width > 0: # and not detected_edge:
        if abs(center_x - img_w/2) < 20: 
            center_x = img_w/2
        x_pid.SetPoint = img_w/2
        x_pid.update(center_x)
        dx = round(x_pid.output, 2)
        dx = 0.8 if dx > 0.8 else dx
        dx = -0.8 if dx < -0.8 else dx
        set_velocity.publish(__create_set_velocity_message(100, 90, dx))
        move = True

        if 20 <= width:
            last_width = width
            
    else:
        if move:
            move = False
            __stop_armpi_pro()


follow_lines_subscriber = node.create_subscription(Result, '/visual_processing/result/line', follow_lines, 1)