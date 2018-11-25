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
        go_amount = 200
        if next_chance == 0:
            go = game_state.board.property_at(0)
            current_player.position = go
            current_player.increment(go_amount)
        elif next_chance == 1:
            illinois_avenue = game_state.board.property_at(24)
            old_position = current_player.position
            current_player.position = illinois_avenue
            increment_amount = go_amount if game_state.board.passes_go(old_position, illinois_avenue) else 0
            current_player.increment(increment_amount)
