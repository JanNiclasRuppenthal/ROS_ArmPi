import time
from ArmIK.ArmMoveIK import *
import HiwonderSDK.Board as Board
import math

from rclpy.node import Node


class Deliver(Node):
    def __init__(self, coordinate_calc):
        super().__init__("stationary_deliver_node")
        self.__AK = ArmIK()
        self.__coordinate_calculation = coordinate_calc

        self.__coordinates_last = {
            'red':   (-15 + 0.5, 12 - 0.5, 1.5),
            'green': (-15 + 0.5, 6 - 0.5,  1.5),
            'blue':  (-15 + 0.5, 0 - 0.5,  1.5)
        }

        self.__coordinates = {
            'red':   (-30 + 0.5, 12 - 0.5, 1.5),
            'green': (-30 + 0.5, 6 - 0.5,  1.5),
            'blue':  (-30 + 0.5, 0 - 0.5,  1.5)
        }

        self.__count_placed_colored_cubes = {
            'red':   0,
            'green': 0,
            'blue':  0
        }

    def init_move(self):
        Board.setBusServoPulse(1, 450, 300)
        Board.setBusServoPulse(2, 500, 500)
        self.__AK.setPitchRangeMoving((0, 10, 10), -30, -30, -90, 1500)

    def are_coordinates_valid(self, x, y):
        return x != -1 and y != -1

    def __convert_angle_to_pulse(self, x, y, angle):
        # We need to declare that the y-Axis has a degree of zero degreees and not 90 degrees
        # Because of that we need to subtract 90 to the result of atan2
        angle_from_origin_to_object = 90 - round(math.degrees(math.atan2(y, abs(x))), 1)

        # If the object has a positive x coordinate, then the servo needs to decrement its pulse
        # so that the arm is aligned with the x-axis
        if x > 0:
            angle_from_origin_to_object = -angle_from_origin_to_object

        angle_right = angle
        angle_left = angle - 90

        rotation_angle, rotation_direction = self.__calculate_rotation(angle_left, angle_right)

        calculated_angle = (angle_from_origin_to_object + rotation_direction * rotation_angle)
        pulse = int(500 + calculated_angle * (1000 / 240))
        return pulse

    def __calculate_rotation(self, angle_left, angle_right):
        if abs(angle_right) < abs(angle_left):
            rotation_angle = abs(angle_right)
            rotation_direction = 1
        else:
            rotation_angle = abs(angle_left)
            rotation_direction = -1
        return rotation_angle, rotation_direction

    def deliver_cube(self, x, y, last_robot):
        detected_color = self.__coordinate_calculation.get_detected_color()

        # placement coordinate
        '''
        placement coordinate:
        normal: (-15 + 0.5, y, 1.5)
        -35.2 = 35.7 + 0.5 is unreachable 
        '''

        goal_coord_x, goal_coord_y, goal_coord_z = self.determine_goal_coordinates(detected_color, last_robot)

        # Remove to target position, high is 6 cm, through return result to judge whether it can reach the specified location
        # if the running time is not given，it is automatically calculated and returned by the result
        result = self.__AK.setPitchRangeMoving((x, y, 7), -90, -90, 0)
        if result:
            time.sleep(result[2]/1000) # if it can reach to specified location, then get running time

            self.__open_claw()

            self.__move_to_cube(x, y)

            self.__close_claw()

            Board.setBusServoPulse(2, 500, 500)
            self.__AK.setPitchRangeMoving((x, y, 12), -90, -90, 0, 1000)  # ArmPi Robot arm up
            time.sleep(1)

            self.__move_to_goal_coordinate(goal_coord_x, goal_coord_y, goal_coord_z)

            self.__open_claw()

            self.__AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, 12), -90, -90, 0, 800) # ArmPi Robot arm up
            time.sleep(0.8)

            self.__count_placed_colored_cubes[detected_color] += 1
        else:
            self.get_logger().warn("Could not reach the coordinates %s" % str(x, y))


    def __open_claw(self):
        self.get_logger().info("Opening Claw")
        Board.setBusServoPulse(1, 220, 500)
        time.sleep(0.8)


    def __close_claw(self):
        self.get_logger().info("Closing Claw")
        Board.setBusServoPulse(1, 500, 500)
        time.sleep(0.8)


    def determine_goal_coordinates(self, detected_color, last_robot):
        goal_coordinates = self.__coordinates if (not last_robot) else self.__coordinates_last
        goal_coord_x, goal_coord_y, goal_coord_z = goal_coordinates[detected_color]

        # Last robot in the line should stack the cubes
        # A cube is 5 cm * 5 cm * 5cm
        # The robot has to move up its arm by 2.5 cm because the robot grabs the middle of the cube
        if last_robot:
            goal_coord_z += self.__count_placed_colored_cubes[detected_color] * 2.5

        self.get_logger().info(f"Calculated coordinates: ({goal_coord_x}, {goal_coord_y}, {goal_coord_z})")

        return goal_coord_x, goal_coord_y, goal_coord_z


    def __move_to_cube(self, x, y):
        servo2_pulse = self.__convert_angle_to_pulse(x, y, self.__coordinate_calculation.get_rotation_angle())
        Board.setBusServoPulse(2, servo2_pulse, 500)  # rotate the second servo
        time.sleep(0.5)

        self.__AK.setPitchRangeMoving((x, y, 1.5), -90, -90, 0, 1000)  # ArmPi goes to the position of the detected cube
        time.sleep(1.5)


    def __move_to_goal_coordinate(self, goal_coord_x, goal_coord_y, goal_coord_z):
        # ArmPi goes to the goal coordinates with z = 12
        result = self.__AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, 12), -90, -90, 0)
        time.sleep(result[2] / 1000)

        servo2_angle = getAngle(goal_coord_x, goal_coord_y, -90)
        Board.setBusServoPulse(2, servo2_angle, 500)
        time.sleep(0.5)

        # ArmPi goes down to z = goal_coord_z + 3
        self.__AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, goal_coord_z + 3), -90, -90, 0, 500)
        time.sleep(0.5)

        # ArmPi is at the next coordinates
        self.__AK.setPitchRangeMoving((goal_coord_x, goal_coord_y, goal_coord_z), -90, -90, 0, 1000)
        time.sleep(0.8)