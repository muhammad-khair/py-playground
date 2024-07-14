from abc import ABCMeta, abstractmethod
from unittest import TestCase


class VehicleInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, 'speed')
            and hasattr(subclass, 'move') and callable(subclass.move)
            or NotImplemented
        )

    @property
    @abstractmethod
    def speed(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def move(self, distance: int) -> int:
        raise NotImplementedError


class Car(VehicleInterface):
    @property
    def speed(self) -> int:
        return 10

    def move(self, distance: int) -> int:
        return distance + self.speed


class TestABC(TestCase):
    def test_vehicle_instance(self):
        self.assertIsInstance(Car(), VehicleInterface)

    def test_property(self):
        self.assertEqual(Car().speed, 10)

    def test_method(self):
        self.assertEqual(Car().move(5), 15)
