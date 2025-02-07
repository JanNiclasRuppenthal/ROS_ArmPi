import sys

import rclpy
from transport_assembly.stationary.transport import TransportAssembly

def read_all_arguments():
    ID = int(sys.argv[1])
    number_of_stationary_robots = int(sys.argv[2])
    return ID, number_of_stationary_robots

def main():
    rclpy.init()

    ID, number_of_stationary_robots = read_all_arguments()

    transport_assembly = TransportAssembly(ID, number_of_stationary_robots)
    transport_assembly.start_scenario()


if __name__ == '__main__':
    main()