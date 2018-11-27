import game_phases.game_phase
from game_state.property_type import PropertyType


class SpecialProperty(game_phases.game_phase.GamePhase):
    def __init__(self, dice=None):
        self._dice = dice

    def apply(self, game_context, action=None):
        current_player = game_context.state.current_player
        if current_player.position.type == PropertyType.CHANCE:
            game_context = self._play_chance(game_context)
        return game_context, None

    def __repr__(self):
        return 'Special Property Phase'

    def _play_chance(self, game_context):
        game_state = game_context.state
        next_chance = game_state.board.next_chance()
        current_player = game_state.current_player
        go_amount = 200
        if next_chance == 0:
            go = game_state.board.property_at(0)
            current_player.position = go
            current_player.increment(go_amount)
            game_context.phase = game_context.get_phase('BSMT')
        elif next_chance == 1:
            illinois_avenue = game_state.board.property_at(24)
            self._teleport_player(game_state, illinois_avenue)
            game_context.phase = game_context.get_phase('BSMT')
        elif next_chance == 2:
            st_charles_place = game_state.board.property_at(11)
            self._teleport_player(game_state, st_charles_place)
            game_context.phase = game_context.get_phase('BSMT')
        elif next_chance == 3:
            new_position = game_state.board.nearest_utility(current_player.position)
            current_player.position = new_position
            if new_position.type == PropertyType.UNOWNED:
                game_context.phase = game_context.get_phase('BuyProperty')
            elif new_position.type == PropertyType.OWNED and new_position.owned_by is not current_player:
                dice_roll = self._dice.roll()
                penalty = 10 * sum(dice_roll)
                owner = new_position.owned_by
                owner.increment(penalty)
                current_player.deduct(penalty)
                game_context.phase = game_context.get_phase('BSMT')
            else:
                game_context.phase = game_context.get_phase('BSMT')
        elif next_chance in (4, 5):
            new_position = game_state.board.nearest_railroad(current_player.position)
            current_player.position = new_position
            if new_position.type == PropertyType.UNOWNED:
                game_context.phase = game_context.get_phase('BuyProperty')
            elif new_position.type == PropertyType.OWNED and new_position.owned_by is not current_player:
                penalty = 10 * new_position.rent()
                owner = new_position.owned_by
                owner.increment(penalty)
                current_player.deduct(penalty)
                game_context.phase = game_context.get_phase('BSMT')
            else:
                game_context.phase = game_context.get_phase('BSMT')
        elif next_chance == 12:
            st_charles_place = game_state.board.property_at(5)
            self._teleport_player(game_state, st_charles_place)
            game_context.phase = game_context.get_phase('BSMT')
        elif next_chance == 13:
            board_walk = game_state.board.property_at(39)
            current_player.position = board_walk
            game_context.phase = game_context.get_phase('BSMT')
        return game_context

    def _teleport_player(self, game_state, new_position):
        go_amount = 200
        current_player = game_state.current_player
        old_position = current_player.position
        current_player.position = new_position
        increment_amount = go_amount if game_state.board.passes_go(old_position, new_position) else 0
        current_player.increment(increment_amount)
