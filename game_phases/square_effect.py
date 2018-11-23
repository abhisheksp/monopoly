import game_phases.game_phase
from game_state.property_type import PropertyType


class SquareEffect(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        game_state = game_context.state
        current_player = game_state.current_player
        if current_player.position.type == PropertyType.UNOWNED:
            game_context.phase = game_context.get_phase('BuyProperty')
        elif current_player.position.owned_by is current_player:
            game_context.phase = game_context.get_phase('DiceRoll')
        else:
            game_context.phase = game_context.get_phase('PayRent')
        return game_context, None

    def __repr__(self):
        return 'Square Effect Phase'

