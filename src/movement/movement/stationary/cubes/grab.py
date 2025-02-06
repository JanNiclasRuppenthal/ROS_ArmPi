import time
import HiwonderSDK.Board as Board
import math

from rclpy.node import Node


class GrabCube(Node):
    def __init__(self, AK):
        super().__init__("stationary_grab_node")
        self.__AK = AK

    def grab_cube(self, x, y, rotation_angle):

        grabbed = False

        # Remove to target position, high is 6 cm, through return result to judge whether it can reach the specified location
        # if the running time is not given，it is automatically calculated and returned by the result
        result = self.__AK.setPitchRangeMoving((x, y, 7), -90, -90, 0)
        if result:
            time.sleep(result[2]/1000) # if it can reach to specified location, then get running time
            self.open_claw()

            self.__move_to_cube(x, y, rotation_angle)

            self.close_claw()

            Board.setBusServoPulse(2, 500, 500)
            grabbed = True
        else:
            self.get_logger().warn("Could not reach the coordinates %s" % str(x, y))

        return grabbed

    def open_claw(self):
        self.get_logger().info("Opening Claw")
        Board.setBusServoPulse(1, 220, 500)
        time.sleep(0.8)

    def close_claw(self):
        self.get_logger().info("Closing Claw")
        Board.setBusServoPulse(1, 500, 500)
        time.sleep(0.8)


    def __move_to_cube(self, x, y, rotation_angle):
        servo2_pulse = self.__convert_angle_to_pulse(x, y, rotation_angle)
        Board.setBusServoPulse(2, servo2_pulse, 500)  # rotate the second servo
        time.sleep(0.5)

        self.get_logger().info(f"Moving to cube at ({x}, {y}, 1.5)")
        self.__AK.setPitchRangeMoving((x, y, 1.5), -90, -90, 0, 1000)  # ArmPi goes to the position of the detected cube
        time.sleep(1.5)

    def __convert_angle_to_pulse(self, x, y, angle):
        # We need to declare that the y-Axis has a degree of zero degrees and not 90 degrees
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

        self.get_logger().info(f"I calculated the angle = {rotation_angle}")
        self.get_logger().info(f"I calculated the directio of the rotation: {rotation_direction}")

        return rotation_angle, rotation_direction