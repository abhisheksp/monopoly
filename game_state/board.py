from game_state.property import Property
from game_state.property_type import PropertyType


class Board:
    def __init__(self):
        # TODO: expand entire board and include rents
        self._squares = [
            Property('Go', None, 0, PropertyType.UNOWNED),
            Property('Mediterranean Avenue', None, 100, PropertyType.UNOWNED),
            Property('Community Chest', None, 0, PropertyType.COMMUNITY_CHEST),
            Property('Baltic Avenue', None, 300, PropertyType.UNOWNED),
            Property('Income Tax', None, 0, PropertyType.UNOWNED),
            Property('Reading Railroad', None, 200, PropertyType.UNOWNED),
            Property('Oriental Avenue', None, 300, PropertyType.UNOWNED),
            Property('Chance', None, 0, PropertyType.CHANCE)
        ]
        self._reverse_index = {property_: i for i, property_ in enumerate(self._squares)}

    def move(self, current_position, dice_roll):
        current_position_idx = self._reverse_index[current_position]
        new_position_idx = (current_position_idx + sum(dice_roll)) % len(self._squares)
        return self._squares[new_position_idx]

    def property_at(self, position):
        return self._squares[position]

    def __repr__(self):
        repr_str = '********** BOARD ***********\n'
        for square in self._squares:
            if square.type == PropertyType.OWNED:
                repr_str += '{} owns {}\n'.format(square.owned_by.id, square.name)
        repr_str += '****************************\n'
        return repr_str
