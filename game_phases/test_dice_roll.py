import unittest
from game_phases.dice_roll import DiceRoll
from game_state.player import Player
from game_state.game_state import GameState


class DiceRollTest(unittest.TestCase):
    def test_apply_different_dice_roll(self):
        dice_roll = DiceRoll()
        player_1 = Player(1)
        player_2 = Player(2)
        players = [player_1, player_2]
        game_state = GameState(players)

        new_phase, new_state = dice_roll.apply(game_state)

        self.assertTrue(isinstance(new_phase, DiceRoll))
        self.assertTrue(new_state.current_player is player_2)

    def test_apply_same_dice_roll(self):
        dice_roll = DiceRoll()
        previous_rolls = 0, 6
        player_1 = Player(1, previous_rolls)
        player_2 = Player(2)
        players = [player_1, player_2]
        game_state = GameState(players)

        new_phase, new_state = dice_roll.apply(game_state)

        self.assertTrue(isinstance(new_phase, DiceRoll))
        self.assertTrue(new_state.current_player is player_1)

if __name__ == '__main__':
    unittest.main()
