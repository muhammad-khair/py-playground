from typing import Set, Iterator, List
from unittest import TestCase


def primes(limit: int) -> Iterator[int]:
    multiples: Set[int] = set()
    for number in range(2, limit + 1):
        if number in multiples:
            continue
        for multiple in range(number * 2, limit + 1, number):
            multiples.add(multiple)
        yield number


class TestIterator(TestCase):
    def test_primes_iterator_small(self):
        expected_primes = [2, 3, 5, 7]
        collected_primes: List[int] = []
        for number in primes(10):
            collected_primes.append(number)
        self.assertEqual(expected_primes, collected_primes)

    def test_primes_iterator(self):
        expected_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        collected_primes: List[int] = []
        for number in primes(100):
            collected_primes.append(number)
        self.assertEqual(expected_primes, collected_primes)
