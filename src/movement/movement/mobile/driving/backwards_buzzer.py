from rclpy.node import Node

from ros_robot_controller.msg import BuzzerState

class BackwardsBuzzer(Node):
    def __init__(self):
        super().__init__('buzzer_node')
        self.__buzzer_publisher = self.create_publisher(BuzzerState, '/ros_robot_controller/set_buzzer', 1)

    def __create_buzzer_state_message(self, freq, on_time, off_time, repeat):
        set_buzzer_state_message = BuzzerState()
        set_buzzer_state_message.freq = int(freq)
        set_buzzer_state_message.on_time = float(on_time)
        set_buzzer_state_message.off_time = float(off_time)
        set_buzzer_state_message.repeat = int(repeat)
        return set_buzzer_state_message

    def buzz(self, freq, on_time, off_time, repeat):
        start_buzzer_message = self.__create_buzzer_state_message(freq, on_time, off_time, repeat)
        self.__buzzer_publisher.publish(start_buzzer_message)