from unittest import TestCase
from unittest.mock import MagicMock

from game_phases import Context
from game_phases.bsmt import BSMT
from game_phases.pay_rent import PayRent
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class PayRentTest(TestCase):
    def test_apply_regular_property(self):
        bsmt_phase = BSMT()
        pay_rent_phase = PayRent()
        phases = {
            'BSMT': bsmt_phase,
            'PayRent': pay_rent_phase,
        }
        board = Board()
        player_1 = Player(1, position=board.property_at(0))
        player_2 = Player(2, amount=1000, position=board.property_at(1))
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_1)
        mediterranean_avenue.rent = MagicMock(return_value=100)
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = pay_rent_phase
        context = Context(phases, game_state, game_phase)
        new_context = context.apply()

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertEqual(new_context.state.current_player.amount, 900)
