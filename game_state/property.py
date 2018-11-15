from game_state.property_type import PropertyType


class Property:
    def __init__(self, name, color, cost, type_, player=None):
        self.name = name
        self.color = color
        self.cost = cost
        self.owned_by = player
        self.type = type_

    def own(self, player):
        self.owned_by = player
        self.type = PropertyType.OWNED

    def __repr__(self):
        return '{}'.format(self.name)