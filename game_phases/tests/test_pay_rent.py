from unittest import TestCase
from unittest.mock import MagicMock

from game_phases import Context
from game_phases.bsmt import BSMT
from game_phases.pay_rent import PayRent
from game_phases.turn_end import TurnEnd
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class PayRentTest(TestCase):
    @staticmethod
    def fake_bsmt_cycle(amount):
        def return_func(context, _):
            context.state.current_player.increment(amount)
            return context, None
        return return_func

    def test_apply(self):
        bsmt_phase = BSMT()
        pay_rent_phase = PayRent()
        turn_end_phase = TurnEnd()
        phases = {
            'BSMT': bsmt_phase,
            'PayRent': pay_rent_phase,
            'TurnEnd': turn_end_phase,
        }
        board = Board()
        player_1 = Player(1, amount=100, position=board.property_at(0))
        player_2 = Player(2, amount=10, position=board.property_at(1))
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_1)
        rent = 100
        mediterranean_avenue.rent = MagicMock(return_value=rent)
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = pay_rent_phase
        context = Context(phases, game_state, game_phase)
        bsmt_phase.apply = self.fake_bsmt_cycle(rent)

        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertEqual(new_context.state.current_player.amount, 10)
        self.assertEqual(player_1.amount, 200)

    def test_apply_player_bankrupt(self):
        bsmt_phase = BSMT()
        pay_rent_phase = PayRent()
        turn_end_phase = TurnEnd()
        phases = {
            'BSMT': bsmt_phase,
            'PayRent': pay_rent_phase,
            'TurnEnd': turn_end_phase,
        }
        board = Board()
        player_1 = Player(1, position=board.property_at(0))
        player_2 = Player(2, amount=10, position=board.property_at(1))
        mediterranean_avenue = board.property_at(1)
        mediterranean_avenue.own(player_1)
        rent = 100
        mediterranean_avenue.rent = MagicMock(return_value=rent)
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = pay_rent_phase
        context = Context(phases, game_state, game_phase)
        bsmt_phase.apply = self.fake_bsmt_cycle(rent - 20)

        new_context, next_action = context.apply()

        self.assertTrue(new_context.phase is turn_end_phase)
        self.assertEqual(new_context.state.current_player.amount, 90)
