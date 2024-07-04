class ArmPi():
    def __init__(self):
        self.__got_delivery = False

    def set_delivery_flag(self, flag):
        self.__got_delivery = flag

    def get_delivery_flag(self):
        return self.__got_delivery