import game_phases.game_phase


class BuyHouse(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_state = game_context.state
        property_, build_type, count = action
        player = property_.owned_by
        if game_state.bank.houses_available:
            property_.build(count)
            build_cost = property_.build_costs[build_type] * count
            player.deduct(build_cost)
        return game_context, None

    def __repr__(self):
        return 'Buy House Phase'
