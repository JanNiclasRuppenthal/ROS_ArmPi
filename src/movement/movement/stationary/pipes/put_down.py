import time

from movement.stationary.pipes.common_movement import Movement
from object_detection.detected_object import DetectedObject

class PutDownMovement(Movement):
    def __init__(self, AK):
        super().__init__("movement_put_down_node", AK)

    def put_down_grabbed_object(self, detected_object : DetectedObject):
        # Go to the position of the object with z = 7
        result = self._AK.setPitchRangeMoving((detected_object.get_x(), detected_object.get_y(), 7), -90, -90, 0)
        self.get_logger().info(f"Put down the grabbed object back at ({detected_object.get_x()}, {detected_object.get_y()}, 7) with the following values: {result}")
        time.sleep(result[2]/1000)

        # move the arm to the previous position of the grabbed pipe
        self._move_to_detected_object(detected_object)

        self.open_claw()

    def put_down_assembled_object(self, object_type):
        # The goal position is the green field left to the robot
        goal_coord_x, goal_coord_y, goal_coord_z = (-15 + 0.5, 6 - 0.5,  1.5)
        self.__put_object_at(goal_coord_x, goal_coord_y, goal_coord_z, object_type)


    def __put_object_at(self, x, y, z, object_type):
        result = self._AK.setPitchRangeMoving((x, y, 12), 10, 10, -90) # ArmPi goes to the goal coordinates with z = 12
        time.sleep(result[2]/1000)

        self._AK.setPitchRangeMoving((x, y, z + 3), 10, 10, -90, 500) # ArmPi goes down to z = goal_coord_z + 3
        time.sleep(0.5)

        z = self._get_z_coordinate(object_type)

        self._AK.setPitchRangeMoving((x, y, z), 10, 10, -90, 1000) # ArmPi is at the next coordinates
        time.sleep(0.8)

        self.open_claw()

        self._AK.setPitchRangeMoving((x, y, 12), 10, 10, -90, 800)
        time.sleep(0.8)