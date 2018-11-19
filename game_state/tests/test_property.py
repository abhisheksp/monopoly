import unittest
from unittest import TestCase

from game_state.player import Player
from game_state.property import Property


class PropertyTest(TestCase):
    def test_regular_rent(self):
        rent = {0: 200}
        property_1 = Property('Mediterranean Ave', None, None, None, rent=rent)
        player = Player(1)
        property_1.own(player)
        self.assertEqual(property_1.rent(), 200)

    def test_double_rent(self):
        rent = {0: 200}
        property_1 = Property('Mediterranean Ave', None, None, None, rent=rent)
        property_2 = Property('Baltic Ave', None, None, None, None)
        player = Player(1)
        property_1.own(player)
        property_2.own(player)
        property_1.group = [property_2]
        property_2.group = [property_1]

        self.assertEqual(property_1.rent(), 400)

    def test_rent_with_houses(self):
        rent = {1: 400}
        property_1 = Property('Mediterranean Ave', None, None, None, houses=1, rent=rent)
        property_2 = Property('Baltic Ave', None, None, None, None)
        player = Player(1)
        property_1.own(player)
        property_2.own(player)
        property_1.group = [property_2]
        property_2.group = [property_1]

        self.assertEqual(property_1.rent(), 400)


if __name__ == '__main__':
    unittest.main()
