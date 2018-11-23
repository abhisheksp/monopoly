from unittest import TestCase

from game_phases import Context
from game_phases.bsmt import BSMT
from game_phases.sell_house import SellHouse
from game_state.bank import Bank
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class SellHouseTest(TestCase):
    def test_apply(self):
        sell_house_phase = SellHouse()
        bsmt_phase = BSMT()
        phases = {
            'SellHouse': sell_house_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        player_1 = Player(1, amount=500, position=board.property_at(1))
        player_2 = Player(2, amount=500, position=board.property_at(0))
        players = [player_1, player_2]
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_1)
        mediterranean_avenue.build(2)
        mediterranean_avenue.build_costs = {'House': 100}
        bank = Bank()
        game_state = GameState(players, board, bank=bank)
        game_phase = sell_house_phase
        context = Context(phases, game_state, game_phase)
        action = (mediterranean_avenue, 'House', 1)

        new_context, next_action = context.apply(action)

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertEqual(mediterranean_avenue.houses, 1)
        self.assertEqual(player_1.amount, 550)
        self.assertEqual(player_2.amount, 500)
