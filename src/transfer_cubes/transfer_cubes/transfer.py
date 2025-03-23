import time
from threading import Thread

from rclpy.node import Node

from ArmIK.ArmMoveIK import *

from movement.stationary.cubes.stack import StackCube
from robot.armpi import ArmPi

from robot.publisher.delivery_publisher import DeliveryPublisher
from robot.publisher.finish_publisher import FinishPublisher
from robot.subscriber.delivery_subscriber import DeliverySubscriber
from robot.subscriber.finish_subscriber import FinishSubscriber
from common.executor.executor_subscriptions import MultiExecutor
from movement.stationary.cubes.coordinates import CoordinatesCalculation
from movement.stationary.cubes.deliver import DeliverCube

from util.cam import Cam



class TransferCubes(Node):
    def __init__(self, ID, last_robot):
        super().__init__("transfer_cubes_node")
        self.__first_start = ID == 0
        AK = ArmIK()
        self.__armpi = ArmPi(ID, last_robot)
        self.__cam = Cam()
        self.__coordinates_calculation = CoordinatesCalculation()

        if last_robot:
            self.__movement = StackCube(AK)
        else:
            self.__movement = DeliverCube(AK)

        self.__create_nodes()

        # start executor for all subscribers
        self.__start_executor()

    def __create_nodes(self):
        self.__delivery_publisher = DeliveryPublisher(self.__armpi)
        self.__finish_publisher = FinishPublisher(self.__armpi)
        self.__delivery_subscriber = DeliverySubscriber(self.__armpi)
        self.__finish_subscriber = FinishSubscriber(self.__armpi)

    def __start_executor(self):
        subscriber_nodes = [self.__delivery_subscriber, self.__finish_subscriber]
        self.__executor = MultiExecutor(subscriber_nodes)
        thread = Thread(target=self.__executor.start_spinning)
        thread.start()
        self.get_logger().info("Started the executor for all subscriber nodes in a thread!")

    def start_scenario(self):
        self.__cam.open()
        self.get_logger().info("Opened the camera!")

        self.__movement.init_move()
        self.get_logger().info("Move to my initial position!")
        time.sleep(2)

        while True:
            if self.did_previous_robot_finished() and self.found_no_cubes():
                self.get_logger().info("Previous robot finished and I found no cubes!")
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

    def end_scenario(self):
        self.__finish_publisher.send_msgs()
        self.__executor.execute_shutdown()
        self.__cam.shutdown()
        self.get_logger().info("Ended the scenario!")

    def did_previous_robot_finished(self):
        return self.__armpi.get_finish_flag() or self.__armpi.get_ID() == 0

    def notify_robots(self):
        self.__delivery_publisher.send_msgs()
        self.__armpi.set_delivery_flag(False)