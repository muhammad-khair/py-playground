from functools import wraps
from typing import Callable
from unittest import TestCase


def doubles(function: Callable):
    @wraps(function)
    def wrapper(*args, **kwargs):
        result = function(*args, **kwargs)
        if result is not None:
            return result * 2
        return None
    return wrapper


@doubles
def echo(number: int) -> int:
    return number


class TestDecorator(TestCase):
    def test_decorator(self):
        self.assertEqual(8, echo(4))
