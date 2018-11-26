import json
from collections import defaultdict

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
            types_ = defaultdict(lambda: PropertyType.UNOWNED)
            types_['Chance'] = PropertyType.CHANCE
            types_['Chest'] = PropertyType.COMMUNITY_CHEST
            types_['Chance Special'] = PropertyType.JAIL_CHANCE
            types_['Community Chest Special'] = PropertyType.JAIL_COMMUNITY_CHEST
            type_ = types_[square['type']]
            group = []
            if int(square['group_size']) > 0:
                group = list(map(int, square['group']))
            return Property(name, color, cost, type_, build_costs=build_costs, mortgage_value=mortgage_value, rent=rent,
                            group=group)

        with open('/Users/abhisheksp/workspace/monopoly/board.json') as f:
            board_data = json.load(f)
            properties = dict(map(lambda x: (int(x[0]), json_mapper(x[1])), board_data.items()))
            for _, property_ in properties.items():
                property_.group = list(map(lambda x: properties[x], property_.group))
            self._squares = properties

        self._reverse_index = {property_: i for i, property_ in self._squares.items()}

        self._chance_top = -1
        self._community_chest_top = -1

    def move(self, current_position, dice_roll):
        current_position_idx = self._reverse_index[current_position]
        new_position_idx = (current_position_idx + sum(dice_roll)) % 40
        return self._squares[new_position_idx]

    def passes_go(self, old_position, new_position):
        pass

    def nearest_utility(self, position):
        pass

    def nearest_railroad(self, position):
        pass

    def property_at(self, position):
        return self._squares[position]

    def next_chance(self):
        self._chance_top = (self._chance_top + 1) % 16
        return self._chance_top

    def next_community_chest(self):
        self._community_chest_top = (self._community_chest_top + 1) % 16
        return self._community_chest_top

    def __repr__(self):
        repr_str = '********** BOARD ***********\n'
        for _, square in self._squares.items():
            if square.type == PropertyType.OWNED:
                repr_str += '{} owns {}\n'.format(square.owned_by.id, square.name)
        repr_str += '****************************\n'
        return repr_str
