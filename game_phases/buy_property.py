import game_phases.game_phase


class BuyProperty(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_state = game_context.state
        current_player = game_state.current_player
        current_position = current_player.position
        if current_player.agent.buy_property(game_state):
            current_player.add_debt(bank=current_position.cost)
            bsmt_phase = game_context.get_phase('BSMT')
            game_context, _ = bsmt_phase.apply(game_context, None)
            current_position.own(current_player)
            current_player.deduct(current_position.cost)
            current_player.deduct_debt(bank=current_position.cost)
            game_context.phase = game_context.get_phase('BSMT')
        else:
            game_context.phase = game_context.get_phase('Auction')
        return game_context, None

    def __repr__(self):
        return 'Buy Property Phase'
