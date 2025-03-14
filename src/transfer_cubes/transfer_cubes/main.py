import sys
import rclpy

from transfer_cubes.transfer import TransferCubes


def read_all_arguments():
    ID = int(sys.argv[1])
    last_robot = bool(int(sys.argv[2]))

    return ID, last_robot

def main():
    rclpy.init()

    ID, last_robot = read_all_arguments()

    transfer_cubes = TransferCubes(ID, last_robot)
    transfer_cubes.start_scenario()


if __name__ == '__main__':
    main()