from typing import Any, Dict, Tuple
from unittest import TestCase


def read_arguments(*many_args: int) -> Tuple[int]:
    return many_args


def read_keywords(**many_keys) -> Dict[str, Any]:
    return many_keys


def read_params(first, second, /, third, *, fourth):
    print(first, second, third, fourth)


class TestParameters(TestCase):
    def test_arguments(self):
        args = read_arguments(1, 2, 3)
        self.assertEqual((1, 2, 3), args)

    def test_keywords(self):
        keywords = read_keywords(first=1, second=2)
        self.assertEqual({"first": 1, "second": 2}, keywords)

    def test_params_label_fourth(self):
        read_params(1, 2, 3, fourth=4)

    def test_params_label_third_fourth(self):
        read_params(1, 2, third=3, fourth=4)
