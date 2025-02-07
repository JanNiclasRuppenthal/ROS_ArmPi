from movement.stationary.cubes.common_movement import Movement
from movement.stationary.cubes.grab import GrabCube


class StackCube(Movement):
    def __init__(self, AK):
        Movement.__init__(self, "stationary_stack_node", AK)
        self.__grab_cube = GrabCube(AK)

        self.__coordinates = {
            'red':   (-15 + 0.5, 12 - 0.5, 1.5),
            'green': (-15 + 0.5, 6 - 0.5,  1.5),
            'blue':  (-15 + 0.5, 0 - 0.5,  1.5)
        }

        self.__count_placed_colored_cubes = {
            'red':   0,
            'green': 0,
            'blue':  0
        }


    def move_cube(self, x, y, rotation_angle, detected_color):
        grabbed_cube = self.__grab_cube.grab_cube(x, y, rotation_angle)
        if grabbed_cube:
            self._move_arm_up(x, y, 1)

            goal_coord_x, goal_coord_y, goal_coord_z = self.__calculate_goal_coordinates(detected_color)
            self._move_to_goal_coordinate(goal_coord_x, goal_coord_y, goal_coord_z)
            self.get_logger().info(f"I moved the cube to ({goal_coord_x}, {goal_coord_y}, {goal_coord_z})")

            self.__grab_cube.open_claw()

            self._move_arm_up(goal_coord_x, goal_coord_y, 0.8)

            self.__count_placed_colored_cubes[detected_color] += 1

            # move back to the initial position
            self.init_move()


    def __calculate_goal_coordinates(self, detected_color):
        goal_coord_x, goal_coord_y, goal_coord_z = self.__coordinates[detected_color]
        goal_coord_z += self.__count_placed_colored_cubes[detected_color] * 2.5
        self.get_logger().info(f"Calculated coordinates: ({goal_coord_x}, {goal_coord_y}, {goal_coord_z})")

        return goal_coord_x, goal_coord_y, goal_coord_z