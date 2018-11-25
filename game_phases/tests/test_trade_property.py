from unittest import TestCase

from game_phases import Context
from game_phases.trade_property import TradeProperty
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class TradePropertyTest(TestCase):
    def test_selling_property(self):
        trade_property_phase = TradeProperty()
        board = Board()
        player_1 = Player(1, amount=500, position=board.property_at(1))
        player_2 = Player(2, amount=500, position=board.property_at(0))
        players = [player_1, player_2]
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_1)
        baltic_avenue = board.property_at(3)
        baltic_avenue.own(player_1)
        reading_railroad = board.property_at(5)
        reading_railroad.own(player_2)
        oriental_avenue = board.property_at(6)
        oriental_avenue.own(player_2)

        trades = [
            {'buyer': player_2, 'seller': player_1, 'price': 200, 'properties': [mediterranean_avenue, baltic_avenue]},
            {'buyer': player_1, 'seller': player_2, 'price': 400, 'properties': [reading_railroad, oriental_avenue]}
        ]

        game_state = GameState(players, board)
        game_phase = trade_property_phase
        context = Context({}, game_state, game_phase)
        action = trades

        context.apply(action)

        self.assertEqual(player_1.amount,  500 + 200 - 400)
        self.assertEqual(player_2.amount, 500 - 200 + 400)
        self.assertTrue(mediterranean_avenue.owned_by is player_2)
        self.assertTrue(baltic_avenue.owned_by is player_2)
        self.assertTrue(reading_railroad.owned_by is player_1)
        self.assertTrue(oriental_avenue.owned_by is player_1)
