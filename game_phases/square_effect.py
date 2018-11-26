import game_phases.game_phase
from game_state.property_type import PropertyType


class SquareEffect(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_state = game_context.state
        current_player = game_state.current_player
        current_position = current_player.position
        if current_position.type is PropertyType.UNOWNED:
            game_context.phase = game_context.get_phase('BuyProperty')
        elif current_position.type is PropertyType.MORTGAGED or current_position.owned_by is current_player:
            game_context.phase = game_context.get_phase('BSMT')
        else:
            game_context.phase = game_context.get_phase('PayRent')
        return game_context, None

    def __repr__(self):
        return 'Square Effect Phase'

