import json

from game_state.property import Property
from game_state.property_type import PropertyType


class Board:
    def __init__(self):
        def json_mapper(square):
            name = square['name']
            color = square['color']
            cost = square['value']
            rent = {
                0: int(square['rent']),
                1: int(square['rent_house_1']),
                2: int(square['rent_house_2']),
                3: int(square['rent_house_3']),
                4: int(square['rent_house_4']),
                5: int(square['rent_hotel']),
            }
            mortgage_value = 0
            build_costs = {'House': square['build_cost'], 'Hotel': square['build_cost']}
            type_ = PropertyType.SPECIAL if square['type'] in ('Chance', 'Chest') else PropertyType.UNOWNED
            group = []
            if int(square['group_size']) > 0:
                group = list(map(int, square['group']))
            return Property(name, color, cost, type_, build_costs=build_costs, mortgage_value=mortgage_value, rent=rent,
                            group=group)

        with open('board.json') as f:
            board_data = json.load(f)
            properties = dict(map(lambda x: (int(x[0]), json_mapper(x[1])), board_data.items()))
            for _, property_ in properties.items():
                property_.group = list(map(lambda x: properties[x], property_.group))
            self._squares = properties

        self._reverse_index = {property_: i for i, property_ in self._squares.items()}

    def move(self, current_position, dice_roll):
        current_position_idx = self._reverse_index[current_position]
        new_position_idx = (current_position_idx + sum(dice_roll)) % 40
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
