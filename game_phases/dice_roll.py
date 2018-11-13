import game_phases.game_phase


class DiceRoll(game_phases.game_phase.GamePhase):
    def __init__(self, dice):
        self._dice = dice

    @staticmethod
    def _double_roll(roll):
        return roll[0] == roll[1]

    def apply(self, game_state, action=None):
        dice_roll = self._dice.roll()
        if not self._double_roll(dice_roll):
            game_state.next_player()
        game_state.current_player.update_roll(dice_roll)
        return self, game_state
