import game_phases.game_phase


class TurnEnd(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_state = game_context.state
        if not game_state.current_player.double_roll():
            game_state.next_player()
        game_context.phase = game_context.get_phase('DiceRoll')
        return game_context, None

    def __repr__(self):
        return 'Turn End Phase'

