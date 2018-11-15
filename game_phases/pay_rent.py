import game_phases.game_phase


class PayRent(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_context.phase = game_context.get_phase('BSMT')
        return game_context

    def __repr__(self):
        return 'Pay Rent Phase'

