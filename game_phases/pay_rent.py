import game_phases.game_phase


class PayRent(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        current_player = game_context.state.current_player
        rent = current_player.position.rent()
        current_player.add_debt(opponents=rent)
        bsmt_phase = game_context.get_phase('BSMT')
        game_context, _ = bsmt_phase.apply(game_context, None)
        if current_player.debt() > current_player.amount:
            game_context.phase = game_context.get_phase('TurnEnd')
        else:
            current_player.deduct(rent)
            current_player.deduct_debt(opponents=rent)
            owner = current_player.position.owned_by
            owner.increment(rent)
            game_context.phase = game_context.get_phase('BSMT')
        return game_context, None

    def __repr__(self):
        return 'Pay Rent Phase'

