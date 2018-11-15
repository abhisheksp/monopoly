import game_phases.game_phase


class BuyProperty(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_state = game_context.state
        current_player = game_state.current_player
        if current_player.agent.buy_property(game_state):
            current_player.position.own(current_player)
            # TODO: change financial resources
        game_context.phase = game_context.get_phase('BSMT')
        return game_context
