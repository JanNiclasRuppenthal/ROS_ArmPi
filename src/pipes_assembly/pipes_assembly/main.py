import sys
import rclpy

from pipes_assembly.assembly import AssemblyPipes

object_id = 0

def read_all_arguments():
    ID = int(sys.argv[1])
    number_of_robots = int(sys.argv[2])
    return ID, number_of_robots

def main():
    rclpy.init()
    ID, number_of_robots = read_all_arguments()

    assembly_pipes = AssemblyPipes(ID, number_of_robots)
    assembly_pipes.start_scenario()

if __name__ == '__main__':
    main()