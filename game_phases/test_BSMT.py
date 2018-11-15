from unittest import TestCase

from game_phases.bsmt import BSMT
from game_phases.context import Context
from game_phases.dice_roll import DiceRoll
from game_state.board import Board
from game_state.game_state import GameState
from game_state.player import Player


class TestBSMT(TestCase):
    def test_change_player_on_regular_roll(self):
        dice_roll_phase = DiceRoll()
        bsmt_phase = BSMT()
        phases = {
            'DiceRoll': dice_roll_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        regular_roll = ((1, 2), (2, 3))
        player_1 = Player(1, position=board.property_at(1), previous_rolls=regular_roll)
        player_2 = Player(2, position=board.property_at(0))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_phase = bsmt_phase
        context = Context(phases, game_state, game_phase)
        new_context = context.apply()

        self.assertTrue(new_context.phase is dice_roll_phase)
        self.assertTrue(new_context.state.current_player is player_2)

    def test_change_player_on_double_roll(self):
        dice_roll_phase = DiceRoll()
        bsmt_phase = BSMT()
        phases = {
            'DiceRoll': dice_roll_phase,
            'BSMT': bsmt_phase,
        }
        board = Board()
        double_roll = ((1, 2), (2, 2))
        player_1 = Player(1, position=board.property_at(1), previous_rolls=double_roll)
        player_2 = Player(2, position=board.property_at(0))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_phase = bsmt_phase
        context = Context(phases, game_state, game_phase)
        new_context = context.apply()

        self.assertTrue(new_context.phase is dice_roll_phase)
        self.assertTrue(new_context.state.current_player is player_1)
