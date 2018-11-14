from game_state.property import Property
from game_state.property_type import PropertyType


class Board:
    def __init__(self):
        self._squares = [
            Property('Go', None, None, PropertyType.UNOWNED),
            Property('Mediterranean Avenue', None, None, PropertyType.UNOWNED),
            Property('Community Chest', None, None, PropertyType.COMMUNITY_CHEST),
            Property('Baltic Avenue', None, None, PropertyType.UNOWNED),
            Property('Income Tax', None, None, PropertyType.UNOWNED),
            Property('Reading Railroad', None, None, PropertyType.UNOWNED),
            Property('Oriental Avenue', None, None, PropertyType.UNOWNED),
            Property('Chance', None, None, PropertyType.CHANCE)
        ]
        self._reverse_index = {property_: i for i, property_ in enumerate(self._squares)}

    def move(self, current_position, dice_roll):
        current_position_idx = self._reverse_index[current_position]
        new_position_idx = current_position_idx + sum(dice_roll)
        return self._squares[new_position_idx]

    def property_at(self, position):
        return self._squares[position]
