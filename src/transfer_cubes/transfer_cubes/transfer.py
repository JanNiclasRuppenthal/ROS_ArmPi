import time
from threading import Thread

from ArmIK.ArmMoveIK import *

from movement.stationary.cubes.stack import StackCube
from robot.armpi import ArmPi

from robot.publisher.delivery_publisher import DeliveryPublisher
from robot.publisher.finish_publisher import FinishPublisher
from robot.subscriber.delivery_subscriber import DeliverySubscriber
from robot.subscriber.finish_subscriber import FinishSubscriber

from common.executor.executor_subscriptions import MultiExecutor
from movement.stationary.cubes.coordinates import CoordinatesCaluclation
from movement.stationary.cubes.deliver import DeliverCube

from util.cam import Cam



class TransferCubes:
    def __init__(self, ID, last_robot):
        AK = ArmIK()
        self.__armpi = ArmPi(ID, last_robot)
        self.__first_start = ID == 0
        self.__cam = Cam()
        self.__coordinates_calculation = CoordinatesCaluclation()
        if last_robot:
            self.__movement = StackCube(AK)
        else:
            self.__movement = DeliverCube(AK)

        # create all necessary nodes
        self.__delivery_publisher = DeliveryPublisher(self.__armpi)
        self.__finish_publisher = FinishPublisher(self.__armpi)
        self.__delivery_subscriber = DeliverySubscriber(self.__armpi)
        self.__finish_subscriber = FinishSubscriber(self.__armpi)

        # create executor for all subscriber
        subscriber_nodes = [self.__delivery_subscriber, self.__finish_subscriber]
        self.__executor = MultiExecutor(subscriber_nodes)
        self.start_executor()

    def start_executor(self):
        thread = Thread(target=self.__executor.start_spinning)
        thread.start()

    def start_scenario(self):
        self.__cam.open()

        self.__movement.init_move()
        time.sleep(2)

        while True:
            if self.did_previous_robot_finished() and self.found_no_cubes():
                self.end_scenario()
                break

            if self.allowed_to_deliver_cube():

                if self.__first_start:
                    self.__first_start = False

                world_X, world_Y = self.__coordinates_calculation.get_coordinates(self.__cam)

                if self.__movement.are_coordinates_valid(world_X, world_Y):
                    rotation_angle = self.__coordinates_calculation.get_rotation_angle()
                    detected_color = self.__coordinates_calculation.get_detected_color()
                    self.__movement.move_cube(world_X, world_Y, rotation_angle, detected_color)

                    #publish message
                    self.notify_robots()

    def allowed_to_deliver_cube(self):
        return self.__armpi.get_delivery_flag() or self.__first_start

    def found_no_cubes(self):
        return (-1, -1) == self.__coordinates_calculation.get_coordinates(self.__cam)

    def did_previous_robot_finished(self):
        return self.__armpi.get_finish_flag() or self.__armpi.get_ID() == 0

    def notify_robots(self):
        self.__delivery_publisher.send_msgs()
        self.__armpi.set_delivery_flag(False)

    def end_scenario(self):
        self.__finish_publisher.send_msgs()
        self.__executor.execute_shutdown()
        self.__cam.shutdown()