"""
This module tests the examples shown in the project readme file.
"""

import unittest
from dataclasses import dataclass
from typing import Union

from pewter import add_cast, Castable, CastableValue, cast


class TestPewterExamples(unittest.TestCase):
    def test_basic_example(self):
        @dataclass
        class LipschitzQuaternion:
            x: int
            i: int
            j: int
            k: int

        def quaternion_to_int(value: LipschitzQuaternion) -> int:
            if value.i != 0 or value.j != 0 or value.k != 0:
                raise ValueError()
            return value.x

        add_cast(LipschitzQuaternion, int, quaternion_to_int)
        quarternion = LipschitzQuaternion(3, 0, 0, 0)
        self.assertEqual(cast(quarternion, int), 3)
        self.assertEqual(cast(5, int), 5)

    def test_example_without_generics(self):
        class LikeThree:
            pass

        class LikeFour:
            pass

        add_cast(LikeThree, int, lambda value: 6)
        add_cast(LikeFour, int, lambda value: 7)

        def triple(value: Union[int, LikeThree, LikeFour]) -> int:
            return cast(value, int) * 3

        self.assertEqual(triple(LikeThree()), 18)
        self.assertEqual(triple(LikeFour()), 21)

    def test_example_with_generics(self):
        class LikeThree(Castable[int]):
            pass

        class LikeFour(Castable[int]):
            pass

        add_cast(LikeThree, int, lambda value: 3)
        add_cast(LikeFour, int, lambda value: 4)

        def triple(value: CastableValue[int]) -> int:
            return cast(value, int) * 3

        self.assertEqual(triple(LikeThree()), 9)
        self.assertEqual(triple(LikeFour()), 12)


if __name__ == "__main__":
    unittest.main()
