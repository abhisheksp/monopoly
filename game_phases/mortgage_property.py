import game_phases.game_phase
from game_state.property_type import PropertyType


class MortgageProperty(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        property_ = action
        owner = property_.owned_by
        if property_.type == PropertyType.OWNED:
            property_.mortgage()
            owner.increment(property_.mortgage_value)
        elif property_.type == PropertyType.MORTGAGED:
            property_.unmortgage()
            unmortgage_price = property_.mortgage_value * 1.1
            owner.deduct(unmortgage_price)
        return game_context, None

    def __repr__(self):
        return 'Mortgage Property Phase'
