class DetectedObject:
    def __init__ (self, x, y, angle, rotation_direction, object_type):
        self.__x = x
        self.__y = y
        self.__angle = angle
        self.__rotation_direction = rotation_direction
        self.__object_type = object_type


    def are_coordinates_valid(self):
        return self.__x == -1 and self.__y == -1

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_angle(self):
        return self.__angle

    def get_rotation_direction(self):
        return self.__rotation_direction

    def get_object_type(self):
        return self.__object_type
