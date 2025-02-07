import time

from movement.stationary.pipes.common_movement import Movement


class HandoverMoves(Movement):
    def __init__(self):
        super().__init__("movement_handover_node")

    def go_to_handover_position(self, ID):
        height = self.__calculate_height(ID)
        result = self._AK.setPitchRangeMoving((0, 20, height), 5, 5, 15)
        self.get_logger().info(f"Move to the handover position (0, 20, {height}) with the following values: {result}")
        time.sleep(result[2]/1000)

        # rotate the claw again
        initial_rotation_value_of_claw = 500
        self._rotate_claw_with_value(initial_rotation_value_of_claw)

    def move_back_from_handover_position(self, ID):
        height = self.__calculate_height(ID)
        result = self._AK.setPitchRangeMoving((0, 18, height), 5, 5, 15)
        self.get_logger().info(f"Move back from the handover position to (0, 18, {height}) with the following values: {result}")
        time.sleep(result[2]/1000)

    def __calculate_height(self, ID):
        height = 0
        if ID == 0:
            height = 28
        elif ID == 1:
            height = 26.5


        self.get_logger().info(f"Calculated the height = {height}")
        return height

    def move_down_from_handover_position(self):
        result = self._AK.setPitchRangeMoving((0, 18, 20), 5, 5, 15)
        self.get_logger().info(f"Move down from the handover position to (0, 18, 20) with the following values: {result}")
        time.sleep(result[2]/1000)