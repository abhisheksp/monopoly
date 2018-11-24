import game_phases.game_phase


class SellHouse(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_state = game_context.state
        property_, build_type, count = action
        player = property_.owned_by
        if game_state.bank.houses_available:
            property_.sell_buildings(count)
            selling_price = (property_.build_costs[build_type] * count) / 2
            player.increment(selling_price)
        return game_context, None

    def __repr__(self):
        return 'Sell House Phase'
