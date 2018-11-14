import game_phases.game_phase


class DiceRoll(game_phases.game_phase.GamePhase):
    def __init__(self, dice):
        self._dice = dice

    def apply(self, game_state, action=None):
        dice_roll = self._dice.roll()
        game_state.current_player.update_roll(dice_roll)
        if not game_state.current_player.double_roll():
            game_state.next_player()
        return self, game_state
