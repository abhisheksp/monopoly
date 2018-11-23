from unittest import TestCase

from game_phases import Context
from game_phases.bsmt import BSMT
from game_phases.buy_house import BuyHouse
from game_state.bank import Bank
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class BuyHouseTest(TestCase):
    def test_apply(self):
        buy_house_phase = BuyHouse()
        bsmt_phase = BSMT()
        phases = {
            'BuyHouse': buy_house_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        player_1 = Player(1, amount=500, position=board.property_at(1))
        player_2 = Player(2, amount=500, position=board.property_at(0))
        players = [player_1, player_2]
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_1)
        mediterranean_avenue.build_costs = {'House': 100}
        bank = Bank()
        game_state = GameState(players, board, bank=bank)
        game_phase = buy_house_phase
        context = Context(phases, game_state, game_phase)
        action = (mediterranean_avenue, 'House', 2)

        new_context, next_action = context.apply(action)

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertEqual(mediterranean_avenue.houses, 2)
        self.assertEqual(player_1.amount, 300)
        self.assertEqual(player_2.amount, 500)
