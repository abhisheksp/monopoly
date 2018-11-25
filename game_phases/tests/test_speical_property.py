from unittest import TestCase
from unittest.mock import MagicMock

from game_phases import Context
from game_phases.bsmt import BSMT
from game_phases.special_property import SpecialProperty
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class SpecialPropertyTest(TestCase):
    def test_chance_0(self):
        bsmt_phase = BSMT()
        special_property_phase = SpecialProperty()
        phases = {
            'BSMT': bsmt_phase,
            'SepcialProperty': special_property_phase,
        }
        board = Board()
        board.next_chance = MagicMock(return_value=0)
        player_1 = Player(1, amount=200, position=board.property_at(1))
        player_2 = Player(2, amount=200, position=board.property_at(36))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_state.next_player()
        game_phase = special_property_phase
        context = Context(phases, game_state, game_phase)
        new_context, next_action = context.apply()
        go = board.property_at(0)

        self.assertTrue(new_context.phase is bsmt_phase)
        self.assertTrue(player_2.position is go)
        self.assertEqual(player_2.amount, 400)
        self.assertEqual(player_1.amount, 200)
