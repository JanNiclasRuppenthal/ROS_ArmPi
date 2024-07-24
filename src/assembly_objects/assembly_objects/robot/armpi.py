class ArmPi():
    def __init__(self, ID):
        self.ID = ID
        self.ready = False 

    def get_ID(self):
        return self.ID

    def get_ready_flag(self):
        return self.ready

    