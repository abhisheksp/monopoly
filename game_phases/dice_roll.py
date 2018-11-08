import game_phases.game_phase
from random import seed, randint


class DiceRoll(game_phases.game_phase.GamePhase):
    def __init__(self):
        seed(6690106822)

    def apply(self, game_state, action=None):
        dice_roll = randint(1, 7)
        if not game_state.current_player.double_roll(dice_roll):
            game_state.next_player()
        game_state.current_player.update_roll(dice_roll)
        return self, game_state
