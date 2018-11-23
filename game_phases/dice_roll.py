import game_phases.game_phase


class DiceRoll(game_phases.game_phase.GamePhase):
    def __init__(self, dice=None):
        self._dice = dice

    def apply(self, context, action=None):
        game_state = context.state
        dice_roll = self._dice.roll()
        current_player = game_state.current_player
        current_player.update_roll(dice_roll)
        new_position = game_state.board.move(current_player.position, dice_roll)
        current_player.update_position(new_position)
        context.phase = context.get_phase('SquareEffect')
        return context, None

    def __repr__(self):
        return 'Dice Roll Phase'

