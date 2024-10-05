from pewter import cast, add_cast, Castable, CastableValue

import unittest


class DistanceMetres:
    metres: int

    def __init__(self, metres: int):
        self.metres = metres


class DistanceKilometres(Castable[DistanceMetres]):
    kilometres: int

    def __init__(self, kilometres: int):
        self.kilometres = kilometres


class TravelDistance(DistanceKilometres):
    crow_flies: bool

    def __init__(self, kilometres: int, crow_flies: bool):
        super().__init__(kilometres)
        self.crow_flies = crow_flies


def kilometres_to_metres(value: DistanceKilometres) -> DistanceMetres:
    return DistanceMetres(value.kilometres * 1000)


add_cast(DistanceKilometres, DistanceMetres, kilometres_to_metres)


class TestPewter(unittest.TestCase):
    def test_kilometres_to_metres(self):
        kilometres = DistanceKilometres(4)
        metres = cast(kilometres, DistanceMetres)
        self.assertEqual(metres.metres, 4000)

    def test_subtype(self):
        travel_distance = TravelDistance(6, True)
        basic_distance = cast(travel_distance, DistanceKilometres)
        self.assertEqual(basic_distance.crow_flies, True)  # type: ignore

    def test_incompatible(self):
        with self.assertRaises(TypeError):
            cast(4, tuple)

    def test_redefine(self):
        def bad_converter(value: DistanceKilometres) -> DistanceMetres:
            return DistanceMetres(23)

        with self.assertRaises(Exception):
            add_cast(DistanceKilometres, DistanceMetres, bad_converter)

    def test_function(self):
        """This also validates MyPy typing."""

        def distance_string(
            distance: CastableValue[DistanceMetres],
        ) -> str:
            cast_distance = cast(distance, DistanceMetres)
            return f"{cast_distance.metres} metres"

        distance = DistanceKilometres(3)
        self.assertEqual(distance_string(distance), "3000 metres")


if __name__ == "__main__":
    unittest.main()
