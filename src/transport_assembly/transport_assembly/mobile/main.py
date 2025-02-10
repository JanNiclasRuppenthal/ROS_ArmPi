import sys
import rclpy
rclpy.init()
from transport_assembly.mobile.transport import Transporter

def read_argument():
    number_of_stationary_robots = int(sys.argv[1])
    allow_buzzer = bool(int(sys.argv[2]))
    return number_of_stationary_robots, allow_buzzer

def main():

    number_of_stationary_robots, allow_buzzer = read_argument()

    transporter = Transporter(number_of_stationary_robots, allow_buzzer)
    transporter.start_scenario()


if __name__ == '__main__':
    main()