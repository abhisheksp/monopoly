import game_phases.game_phase
from game_state.property_type import PropertyType


class SpecialProperty(game_phases.game_phase.GamePhase):
    def __init__(self):
        pass

    def apply(self, game_context, action=None):
        current_player = game_context.state.current_player
        if current_player.position.type == PropertyType.CHANCE:
            self._play_chance(game_context.state)
        game_context.phase = game_context.get_phase('BSMT')
        return game_context, None

    def __repr__(self):
        return 'Special Property Phase'

    def _play_chance(self, game_state):
        next_chance = game_state.board.next_chance()
        current_player = game_state.current_player
        if next_chance == 0:
            current_player.position = game_state.board.property_at(0)
            current_player.increment(200)
