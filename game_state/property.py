from game_state.property_type import PropertyType


class Property:
    def __init__(self, name, color, cost, type_, rent=0, group=None, player=None):
        self.name = name
        self.color = color
        self.cost = cost
        self.owned_by = player
        self.type = type_
        self.group = group
        if group is None:
            self.group = []
        self._rent = rent

    def own(self, player):
        self.owned_by = player
        self.type = PropertyType.OWNED

    def rent(self):
        result = self._rent
        group_owned = all(map(lambda property_: self.owned_by is property_.owned_by, self.group))
        if self.group and group_owned:
            result = self._rent * 2
        return result

    def __repr__(self):
        return '{}'.format(self.name)
