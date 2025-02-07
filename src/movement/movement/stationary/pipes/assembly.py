import time

from movement.stationary.pipes.common_movement import Movement


class AssemblyMovement(Movement):
    def __init__(self):
        super().__init__("movement_assembly_node")

    def go_to_assembly_position(self, x, y, z, angle):
        # Go into the right position
        result = self._AK.setPitchRangeMoving((x, y, z), angle, angle, 0)
        self.get_logger().info(f"Move to the received assembly position ({x}, {y}, {z}) and the ange {angle} with the following values: {result}")
        time.sleep(result[2]/1000)

    def go_to_upper_position(self):
        result = self._AK.setPitchRangeMoving((0, 12.5, 20), -90, -90, 0)
        self.get_logger().info(f"Move to the upper position (0, 12.5, 20) with the following values: {result}")
        time.sleep(result[2]/1000)

    def assembly_objects(self, x, y, z, angle):
        # we need to mirror the x coordinate
        # because both robots face each other
        result = self._AK.setPitchRangeMoving((-x, y, z), angle, angle, 0)
        self.get_logger().info(f"Move to the assembly position ({-x}, {y}, {z}) and angle {angle} with the following values: {result}")
        time.sleep(result[2]/1000)

        time.sleep(1)

        result = self._AK.setPitchRangeMoving((-x, y, z - 6), angle, angle, 0)
        self.get_logger().info(f"Move down to ({-x}, {y}, {z - 6}) and angle {angle} with the following values: {result}")
        time.sleep(result[2]/1000)

        self.open_claw()

    def move_back_to_y_25(self, x, z, angle):
        result = self._AK.setPitchRangeMoving((-x, 25, z - 6), angle, angle, 0)
        self.get_logger().info(f"Move back to y = 25 ({-x}, 25, {z - 6}) and angle {angle} with the following values: {result}")
        time.sleep(result[2]/1000)

        # go to the init position again
        self.init_move()

    def move_to_origin(self, height):
        result = self._AK.setPitchRangeMoving((0, 20, height), 10, 10, 20)
        self.get_logger().info(f"Move back to the origin position of the map (0, 20, {height}) with the following values: {result}")
        time.sleep(result[2]/1000)