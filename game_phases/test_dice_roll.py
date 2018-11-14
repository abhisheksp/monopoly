import unittest
import utils.dice
from game_phases.context import Context
from game_phases.dice_roll import DiceRoll
from game_phases.square_effect import SquareEffect
from game_state.board import Board
from game_state.player import Player
from game_state.game_state import GameState

from unittest.mock import MagicMock


class DiceRollTest(unittest.TestCase):
    def test_apply(self):
        dice = utils.Dice()
        dice.roll = MagicMock(return_value=(1, 2))
        dice_roll_phase = DiceRoll(dice)
        square_effect_phase = SquareEffect()
        phases = {
            'DiceRoll': dice_roll_phase,
            'SquareEffect': square_effect_phase,
        }
        board = Board()
        player_1 = Player(1, position=board.property_at(0))
        player_2 = Player(2, position=board.property_at(0))
        players = [player_1, player_2]
        game_state = GameState(players, board)
        game_phase = dice_roll_phase
        context = Context(phases, game_state, game_phase)
        new_context = context.apply()

        self.assertTrue(new_context.phase is square_effect_phase)
        self.assertTrue(new_context.state.current_player.position is board.property_at(3))


if __name__ == '__main__':
    unittest.main()
